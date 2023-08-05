"""This module contains the :class:`.MosaikInterfaceComponent`, which
cares for all the precious sensors and actuators.

"""
import json
from copy import copy

import numpy as np
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.types import Box
from palaestrai_mosaik.config import AGENT_FULL_ID
from palaestrai_mosaik.environment import LOG


class MosaikInterfaceComponent:
    """The mosaik interface component stores all sensors and actuators.

    Parameters
    ----------

    sensors : list
        List of sensor descriptions. A sensor description should either
        be an instance of
        :class:`palaestrai.agent.sensor_information.SensorInformation`
        or a dict like::

            sensor = {
                # Unique identifier of the sensor containing the
                # Simulator ID, the Entity ID, and the attribute name
                "sensor_id": <sid.eid.attr>,
                # String description of an *palaestrai.types* object
                "observation_space": "Box(low=0.0, high=1.2, "
                                     "shape=(1,), dtype=np.float32)",
            }

    actuators : list
        List of actuator descriptions. An actuator description should
        either be an instance of
        :class:`palaestrai.agent.actuator_information.ActuatorInformation`
        or a dict like::

            actuator = {
                # Unique identifier of the actuator containing the
                # Simulator ID, the Entity ID, and the attribute name
                "actuator_id": <sid.eid.attr>,
                # String description of an *palaestrai.types* object
                "action_space": "Box(low=0.0, high=1.2, "
                                "shape=(1,), dtype=np.float32)",
            }

    seed : int, optional
        A seed for the random number generator (rng). When more than
        one agent provides values for the same actuator, one of the
        values is randomly chosen.

    Attributes
    ----------
    sensors : list
        A *list* containing all :class:`~.SensorInformation` objects.
    actuators : list
        A *list* containing all :class:`~.ActuatorInformation` objects.
    senmap : dict
        A *dict* that stores the index of each sensor as value.
    actmap : dict
        A *dict* that stores the index of each actuator as value.

    """

    def __init__(self, sensors, actuators, seed=None):
        self.sensors = sensors
        self.actuators = actuators

        self.sensor_map = dict()
        self.actuator_map = dict()

        self._rng = np.random.RandomState(seed)

    def create_sensors(self):
        """Create sensors from the sensor description.

        The description is provided during initialization.

        Returns
        -------
        list
            The *list* containing the created sensor objects.

        """
        sensors = list()
        for idx, sensor in enumerate(self.sensors):
            if isinstance(sensor, SensorInformation):
                sensors.append(SensorInformation)
                uid = sensor.sensor_id
            else:
                uid = sensor["sensor_id"]
                space = sensor["observation_space"]
                sensors.append(
                    SensorInformation(
                        sensor_id=uid,
                        observation_space=Box.from_string(space),
                        sensor_value=0,
                    )
                )
            self.sensor_map[uid] = copy(sensors[-1])
        self.sensors = sensors
        return self.sensors

    def create_actuators(self):
        """Create actuators from the actuator description.

        The description is provided during initialization.

        Returns
        -------
        list
            The *list* containing the created actuator objects.

        """
        actuators = list()
        for idx, actuator in enumerate(self.actuators):
            if isinstance(actuator, ActuatorInformation):
                actuators.append(actuator)
            else:
                uid = actuator["actuator_id"]
                space = actuator["action_space"]

                actuators.append(
                    ActuatorInformation(
                        setpoint=None,
                        actuator_id=uid,
                        action_space=Box.from_string(space),
                    )
                )
            self.actuator_map[uid] = copy(actuators[-1])

        self.actuators = actuators
        return self.actuators

    def trigger_sensors(self, world, time):
        """Fill the sensors with fresh data from mosaik.

        This method is called from within the mosaik process.
        At each sync point (i.e., the :class:`.ARLSyncSimulator` is
        stepping), all current outputs of the simulators are written
        into the sensors.

        Parameters
        ----------
        world : :class:`mosaik.scenario.World`
            The current world object.
        time : int
            The current simulation time

        """
        for sid, entities in getattr(world, "_df_cache")[time].items():
            for eid, attrs in entities.items():
                for attr, val in attrs.items():
                    key = f"{sid}.{eid}.{attr}"

                    if key not in self.sensor_map:
                        continue

                    LOG.debug("Trying to access sensor %s.", key)
                    try:
                        sensor = copy(
                            [
                                sen
                                for sen in self.sensors
                                if sen.sensor_id == key
                            ][0]
                        )
                    except IndexError:
                        LOG.warning(
                            "Sensor with id %s not found in available "
                            "sensors. Skipping this one.",
                            key,
                        )
                        continue
                    try:
                        val = check_value(val)
                    except TypeError:
                        LOG.warning(
                            "The type of value %s (%s) from sensor %s "
                            "could not be mapped to one of (int, float"
                            ", str, bool). Setting this value to None!",
                            val,
                            type(val),
                            key,
                        )
                        val = None
                    log_val = (
                        "{ ... }"
                        if (
                            val is not None
                            and isinstance(val, str)
                            and len(val) > 100
                        )
                        else val
                    )

                    LOG.info("Reading value %s from sensor %s.", log_val, key)
                    sensor.sensor_value = val
                    self.sensor_map[key] = sensor

    def get_sensor_readings(self):
        """Get all current sensor readings.

        This method is called from within the communication process.

        Returns
        -------
        list
            The *list* with all sensors and updated values.

        """
        return list(self.sensor_map.values())

    def update_actuators(self, actuators):
        """Update the actuator values.

        This method is called from within the communication process.
        All actuator values from *actuators* are written into
        :attr:`.actuator_map`.

        Parameters
        ----------
        actuators : list
            A *list* of actuator values. The values should be wrapped
            in :class:`.ActuatorInformation` objects, otherwise no
            guarantee can be given that the values are assigned
            correctly.

        """

        for idx, actuator in enumerate(actuators):
            assert isinstance(actuator, ActuatorInformation), (
                "provided actuator is not an instance of "
                f"{ActuatorInformation.__class__}."
            )

            if actuator.actuator_id not in self.actuator_map:
                LOG.warning(
                    "Encountered unknown actuator %s. Skipping.",
                    actuator.actuator_id,
                )
                continue

            try:

                val = check_value(actuator.setpoint)
            except TypeError:
                LOG.warning(
                    "The type of value %s (%s) from actuator %s could "
                    " not be mapped to one of (int, float, str"
                    ", bool). Setting this value to None!",
                    val,
                    type(val),
                    actuator.actuator_id,
                )
                val = None

            actuator.setpoint = val
            self.actuator_map[actuator.actuator_id] = actuator

    def trigger_actuators(self, sim, input_data):
        """Forward the actuator values to the specific simulators.

        This method is called from within the mosaik process.
        In contrast to the sensor calls, the actuators can only be
        triggered per simulator. Each simulator calls the mosaik
        scheduler to fetch its *input_data*. After the normal fetching
        process, the input_data dict is filled with inputs for the
        simulator *sim*.

        In this method, all actuators are checked wether they have
        "better" data or the specific input of the simulator. These
        values are updated and the old values will be overwritten. Then
        the actuators are resetted, i.e., setpoints are set to None.

        The *input_data* is then returned to the scheduler, which
        passes them to the calling simulator.

        Notes
        -----
            It is possible that some simulators may rely on multiple
            inputs for a certain attribute and throw an error after the
            ARL injection, or filter for specific data provider and,
            therefore, ignore the ARL input. As soon as this case
            occurs, this method should be adapted accordingly.

        Parameters
        ----------
        sim : :class:`mosaik.scenario.ModelMock`
            The *ModelMock* of the simulator calling the
            :func:`.get_input_data` function of the mosaik scheduler.
        input_data : dict
            The currently gathered input data for this simulator.
            ARL tries to manipulate them.

        """

        for key, actuator in self.actuator_map.items():
            act_sid, act_eid, attr = key.split(".")
            if sim.sid != act_sid:
                continue
            LOG.debug("Trying to access actuator %s.", key)

            try:
                setpoint = restore_value(actuator.setpoint)
            except TypeError:
                LOG.warning(
                    "Could not restore value %s (%s) of actuator %s. "
                    "Skipping!",
                    actuator.setpoint,
                    type(actuator.setpoint),
                    key,
                )
                continue

            if setpoint is None:
                LOG.debug(
                    "The setpoint of actuator %s is None. Skipping!", key
                )
                continue

            LOG.debug(
                "Trigger actuator for %s with value %s",
                key,
                setpoint,
            )

            if attr not in input_data.setdefault(act_eid, dict()):
                input_data[act_eid][attr] = dict()
                LOG.info(
                    "Attribute %s not found in the input_data of this "
                    "simulator. Creating this entry may be cause of "
                    "some strange and unexpected behavior ...",
                    attr,
                )

            if AGENT_FULL_ID in input_data[act_eid][attr]:
                input_data[act_eid][attr][AGENT_FULL_ID].append(setpoint)

            LOG.info("Setting value %s to actuator %s.", setpoint, key)
            input_data[act_eid][attr] = {AGENT_FULL_ID: [setpoint]}

            self.actuator_map[key] = None

        for model, attrs in input_data.items():
            for attr, src_ids in attrs.items():
                if AGENT_FULL_ID not in src_ids:
                    continue
                assert len(src_ids) == 1
                if len(src_ids[AGENT_FULL_ID]) > 1:
                    LOG.debug(
                        "It seems more than one agent already tried to"
                        " manipulate this entry: found values %s."
                        "May fate decide the outcome of this battle "
                        "...",
                        src_ids[AGENT_FULL_ID],
                    )
                    setpoint = np.random.choice(src_ids[AGENT_FULL_ID])
                else:
                    setpoint = src_ids[AGENT_FULL_ID][0]
                src_ids[AGENT_FULL_ID] = setpoint


def check_value(val):
    if val is None:
        return val
    elif isinstance(val, str):
        return str(val)
    elif isinstance(val, dict):
        return str(json.dumps(val))
    elif isinstance(val, bool):
        return val
    elif val == int(val):
        return int(val)
    elif val == float(val):
        return float(val)
    else:
        raise TypeError


def restore_value(val):
    if val is None:
        return val
    elif isinstance(val, str):
        try:
            return json.load(val)
        except ValueError:
            return val
    elif isinstance(val, bool):
        return val
    elif val == int(val):
        return int(val)
    elif val == float(val):
        return float(val)
    else:
        raise TypeError

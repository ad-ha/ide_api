from __future__ import annotations
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
    PLATFORM_SCHEMA,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    SensorEntity,
)
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    POWER_KILO_WATT,
    DEVICE_CLASS_POWER,
    ENERGY_KILO_WATT_HOUR,
    DEVICE_CLASS_ENERGY,
)
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.helpers.config_validation as cv

__VERSION__ = "0.2.1"

from oligo.asyncio import AsyncIber
from oligo.exception import IberException

DOMAIN = "ide"
DATA_UPDATED = "i-DE Sensor Update"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)

ENERGY_SENSORS = [
    SensorEntityDescription(
        key="power",
        native_unit_of_measurement=POWER_KILO_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        name="Current Consumption",
    ),
    SensorEntityDescription(
        key="energy",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        name="Meter Reading",
    ),
]

SCAN_INTERVAL = timedelta(minutes=60)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:

    """Set up the sensor platform."""
    async_add_entities(
        [
            IDESensor(
                config,
                "Meter Reading",
                "meterReading",
                ENERGY_KILO_WATT_HOUR,
                DEVICE_CLASS_ENERGY,
                STATE_CLASS_TOTAL_INCREASING,
            )
        ],
        True,
    )


class IDESensor(RestoreEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, config, name, variable, unit, deviceclass, stateclass):

        _LOGGER.debug("Initalizing Entity {}".format(name))

        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._variable = variable
        self._unit = unit
        self._deviceclass = deviceclass
        self._stateclass = stateclass
        self._attributes = {}
        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state
        _LOGGER.warning(
            "i-DE Meter could not be updated. Last reading available was restored: {}".format(
                self._state
            )
        )

        async_dispatcher_connect(
            self.hass, DATA_UPDATED, self._schedule_immediate_update
        )

    @callback
    def _schedule_immediate_update(self):
        """Schedule Update when possible"""
        self.async_schedule_update_ha_state(True)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "iDE Meter Reading"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return self._deviceclass

    @property
    def state_class(self):
        return self._stateclass

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        connection = AsyncIber()
        try:
            await connection.login(self.username, self.password)
            self._state = await connection.current_kilowatt_hour_read()
            _LOGGER.debug("Meter Data {}".format(self._state))
        except IberException as exception:
            raise exception
        finally:
            await connection.close()

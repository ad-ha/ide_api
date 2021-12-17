from __future__ import annotations
from datetime import timedelta
import logging

import requests
from requests.exceptions import ConnectTimeout, HTTPError
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
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    POWER_KILO_WATT,
    DEVICE_CLASS_POWER,
    ENERGY_KILO_WATT_HOUR,
    DEVICE_CLASS_ENERGY,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import (
    HomeAssistantType,
    ConfigType,
    DiscoveryInfoType,
)
import homeassistant.helpers.config_validation as cv

from .ide_api import IdeAPI

__VERSION__ = "0.0.1b"

DOMAIN = "ide"

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


# async def async_setup(hass: HomeAssistantType, hass_config: dict):
#    haconfig = hass_config[DOMAIN]
#    has_credentials = CONF_USERNAME in haconfig and CONF_PASSWORD in haconfig
#    if not has_credentials:
#        _LOGGER.debug("No credentials provided")
#    return True


SCAN_INTERVAL = timedelta(minutes=120)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:

    """Set up the sensor platform."""
    # username = config[CONF_USERNAME]
    # password = config[CONF_PASSWORD]

    # ideClient = IDESensor(username, password)

    add_entities(
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


class IDESensor(SensorEntity):
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
        # self.meter = {}

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
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        ides = IdeAPI(self.username, self.password)
        ides.login()
        meter = ides.watthourmeter()

        _LOGGER.debug("Meter Data {}".format(meter))
        #        r = ides.get_cups()
        #
        #        try:
        #            for c in r["data"]["lstCups"]:
        #                if c["Name"] == self._cups:
        #                    cups_id = c["Id"]
        #        except AttributeError:
        #            cups_id = r["data"]["lstCups"][0]["Id"]
        #            self._cups = r["data"]["lstCups"][0]["Name"]

        #        _LOGGER.debug(f"Fetching data for CUPS={self._cups} with Id={cups_id}")

        # attributes = {}
        # attributes["Meter State"] = meter["json_response"]["icp"]
        # attributes["Current Consumptionl"] = meter["json_response"]["consumption"]
        # attributes["Meter Reading"] = meter["json_response"]["meter"]
        # attributes["Potencia Contratada"] = (
        #    str(meter["data"]["potenciaContratada"]) + " kW"
        # )
        self._state = meter
        # self._attributes = attributes

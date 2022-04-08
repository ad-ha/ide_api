import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_ID
from homeassistant.helpers.typing import HomeAssistantType

__VERSION__ = "0.2.0"

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ide"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_ID): cv.string,
    }
)


async def async_setup(hass: HomeAssistantType, config):
    has_credentials = CONF_USERNAME in config and CONF_PASSWORD in config and CONF_ID in config
    if not has_credentials:
        _LOGGER.debug("No credentials provided")
    return True

from .ide_api import IdeAPI
import asyncio
import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.exceptions import HomeAssistantError
from requests.exceptions import ConnectTimeout, HTTPError
from aiohttp import ClientConnectionError

__VERSION__ = "0.1.0"

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ide"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)


async def async_setup(hass: HomeAssistantType, config):
    has_credentials = CONF_USERNAME in config and CONF_PASSWORD in config
    if not has_credentials:
        _LOGGER.debug("No credentials provided")
    return True

import logging
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

__VERSION__ = "0.1.0"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigEntry) -> bool:
    has_credentials = CONF_USERNAME in config and CONF_PASSWORD in config
    if not has_credentials:
        _LOGGER.debug("No credentials provided")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    #hass.async_create_task(
    #    hass.config_entries.async_forward_entry_setup(entry, "sensor")
    #)
    return True

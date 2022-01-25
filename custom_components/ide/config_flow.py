from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    })


class IdeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        await self.async_set_unique_id('ide_unique')
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title='Contrato xxxx', data=user_input)

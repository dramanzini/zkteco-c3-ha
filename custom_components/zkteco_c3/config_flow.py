import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD

from .const import (
    DOMAIN,
    CONF_DOOR_NAMES,
    CONF_OPEN_DURATION,
    DEFAULT_PORT,
    DEFAULT_OPEN_DURATION,
    CONF_DOOR_COUNT,
    DEFAULT_DOOR_COUNT,
)

class ZKTecoC3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]

            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"ZKTeco C3 {host}",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required(CONF_PASSWORD): str,
            vol.Optional(CONF_OPEN_DURATION, default=DEFAULT_OPEN_DURATION): int,
        vol.Optional(CONF_DOOR_COUNT, default=DEFAULT_DOOR_COUNT): int,

        vol.Optional(CONF_DOOR_NAMES, default="Door1,Door2,Door3,Door4"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

from homeassistant.components.lock import LockEntity
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PASSWORD
from homeassistant.helpers.entity import DeviceInfo

from c3 import C3
from c3.controldevice import ControlDeviceOutput

from .const import DOMAIN, CONF_DOOR_NAMES, CONF_OPEN_DURATION, DEFAULT_PORT, DEFAULT_OPEN_DURATION, CONF_DOOR_COUNT, DEFAULT_DOOR_COUNT


async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    password = entry.data[CONF_PASSWORD]
    open_duration = entry.data.get(CONF_OPEN_DURATION, DEFAULT_OPEN_DURATION)

    raw_names = entry.data.get(
        CONF_DOOR_NAMES,
        "Door1,Door2,Door3,Door4"
    )

    names = [name.strip() for name in raw_names.split(",") if name.strip()]
    door_count = entry.data.get(CONF_DOOR_COUNT, DEFAULT_DOOR_COUNT)

    entities = []
    for index, name in enumerate(names[:door_count], start=1):
        entities.append(
            ZKTecoC3Lock(
                entry_id=entry.entry_id,
                host=host,
                port=port,
                password=password,
                open_duration=open_duration,
                door_number=index,
                name=name,
            )
        )

    async_add_entities(entities)


class ZKTecoC3Lock(LockEntity):
    def __init__(self, entry_id, host, port, password, open_duration, door_number, name):
        self._entry_id = entry_id
        self._host = host
        self._port = port
        self._password = password
        self._open_duration = open_duration
        self._door_number = door_number

        self._attr_name = name
        self._attr_unique_id = f"zkteco_c3_{host}_door_{door_number}"
        self._is_locked = True

    @property
    def is_locked(self):
        return self._is_locked

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=f"ZKTeco C3 {self._host}",
            manufacturer="ZKTeco",
            model="C3 Access Controller",
        )

    def unlock(self, **kwargs):
        panel = C3(self._host, self._port)

        try:
            if not panel.connect(self._password):
                raise Exception("No conectó/autenticó contra el C3")

            cmd = ControlDeviceOutput(
                output_number=self._door_number,
                address=1,
                duration=self._open_duration,
            )

            panel.control_device(cmd)

            self._is_locked = False
            self.schedule_update_ha_state()

            def relock():
                self._is_locked = True
                self.schedule_update_ha_state()

            self.hass.loop.call_later(self._open_duration, relock)

        finally:
            try:
                panel.disconnect()
            except Exception:
                pass

    def lock(self, **kwargs):
        self._is_locked = True
        self.schedule_update_ha_state()


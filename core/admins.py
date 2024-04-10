
from fastapi import WebSocket
from .settings import BASIC


class Settings:
    def __init__(self) -> None:
        pass

    # adding key value
    def _parse_setting(self, key, setting):
        setting["key"] = key
        return setting
 
    def get_settings(self):
        return [self._parse_setting(key, v.get_setting()) for key, v in BASIC.items()]

    def update_settings(self, new_settings):
        for key, value in new_settings.items():       # theme | value
            setting = BASIC.get(key)
            # if key found
            if setting and value != setting.get_value():      # if setting chnaged
                BASIC[key].set_value(value)

    def get_basic_settings(self):
        return BASIC

class Admin:
    def __init__(self, admin_key, admin_name) -> None:
        self.admin_key = admin_key
        self.name = admin_name
        
        self.websocket: WebSocket | None = None
        
    async def send_json_data(self, data):
        if self.websocket:
            await self.websocket.send_json(data)
    
    async def send_output(self, output: str):
        await self.send_json_data({ "output": output  + "\n"})

    @property
    def admin_active(self):
        if self.websocket == None: return False
        return True
    
    async def notify(self, message: str):
        pass

# super admin
class Admins:
    def __init__(self) -> None:
        super().__init__()

        self.admins = {}
        self.settings = Settings()
    
    def add_admin(self, key, name):
        self.admins[key] = Admin(key, name)

    def get_settings(self):
        return self.settings.get_settings()

    def check_admin(self, key) -> Admin | None:
        return self.admins.get(key)
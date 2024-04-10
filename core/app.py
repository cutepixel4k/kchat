from fastapi import FastAPI

from .errors import AdminExecuteError
from .admins import Admin, Admins
from config.config import ADMINS
from .rooms import RoomsManager


class AdminExecute:
    def __init__(self) -> None:
        pass

    def parse(self, data):
        try:
            return data.get("input").strip().split(";")
        except:
            raise AdminExecuteError("Error on parsing command")

    # rooms
    async def rooms_command(self, admin: Admin, rooms_manager: RoomsManager, args: list):
        sub_command = args[0]

        # delete rooms
        if sub_command == "delete":
            agressive = False
            if "-a" in args:
                agressive = True
            await rooms_manager.delete_room(args[1], agressive)
            
            return "Successfully deleted"

        # create rooms
        elif sub_command == "create":
            rooms_manager.create_room(*args[1:])
            return "Successfully created"

        raise AdminExecuteError("Command not found")

class MainApp(FastAPI):
    def __init__(self) -> None:
        super().__init__()
        self.admins = Admins()      # single super admin
        self.rooms_manager = RoomsManager()               # all rooms manager
        self.admin_execute = AdminExecute()

        self.active_admins = []

        self._add_admins_from_config()

        # ---------------- creating default rooms
        self.rooms_manager.create_room("Spidy", "FUN 😎", "vip", max_limit=10)
        self.rooms_manager.create_room("Spidy", "LOVE 😍", "vip", max_limit=10)

    def _add_admins_from_config(self):
        for admin_key, name in ADMINS.items():
            self.admins.add_admin(admin_key, name)
   
    def admin_connect(self, admin):
        self.active_admins.append(admin)

    def admin_disconnect(self, admin):
        self.active_admins.remove(admin)

    async def execute_admin_command(self, admin: Admin, data: dict):
        try:
            lines = self.admin_execute.parse(data)

            for line in lines:
                splitted = line.strip().split(" ")
                # if command related to rooms
                if splitted[0] == "rooms":
                    out = await self.admin_execute.rooms_command(admin, self.rooms_manager, splitted[1:])

                    await admin.send_output(out)
                else:
                    raise AdminExecuteError("Command not found")
        except AdminExecuteError as e:
            await admin.send_output(str(e))

        except Exception as e:
            await admin.send_output(str(e))
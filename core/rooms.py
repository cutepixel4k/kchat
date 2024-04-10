from uuid import uuid4

from .admins import Admin
from .errors import AdminExecuteError, ClientError
from .settings import get_setting
from .clients import Client

from uuid import uuid4
import shortuuid


def generate_short_id():
    return shortuuid.uuid()

def generate_uid():
    return uuid4().hex

class Room:
    def __init__(self, room_name: str, room_id: str, username: str, user_id: str, password: str | None = None, private = False, max_limit = 2, room_type = "public", ) -> None:
        self.room_type = room_type

        self.room_id = room_id
        self.username = username
        self.room_name = room_name

        self.max_limit = max_limit
        self.current_users = 0

        self.user_id = user_id
        self.private = private

        self.password = password

        self.room_description = "Hey dont be bad, be friendly 😉"

        self.clients: dict[str, Client] = {}
        self.active_admins: list[Admin] = []

    async def cast_admin_output(self, message: str):
        for admin in self.active_admins:
            await admin.send_output(message)

    # bug may be found
    @property
    def has_password(self):
        if self.password == None:
            return False
        else:
            return True

    @property
    def room_limit(self):
        return f"{self.current_users} / {self.max_limit}"

    def get_room_members(self):
        return list(self.clients.keys())

    # dont use its raw broad cast // data = object
    async def broadcast_raw(self, data):    
        for i in self.clients.values():
            await i.send_personal_data(data)

    # raw broadcast
    async def broadcast_command(self, cmd: str, values):
        await self.broadcast_raw({ "cmd": cmd, "values": values })

    # cmd = msg | values = { username, message }
    async def broadcast_message(self, client: Client, message, cmd = "message"):
        values = { "message": message, "username": client.username, "msgid": generate_short_id() }
        await self.broadcast_command(cmd, values)

    async def braodcast_notify(self, client: Client, values):
        await self.broadcast_command("notify", values)

    async def send_personal_data(self, username, data):
        user = self.clients.get(username)
        if user:
            await user.send_personal_data(data)

    # client add error # error after room created
    async def add_client(self, client: Client):
        if client.username in self.clients.keys(): raise Exception("Username already exists in group")
        if self.current_users == self.max_limit: raise Exception("Room is full 😭")

        self.clients[client.username] = client
        self.current_users += 1

        # data for notify command
        values = {
            "username": client.username,
            "message": "Entered Chat",
            "room_limit": self.room_limit
        }
        # data for message command
        data = {"cmd": "success", "values": { 
            "userName": client.username,
            "userID": client.client_id, 
            "roomID": self.room_id,
            "roomName": self.room_name,
            "roomDescription": self.room_description
        }}

        await client.send_personal_data(data)       # sending succesfull connection
        await self.braodcast_notify(client, values) # sending notify to eveyone

        # ------------------- send to admin
        await self.cast_admin_output(f"{client.username} Joined Room 😁")

    # only notifes to users and removes in clients
    async def remove_client(self, client: Client, notify_message = "Left room"):
        # Need exception handling
        self.clients.pop(client.username)
        self.current_users -= 1

        # sending room details for all users
        # TODO only keep important keys
        if self.current_users > 0:
            values = {
                "id": self.room_id,
                "room_name": self.room_name,
                "username": client.username,
                "message": notify_message,

                "room_limit": self.room_limit
            }
            await self.braodcast_notify(client, values)

    # make global method
    def get_details(self):
        hasPassword = False
        if self.password: hasPassword = True

        return {
            "roomID": self.room_id, 
            "roomName": self.room_name, 
            "roomUsername": self.username, 
            "hasPassword": hasPassword,

            "roomLimit": self.room_limit
        }

    def get_full_details(self):
        details = self.get_details()

        return details

    def set_public(self):
        self.private = False

    def set_private(self):
        self.private = True

    # ------------------------- admins commands TODO
    async def kick_client(self, client_username, reason = "You have been kicked by Admin"):
        client = self.clients.get(client_username)
        if client == None: raise AdminExecuteError("WTF user not found in room 🙄")

        # await self.remove_client(client, "Kicked By Admin")
        await client.websocket.close(reason=reason)

class RoomsManager:
    def __init__(self) -> None:
        self.active_rooms = 0
        # notify everything
        self.vip_rooms: dict[str, Room] = {}
        self.rooms: dict[str, Room] = {}
        # random rooms
        # self.random: list[Admin] = []

    # TODO: Need optimization
    async def room_connect(self, client: Client, action: str) -> Room:
        params = client.websocket.query_params
        room_id = generate_uid()
        password = params.get('password')

        # checks
        if action == "create":
            # ------------------------------ settings
            if self.active_rooms >= get_setting("rooms_limit"):
                raise ClientError("Rooms cant create at this moment 😭")
            if get_setting("allow_new_rooms") != 'Yes':
                raise ClientError("Rooms cant create at this moment 😭")
            # room max limit
            max_limit = get_setting("new_room_limit")
            private = True      # setting private
            room_name = params.get('room_name')
            if room_name == None or room_name.strip().__len__() < 3: raise ClientError("Room name error")
            # make public by sending 0 to params
            if params.get('private') == "no": private = False

            room = Room(room_name.strip(), room_id, client.username, client.client_id, password, private, max_limit)
            # error before adding client in room
            try: await room.add_client(client)
            except Exception as e: raise ClientError(e)

            self.rooms[room_id] = room
            self.active_rooms += 1

            # print("Room created ", self.active_rooms, self.rooms)
            return room

        # done
        elif action == "join":
            room_id = params.get('room_id')
            if room_id == None: raise ClientError("Room not found (maybe)") # raise room not found

            # first checks in VIP room
            room = self.vip_rooms.get(room_id)

            if room == None: # if not found in VIP room
                room = self.rooms.get(room_id)

            # if room not found
            if room == None: raise ClientError("Room not found 😭")

            if client.username in room.clients.keys():
                raise ClientError("Username already in group 🙂") # username already exists

            # if everything ok then user added in group
            await room.add_client(client)
            return room

        else: raise ClientError("WTH is wrong zzz")

    # on message from socket
    async def on_message(self, client: Client, room: Room, data):
        # normal message
        if data["type"] == "message":
            await room.broadcast_message(client, data)

        # unsend message
        elif data["type"] == "msg-unsend":      # unsend message
            values = { "msgid": data["msgid"], "username": client.username }
            await room.broadcast_raw({ "cmd": "msg-unsend", "values": values })

        # personal message
        elif data["type"] == "secret":
            secret_username = data["secret_username"]
            if client.username == secret_username: return
            # --------------------------------------
            values = {  "username": client.username, "msgid": generate_short_id(), "type": "secret", "message": data }
            data = { "cmd": "message", "values": values }

            await room.send_personal_data(secret_username, data)
            await client.send_personal_data(data)

    # on disconnect # work on here
    async def on_disconnect(self, client, room: Room):
        # print("Client left ", client, room)
        # return if room not created
        if room == None: return

        if client:
            await room.remove_client(client)

        if room.room_type == "vip": return # dont remove if its vip

        # removing room 
        if room.current_users == 0 and room:
            try:
                self.rooms.pop(room.room_id)
                self.active_rooms -= 1
            except: pass

    def get_room(self, room_id):
        room = self.vip_rooms.get(room_id)
        if room == None:
            room = self.rooms.get(room_id)
        
        return room

    def get_room_details(self, room_id: str):
        return self.get_room(room_id)

    async def remove_user(self, room_id: str, username: str):
        vip_room = self.vip_rooms.get(room_id)
        
        if vip_room:
            client = vip_room.clients.get(username)

            if client: 
                await client.websocket.close(reason="Kicked by admin")
                await vip_room.remove_client(client, "Kicked out by admin")
        else:
            room = self.rooms.get(room_id)
        
            if room:
                client = room.clients.get(username)
            
                if client: 
                    await client.websocket.close(reason="kicked out by admin")
                    
                    await room.remove_client(client)

    # ------------------------- admins commands 
    async def delete_room(self, room_id, agressive = False, reason = "Removed by admin 😥"):
        room = self.get_room(room_id)
        if room == None: raise AdminExecuteError("WTF room not found 😑")

        for client in room.clients.values():
            # await room.remove_client(client)
            await client.websocket.close(reason = reason)
        
        if agressive and room.room_type == "vip":
            self.vip_rooms.pop(room_id)

    def create_room(self, username, room_name, tp = "public", private = False, max_limit = 2, password = None):
        room_id = uuid4().hex
        room = Room(room_name, room_id, username, uuid4().hex, password, private, max_limit, tp)

        if tp == "vip":
            self.vip_rooms[room_id] = room
        else:
            self.rooms[room_id] = room

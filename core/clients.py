# client --- every user
from fastapi import WebSocket

from .settings import get_setting
from .errors import ClientError


class Client:
    def __init__(self, username: str, websocket: WebSocket, client_id: str) -> None:
        self.client_id = client_id

        self.username = username
        self.websocket = websocket
        self.room_admin = False

    # TODO handle socket not found error
    async def send_personal_data(self, data):
        try:
            await self.websocket.send_json(data)
        # add exception here if found errors
        except: pass

# checks before creating client
def create_client(username: str, websocket: WebSocket, uid: str):
    # checking blocked users
    if get_setting("blocked_names").find(username) != -1:
        raise ClientError("Username blocked 😁")

    username = username.strip()
    usplit = username.split(' ')
    if usplit.__len__() > 1 or username.__len__() < 3 or username.__len__() > 8:
        raise ClientError("Invalid username")
    return Client(username, websocket, uid)

# 
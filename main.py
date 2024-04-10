from fastapi import Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from core.errors import AdminExecuteError, ClientError
from core.clients import create_client
from config.config import ORIGINS
from core.app import MainApp

from uuid import uuid4
from json import loads


from fastapi.staticfiles import StaticFiles



app = MainApp()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_uid():
    return uuid4().hex

# ------------------------------------------------------------------------ admin routes
@app.get("/api/admin/settings", tags=["Admin"]) # get settings    
def get_settings(admin_key: str):
    try:
        admin = app.admins.check_admin(admin_key)
        if admin == None: raise HTTPException(404, detail="Admin key not found")
        settings = app.admins.get_settings()

        return { "res": "ok", "settings": settings }
    except Exception as e:
        HTTPException(404, detail=str(e))

# TODO check key in settings and change key to be in post for security
@app.post("/api/admin/settings", tags=["Admin"])  # set settings
async def change_settings(admin_key: str, req: Request):
    # send error
    if app.admins.check_admin(admin_key) == False: raise HTTPException(404, detail="Error admin key")
    try:
        data = loads(await req.body())
        app.admins.settings.update_settings(data["body"])
        return { "res": "ok" }
    except:
        raise HTTPException(500, detail="Error updating settings")

# TODO make this post
@app.get("/api/admin/check_key")
async def check_admin_key(key: str):
    admin = app.admins.check_admin(key)
    if admin == None: raise HTTPException(404, detail="Error admin key")
    return { "res": "ok", "name": admin.name }

@app.get('/api/admin/room/details', tags=["room"])
def get_admin_room_details(room_id: str): # { status, details }
    room = app.rooms_manager.get_room(room_id)

    if room:
        return {"res": "ok", "details": room.get_full_details()}

    raise HTTPException(404, detail="Room not found")

# ------------------------------------------------------------------------
@app.get('/api/room/details', tags=["room"])
def get_room_details(room_id: str): # { status, details }
    room = app.rooms_manager.get_room_details(room_id)
    if room:
        return { "res": 200, "details": room.get_details()}
    else: raise HTTPException(404, detail="Error room not found")

# TODO need optimize - private rooms disabled on results
@app.get('/api/rooms/search', tags=["room"])
def search_room(room_name: str):
    room_name = room_name.lower()
    vip_rooms = [v.get_details() for v in app.rooms_manager.vip_rooms.values() if v.room_name.lower().startswith(room_name) and v.private == False]
    rooms = [v.get_details() for v in app.rooms_manager.rooms.values() if v.room_name.lower().startswith(room_name) and v.private == False]

    return { "vip_rooms" : vip_rooms, "rooms": rooms}

@app.get('/api/room/members', tags=["room"])
def get_room_members(room_id: str):
    try:
        room = app.rooms_manager.vip_rooms.get(room_id)
        if room:
            return { "res": "ok", "members": room.get_room_members() }
        room = app.rooms_manager.rooms.get(room_id)
        if room:
            return { "res": "ok", "members": room.get_room_members() }
    except:
        raise HTTPException(404, "Error finding members")

# room socket ----------------------------------------------------------------
# /ws/room/create/example?room_id=tests&password=hello
@app.websocket("/ws/room/{action}/{username}")
async def websocket_endpoint(websocket: WebSocket, action: str, username: str):
    await websocket.accept()
    
    room = None
    client = None

    try:
        # creating client -- just close socket if ClientError
        client = create_client(username, websocket, generate_uid())
        if action == "create": client.room_admin = True # making room admin

        # getting error starting point -- room create error if room created
        room = await app.rooms_manager.room_connect(client, action)

        # print("User connected ", client, room, room.clients)

        while True:
            data = await websocket.receive_json()
            await app.rooms_manager.on_message(client, room, data)

    except WebSocketDisconnect:
        await app.rooms_manager.on_disconnect(client, room)

    except ClientError as e:
        await websocket.close(4500, reason=str(e))
        await app.rooms_manager.on_disconnect(client, room)

# -----------------------admins websocket
@app.websocket("/ws/admin")
async def websocket_admin(websocket: WebSocket, admin_key: str):
    await websocket.accept()
    try:
        admin = app.admins.check_admin(admin_key)
        if admin == None: raise AdminExecuteError("Error key")
        # --------------------------- if everything ok then admins to room manager
        admin.websocket = websocket
        app.admin_connect(admin)
        
        while True:
            data = await websocket.receive_json()
            await app.execute_admin_command(admin, data)

    except WebSocketDisconnect:
        app.admin_disconnect(admin)

    except AdminExecuteError as e:
        await websocket.close(reason=str(e))

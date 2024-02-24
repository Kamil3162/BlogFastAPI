from fastapi import WebSocket, FastAPI, APIRouter, WebSocketDisconnect
from BlogFastAPI.app.services.WsManager import manager
import json
import datetime

create_ws_app = APIRouter()

@create_ws_app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    print(websocket, user_id)

    manager.connect(user_id, websocket)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            message = {"time": current_time, "clientId": user_id,
                       "message": data}
            await manager.broadcast(json.dumps(message))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time": current_time, "clientId": user_id,
                   "message": "Offline"}
        await manager.broadcast(json.dumps(message))


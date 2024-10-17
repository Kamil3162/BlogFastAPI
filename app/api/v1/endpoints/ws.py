import json
import datetime

from fastapi import WebSocket, FastAPI, APIRouter, WebSocketDisconnect
from ....services.ws import manager

create_ws_app = APIRouter()

@create_ws_app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    if user_id:
        await manager.connect(user_id, websocket)
        await manager.send_online_status(user_id)

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        # filter and send message to particular user based on id
        try:
            while True:
                # text get from ws/react
                data_str = await websocket.receive_text()

                try:
                    data = json.loads(data_str)
                    print(data)

                    target_user_id = data.get("target_usr")
                    source_user_id = data.get("source_usr")

                    if target_user_id:
                        ws_socket = manager.get_ws_by_userid(target_user_id)
                        # await manager.send_personal_message(
                        #     json.dumps(message), target_user_id)

                except json.JSONDecodeError:
                    print("This data isnt in json data")

                message = {"time": current_time, "clientId": user_id,
                           "message": "hello back response from server"}
                await manager.broadcast_message(message)

        except WebSocketDisconnect:
            message = {"time": current_time, "clientId": user_id,
                       "message": "Offline"}
            await manager.broadcast_message(json.dumps(message))
            await manager.disconnect(user_id)

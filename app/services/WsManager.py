from fastapi import WebSocket, FastAPI, APIRouter
from typing import List

class WsManager:
    def __init__(self):
        self.active_connections: List[str, WebSocket] = dict()

    async def connect(self, user_id: str, websocket: WebSocket):
        print("connect to ws")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, user_id: str):
        websocket = self.active_connections[user_id]
        websocket.send_text(message)

    async def broadcast_message(self, message):
        for connection in self.active_connections:
            connection.send(message)

    async def send_online_status(self):
        for user_id, connection in self.active_connections.items():
            connection.send(str(user_id))

manager = WsManager()


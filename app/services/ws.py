import json

from fastapi import WebSocket, FastAPI, APIRouter
from typing import List, Dict

class WsManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = dict()

    async def connect(self, user_id: str, websocket: WebSocket):
        print("Connecting to ws", user_id)
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str):
        connection = self.active_connections.pop(user_id, None)
        if connection:
            await connection.close()
            print("Disconnected", user_id)

    async def send_personal_message(self, message: str, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(message)
            except RuntimeError as e:
                print(f"Error sending message to {user_id}: {e}")

    async def broadcast_message(self, message):
        print("to jest broadcast message")
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(message))
            except RuntimeError:
                # Mark user for disconnection if message sending fails
                print("error broadcast message")

    async def send_online_status(self, user_id: str):
        data = {
            'type': 'info_status',
            'status': 'online',
            'user_id': user_id,
            'message': "32"
        }
        await self.broadcast_message(json.dumps(data))
    async def get_ws_by_userid(self, user_id: str):
        return self.active_connections.get(user_id)


manager = WsManager()


from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int,WebSocket] = {}
        self.__is_updated: Dict[int:bool] = {}

    async def connect(self, websocket: WebSocket, client_id:int):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        try:
            self.is_updated[client_id] = False or self.is_updated[client_id]
        except KeyError:
            self.is_updated[client_id] = False
    
    def disconnect(self, client_id:int):
        del self.active_connections[client_id]
    
    async def send_personal_message(self, message:str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message:str):
        for key, connection in self.active_connections.items():
            await connection.send_text(message)
from pydantic import BaseModel
from starlette.responses import Response, HTMLResponse
from typing import List, Dict
from fastapi import WebSocket, APIRouter,WebSocketDisconnect
from src import manageTripMode
from src.utils.ConnectionManager import ConnectionManager
import time, pickle, asyncio
router = APIRouter()

manager = ConnectionManager()

class TripModeInfo(BaseModel):
    houseId : int
    isTrip : bool
    tripFrom : str = '2018-04-04 10:00:00'
    tripTo : str = '2018-04-04 10:00:00'

@router.post("/house/tripmode")
async def manageTripmode(response:Response, tripModeInfo : TripModeInfo):
    response.status_code, result, house_id = manageTripMode.ManageTripMode().setTripMode(tripModeInfo)
    manager.is_updated[house_id] = True
    return result

@router.websocket("/ws/{client_id}")
async def db_monitor(websocket:WebSocket, client_id:int):
    await manager.connect(websocket,client_id)
    while True:
        try:
            if manager.is_updated[client_id] == True:
                await manager.send_personal_message('db updated',websocket)
                manager.is_updated[client_id] = False
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            print(f'Client #{client_id} left the chat')
        await asyncio.sleep(5) # 5초마다 확인 (비동기로)

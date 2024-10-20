import os

import uvicorn
from fastapi import FastAPI, WebSocket

from NetworkManager.WSManager import WSConnectionManager
from fastapi.middleware.cors import CORSMiddleware

from StateManager import BossState

# configuration
host = "localhost"
socket_port = 5500

app = FastAPI()
ws_connection_manager = WSConnectionManager()

origins = [
    "http://{host}:{port}".format(host=host, port=socket_port),
    "ws://{host}:{port}".format(host=host, port=socket_port),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_connection_manager.connect(websocket)
    print("Connect to: ", websocket.client.host, ":", websocket.client.port)


@app.websocket("/ws/boss/predict_state")
async def websocket_predict_boss_state(websocket: WebSocket, data):
    is_connected = True
    if not ws_connection_manager.check_connection():
        is_connected = False
        is_connected = await ws_connection_manager.connect(websocket)
    if is_connected:
        return {"state", BossState.BossState.REST}, 200
    return {"error", "cannot connect to server"}, 403


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=socket_port)

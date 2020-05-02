from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

from notifier import Notifier


app = FastAPI()
# プッシュ通知各種設定が定義されているインスタンス
notifier = Notifier()

# Websocket用のパス
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # クライアントとのコネクション確立
    await notifier.connect(websocket)
    try:
        while True:
            # クライアントからメッセージの受け取り
            data = await websocket.receive_text()
            # 双方向通信する場合
            #  await websocket.send_text(f"Message text was: {data}")
            # ブロードキャスト
            await notifier.push(f"Message text was: {data}")
    # セッションが切れた場合
    except WebSocketDisconnect:
        # 切れたセッションの削除
        notifier.remove(websocket)

# ブロードキャスト用のAPI
@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    # ブロードキャスト
    await notifier.push(f"! Push notification: {message} !")

# サーバ起動時の処理
@app.on_event("startup")
async def startup():
    # プッシュ通知の準備
    await notifier.generator.asend(None)

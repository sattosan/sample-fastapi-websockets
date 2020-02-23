from fastapi import FastAPI
from starlette.websockets import WebSocket

app = FastAPI()

# 接続中のクライアントを識別するためのヘッダを格納
clients = {}

# WebSockets用のエンドポイント
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのヘッダを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    try:
        while True:
            # クライアントからメッセージを受信
            data = await ws.receive_text()
            # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
            for client in clients.values():
                await client.send_text(f"ID: {key} | Message: {data}")
    except:
        await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]

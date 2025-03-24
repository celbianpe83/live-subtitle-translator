# test_ws_client.py
import asyncio
import websockets

async def test_subtitle():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            text = input("✏️ Escribe un subtítulo para enviar: ")
            if not text:
                break
            await websocket.send(text)
            print(f"✅ Enviado: {text}")

asyncio.run(test_subtitle())
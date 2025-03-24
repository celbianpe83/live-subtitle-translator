import asyncio
import websockets
import threading

class WebSocketSubtitleReceiver:
    def __init__(self, on_texto, host="localhost", port=8765):
        self.on_texto = on_texto
        self.host = host
        self.port = port
        self.loop = None
        self.server = None
        self.thread = None

    async def handler(self, websocket):  # Eliminado el argumento 'path'
        print(f"Conexión desde: {websocket.remote_address}")
        print(f"Ruta solicitada: {websocket.request.path}")  # Accediendo a la ruta de la solicitud
        async for message in websocket:
            texto = message.strip()
            if texto:
                self.on_texto(texto)

    async def start_server(self):
        self.server = await websockets.serve(
            self.handler,  # Pasamos el 'handler' correctamente
            self.host,
            self.port
        )
        print(f"[✅ WS Server] Escuchando en ws://{self.host}:{self.port}")
        await self.server.wait_closed()

    def start(self):
        def run():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.start_server())

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def stop(self):
        if self.server and self.loop and self.loop.is_running():
            print("[🛑 WS Server] Deteniendo servidor WebSocket...")

            async def shutdown():
                self.server.close()
                await self.server.wait_closed()
                self.loop.stop()

            asyncio.run_coroutine_threadsafe(shutdown(), self.loop)
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2)
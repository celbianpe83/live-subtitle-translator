// background.js
let socket = null;
let maxReintentos = 10;
let intentos = 0;
let conectado = false;
const delayReconexion = 2000; // 2 segundos

const URL_WS = "ws://localhost:8765";
const ICON_OK = "icon_ok.png";
const ICON_ERROR = "icon_error.png";

function actualizarIcono(ok) {
  chrome.action.setIcon({ path: ok ? ICON_OK : ICON_ERROR });
}

function conectarWebSocket() {
  if (intentos >= maxReintentos) {
    console.warn("[WS] Demasiados intentos fallidos. Deteniendo reconexión.");
    actualizarIcono(false);
    return;
  }

  socket = new WebSocket(URL_WS);
  
  socket.onopen = () => {
    console.log("[WS] ✅ Conectado exitosamente");
    conectado = true;
    intentos = 0;
    actualizarIcono(true);
  };

  socket.onerror = (err) => {
    console.warn("[WS] ❌ Error en conexión:", err.message);
  };

  socket.onclose = () => {
    console.warn("[WS] 🔌 Conexión cerrada");
    conectado = false;
    intentos++;
    actualizarIcono(false);

    setTimeout(() => conectarWebSocket(), delayReconexion);
  };
}

// Permite reintentar manualmente al hacer clic en la extensión
chrome.action.onClicked.addListener(() => {
  if (!conectado) {
    console.log("[WS] 🔄 Reintentando conexión manual...");
    intentos = 0;
    conectarWebSocket();
  }
});

// Iniciar al cargar
conectarWebSocket();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "ping") {
    sendResponse({ ok: true });
  }

  if (message.type === "subtitle" && socket && socket.readyState === WebSocket.OPEN) {
    socket.send(message.texto);
  }
});

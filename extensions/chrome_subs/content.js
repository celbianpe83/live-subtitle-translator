console.log("[🔁 Extensión iniciada: Detectando subtítulos...]");

let selectorSubtitulo = "span";
const hostname = window.location.hostname;

if (hostname.includes("primevideo.com")) {
  selectorSubtitulo = ".atvwebplayersdk-captions-text";
} else if (hostname.includes("netflix.com")) {
  selectorSubtitulo = ".player-timedtext-text-container span";
} else if (hostname.includes("youtube.com")) {
  selectorSubtitulo = ".ytp-caption-segment";
} else if (hostname.includes("crunchyroll.com")) {
  selectorSubtitulo = ".caption-visual-line";
} else {
  console.warn("[⚠️ Extensión]: Plataforma no reconocida, usando <span>");
}

let ultimoTexto = "";
let esconderOriginal = true;

// ✅ SOLO INICIA OBSERVER DESPUÉS DE CARGAR CONFIG
chrome.storage.sync.get(["mostrarSubtitulos"], (result) => {
  esconderOriginal = result.mostrarSubtitulos === false;
  console.log("[⚙️ Config] Mostrar subtítulos originales:", !esconderOriginal);

  iniciarObservadorCuandoListo();  // 🔁 SOLO aquí se inicia el observer
});

function iniciarObservadorCuandoListo() {
  const target = document.querySelector(selectorSubtitulo);

  if (!target) {
    console.warn("⏳ Aguardando subtítulos...");
    setTimeout(iniciarObservadorCuandoListo, 1000);
    return;
  }

  console.log("👀 Observando subtítulos en:", selectorSubtitulo);

  const observer = new MutationObserver(() => {
    const nodos = document.querySelectorAll(selectorSubtitulo);
    const texto = Array.from(nodos).map(n => n.innerText.trim()).join(" ").trim();

    if (texto && texto !== ultimoTexto) {
      ultimoTexto = texto;

      chrome.runtime.sendMessage({ type: "ping" }, (response) => {
        if (chrome.runtime.lastError) {
          console.warn("⚠️ Background no disponible:", chrome.runtime.lastError.message);
          return;
        }

        chrome.runtime.sendMessage({ type: "subtitle", texto });
      });

      // ✅ Aplica estilo solo si debe ocultar
      if (esconderOriginal) {
        nodos.forEach(n => {
          n.style.visibility = "hidden";
        });
      }
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
  });
}
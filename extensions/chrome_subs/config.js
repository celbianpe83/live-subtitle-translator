const checkbox = document.getElementById("mostrarSubtitulos");

chrome.storage.sync.get(["mostrarSubtitulos"], (data) => {
  checkbox.checked = data.mostrarSubtitulos ?? false;
});

checkbox.addEventListener("change", () => {
  chrome.storage.sync.set({ mostrarSubtitulos: checkbox.checked });
});
import tkinter as tk
from tkinter import ttk, StringVar
from infrastructure.capturers.ocr_capturer import OCRCapturer
from infrastructure.capturers.browser_capturer import BrowserSubtitleCapturer

class SubtitleApp:
    def __init__(self, root, on_play, on_stop, use_browser=False, region=None):
        self.root = root
        self.on_play = on_play
        self.on_stop = on_stop
        self.use_browser = use_browser
        self.region = region

        self.filme_var = StringVar()
        self.input_var = StringVar()
        self.traducido_var = StringVar()

        self.controls_frame = tk.Frame(root, bg="black")
        self.controls_frame.pack(side="top", fill="x", padx=20, pady=10)

        self.combo = ttk.Combobox(
            self.controls_frame, textvariable=self.filme_var, state="readonly")
        self.combo.pack(side="left", padx=5)

        self.entry = tk.Entry(
            self.controls_frame, textvariable=self.input_var, state="disabled",
            bg="gray20", fg="white", insertbackground="white"
        )
        self.entry.pack(side="left", padx=5)

        self.play_button = tk.Button(
            self.controls_frame, text="▶️", command=self.play_clicked,
            bg="gray25", fg="white", state="disabled"
        )
        self.play_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(
            self.controls_frame, text="⏹️", command=self.stop_clicked,
            bg="gray25", fg="white"
        )
        self.stop_button.pack_forget()  # oculto al iniciar

        self.opacity_slider = tk.Scale(
            self.controls_frame, from_=30, to=100, orient="horizontal",
            command=self.update_opacity, bg="black", fg="white",
            showvalue=False, width=10, sliderlength=20
        )
        self.opacity_slider.set(75)
        self.opacity_slider.pack_forget()  # oculto al iniciar

        self.set_opacity_button = tk.Button(
            self.controls_frame, text="✔️", command=self.confirm_opacity,
            bg="gray25", fg="white"
        )
        self.set_opacity_button.pack_forget()

        self.label = tk.Label(
            root,
            textvariable=self.traducido_var,
            font=("Helvetica", 24, "bold"),
            fg="cyan",
            bg="black",
            justify="center",
            wraplength=self.root.winfo_width() - 80
        )
        self.label.pack(fill="both", expand=True, padx=40, pady=20)

        self.filme_var.trace_add("write", self.filme_selected)
        self.input_var.trace_add("write", self.filme_selected)

        self.root.bind("<Configure>", self.ajustar_wrap)

        # Inicializar capturer conforme a fonte
        if self.use_browser:
            self.capturer = BrowserSubtitleCapturer()
        else:
            self.capturer = OCRCapturer(self.region)

    def ajustar_wrap(self, event=None):
        if event:
            self.label.config(wraplength=event.width - 80)

    def update_opacity(self, val):
        self.root.attributes("-alpha", int(val)/100)

    def confirm_opacity(self):
        self.update_opacity(self.opacity_slider.get())
        self.opacity_slider.pack_forget()
        self.set_opacity_button.pack_forget()

    def play_clicked(self):
        self.combo.pack_forget()
        self.entry.pack_forget()
        self.play_button.pack_forget()

        self.stop_button.pack(side="left", padx=5)
        self.opacity_slider.pack(side="left", padx=5)
        self.set_opacity_button.pack(side="left", padx=5)

        filme = self.filme_var.get()
        if filme == "Nuevo filme":
            filme = self.input_var.get()

        # Iniciar captura com callback
        self.capturer.start(self._on_subtitle)
        self.on_play(filme)

    def stop_clicked(self):
        self.show_guardando()
        self.root.after(1000, lambda: (self.on_stop(), self.root.quit()))

    def set_options(self, filmes):
        self.combo["values"] = ["Selecciona filme"] + filmes + ["Nuevo filme"]
        self.combo.current(0)

    def filme_selected(self, *_):
        if self.filme_var.get() == "Nuevo filme":
            self.entry.config(state="normal")
        else:
            self.entry.config(state="disabled")

        if self.filme_var.get() != "Selecciona filme" and (
            self.filme_var.get() != "Nuevo filme" or self.input_var.get().strip()
        ):
            self.play_button.config(state="normal")
        else:
            self.play_button.config(state="disabled")

    def set_traduccion(self, texto, color="cyan"):
        self.label.config(fg=color)
        self.traducido_var.set(texto)

    def show_guardando(self):
        self.set_traduccion(
            "💾 Guardando nuevas traducciones...", color="yellow")

    def _on_subtitle(self, texto):
        # Método que recebe os subtítulos do capturer
        self.set_traduccion(texto)

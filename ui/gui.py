import tkinter as tk
from tkinter import ttk, StringVar

class TranslationUI:
    def __init__(self, root, iniciar_callback, detener_callback, filmes):
        self.root = root
        self.root.title("Overlay de subtítulos")
        self.root.geometry("850x160+180+540")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg="black")

        try:
            self.root.wm_attributes("-type", "dock")
        except tk.TclError:
            pass

        self.traducido_var = StringVar()
        self.opacidad_var = tk.DoubleVar(value=0.75)
        self.filme_actual = ""
        self.iniciar_callback = iniciar_callback
        self.detener_callback = detener_callback

        self._crear_widgets(filmes)

    def _crear_widgets(self, filmes):
        self.frame_top = tk.Frame(self.root, bg="black")
        self.frame_top.pack(pady=5)

        tk.Label(self.frame_top, text="Selecciona filme:", fg="white", bg="black").grid(row=0, column=0, padx=5)

        self.combo = ttk.Combobox(self.frame_top, state="readonly")
        self.combo.grid(row=0, column=1, padx=5)
        self.combo["values"] = ["Selecciona filme"] + filmes + ["Nuevo filme"]
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.on_combo_change)

        self.entry = tk.Entry(self.frame_top, state="disabled")
        self.entry.grid(row=0, column=2, padx=5)
        self.entry.bind("<KeyRelease>", self.on_entry_change)

        self.btn_play = tk.Button(self.frame_top, text="Play", state="disabled", command=self.iniciar_traduccion)
        self.btn_play.grid(row=0, column=3, padx=5)

        self.btn_stop = tk.Button(self.frame_top, text="Stop", state="disabled", command=self.detener_traduccion)
        self.btn_stop.grid(row=0, column=4, padx=5)

        tk.Scale(self.frame_top, from_=0.3, to=1.0, resolution=0.05, orient="horizontal", variable=self.opacidad_var,
                 label="Opacidad", bg="black", fg="white",
                 command=self._actualizar_opacidad).grid(row=0, column=5, padx=10)

        self.etiqueta = tk.Label(
            self.root, textvariable=self.traducido_var,
            font=("Helvetica", 24, "bold"), fg="cyan", bg="black", justify="center"
        )
        self.etiqueta.pack(fill="both", expand=True, padx=40, pady=10)
        self.root.bind("<Configure>", self._ajustar_wrap)

    def _ajustar_wrap(self, event):
        self.etiqueta.config(wraplength=event.width - 80)

    def _actualizar_opacidad(self, val):
        self.root.wm_attributes("-alpha", float(val))

    def on_combo_change(self, event):
        seleccion = self.combo.get()
        if seleccion == "Nuevo filme":
            self.entry.config(state="normal")
            self.btn_play.config(state="disabled")
        elif seleccion != "Selecciona filme":
            self.entry.config(state="disabled")
            self.entry.delete(0, tk.END)
            self.filme_actual = seleccion
            self.btn_play.config(state="normal")
        else:
            self.entry.config(state="disabled")
            self.btn_play.config(state="disabled")

    def on_entry_change(self, *args):
        if self.entry.get().strip():
            self.btn_play.config(state="normal")
        else:
            self.btn_play.config(state="disabled")

    def iniciar_traduccion(self):
        if self.combo.get() == "Nuevo filme":
            self.filme_actual = self.entry.get().strip()
        self.combo.grid_remove()
        self.entry.grid_remove()
        self.btn_play.grid_remove()
        self.btn_stop.config(state="normal")
        self.iniciar_callback(self.filme_actual)

    def detener_traduccion(self):
        self.combo.grid()
        self.entry.grid()
        self.btn_play.grid()
        self.combo.set("Selecciona filme")
        self.btn_play.config(state="disabled")
        self.btn_stop.config(state="disabled")
        self.entry.config(state="disabled")
        self.detener_callback()

    def set_texto(self, texto):
        self.traducido_var.set(texto)

    def get_film(self):
        return self.filme_actual

    def get_etiqueta(self):
        return self.etiqueta

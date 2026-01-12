import tkinter as tk
from tkinter import messagebox, ttk

from models.inscripcion import Inscripcion
from strategy.validador_datos_completos import ValidadorDatosCompletos
from strategy.validador_cupos import ValidadorCupos
from servicios.inscripcion_service import InscripcionService
from repository.inscripcion_repository import InscripcionRepository


class PostulanteApp:
    def __init__(self, root, postulante):
        self.root = root
        self.postulante = postulante

        self.root.title("Inscripción del Postulante")
        self.root.geometry("500x400")

        # Servicios y validadores
        self.validador_datos = ValidadorDatosCompletos()
        self.validador_cupos = ValidadorCupos()
        self.inscripcion_service = InscripcionService(
            InscripcionRepository()
        )

        # Ofertas (por ahora en memoria)
        self.ofertas = [
            # luego pueden venir de BD o repo
        ]

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self.root,
            text=f"Bienvenido {self.postulante.nombre}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        ttk.Label(self.root, text="Seleccione una carrera:").pack()

        self.combo_ofertas = ttk.Combobox(
            self.root,
            values=[o.nombre for o in self.ofertas],
            state="readonly"
        )
        self.combo_ofertas.pack(pady=10)

        ttk.Button(
            self.root,
            text="Inscribirse",
            command=self.inscribirse
        ).pack(pady=15)

    def inscribirse(self):
        nombre_oferta = self.combo_ofertas.get()

        if not nombre_oferta:
            messagebox.showerror("Error", "Debe seleccionar una carrera")
            return

        oferta = next(
            (o for o in self.ofertas if o.nombre == nombre_oferta),
            None
        )

        inscripcion = Inscripcion(
            self.postulante,
            oferta,
            self.validador_datos,
            self.validador_cupos
        )

        try:
            self.inscripcion_service.registrar(inscripcion)
            messagebox.showinfo(
                "Éxito",
                f"Inscripción realizada\nEstado: {inscripcion.estado}"
            )

        except ValueError as e:
            messagebox.showerror("Error", str(e))

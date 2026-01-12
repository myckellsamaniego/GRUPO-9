import tkinter as tk
from tkinter import messagebox, ttk

from models.inscripcion import Inscripcion
from strategy.validador_datos_completos import ValidadorDatosCompletos
from strategy.validador_cupos import ValidadorCupos
from servicios.inscripcion_service import InscripcionService
from repository.inscripcion_repository import InscripcionRepository
from models.oferta_academica import OfertaAcademica


class PostulanteApp:
    """
    GUI del Postulante
    """

    def __init__(self, root, postulante):
        self.root = root
        self.postulante = postulante

        self.root.title("Panel del Postulante - Sistema de Admisión")
        self.root.geometry("600x400")

        #Servicios y validadores
        self.validador_datos = ValidadorDatosCompletos()
        self.validador_cupos = ValidadorCupos()
        self.inscripcion_service = InscripcionService(
            InscripcionRepository()
        )

        # Ofertas 
        self.ofertas = [
            OfertaAcademica("MED-001", "Medicina", 10),
            OfertaAcademica("ING-002", "Ingeniería en Sistemas", 20),
            OfertaAcademica("DER-003", "Derecho", 15),
        ]

        self.crear_interfaz()
        self.mostrar_estado_actual()

    # INTERFAZ 

    def crear_interfaz(self):
        ttk.Label(
            self.root,
            text=f"Bienvenido {self.postulante.nombre}",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        # Estado de inscripción
        self.estado_label = ttk.Label(
            self.root,
            text="Estado de inscripción: No registrado",
            font=("Arial", 11)
        )
        self.estado_label.pack(pady=5)

        # Selección de carrera
        ttk.Label(self.root, text="Seleccione una carrera:").pack(pady=5)

        self.combo_ofertas = ttk.Combobox(
            self.root,
            values=[o.nombre for o in self.ofertas],
            state="readonly",
            width=35
        )
        self.combo_ofertas.pack(pady=5)

        # Botones
        botones_frame = ttk.Frame(self.root)
        botones_frame.pack(pady=20)

        ttk.Button(
            botones_frame,
            text="Inscribirse",
            command=self.inscribirse
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            botones_frame,
            text="Cerrar Sesión",
            command=self.cerrar_sesion
        ).grid(row=0, column=1, padx=10)

    # LÓGICA

    def mostrar_estado_actual(self):
        """
        Verifica si el postulante ya tiene una inscripción.
        """
        inscripcion = self.inscripcion_service.buscar_por_cedula(
            self.postulante.datos_personales.cedula
        )

        if inscripcion:
            self.estado_label.config(
                text=f"Estado de inscripción: {inscripcion['estado_inscripcion']}"
            )
            self.combo_ofertas.config(state="disabled")
        else:
            self.estado_label.config(
                text="Estado de inscripción: No registrado"
            )

    def inscribirse(self):
        nombre_oferta = self.combo_ofertas.get()

        if not nombre_oferta:
            messagebox.showerror("Error", "Debe seleccionar una carrera")
            return

        oferta = next(
            (o for o in self.ofertas if o.nombre == nombre_oferta),
            None
        )

        if not oferta:
            messagebox.showerror("Error", "Oferta no válida")
            return

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

            self.mostrar_estado_actual()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cerrar_sesion(self):
        self.root.destroy()

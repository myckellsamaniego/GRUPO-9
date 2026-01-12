import tkinter as tk
from tkinter import ttk, messagebox

from servicios.inscripcion_service import InscripcionService
from repository.inscripcion_repository import InscripcionRepository


class AdminApp:
    def __init__(self, root, administrador):
        self.root = root
        self.administrador = administrador

        self.root.title("Panel Administrador - Sistema de Admisión")
        self.root.geometry("700x400")

        # Servicio
        self.inscripcion_service = InscripcionService(
            InscripcionRepository()
        )

        self.crear_interfaz()
        self.cargar_inscripciones()

    def crear_interfaz(self):
        ttk.Label(
            self.root,
            text=f"Administrador: {self.administrador.nombre}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Tabla
        columnas = ("cedula", "postulante", "carrera", "estado")

        self.tabla = ttk.Treeview(
            self.root,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading("cedula", text="Cédula")
        self.tabla.heading("postulante", text="Postulante")
        self.tabla.heading("carrera", text="Carrera")
        self.tabla.heading("estado", text="Estado")

        self.tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        ttk.Button(
            self.root,
            text="Actualizar",
            command=self.cargar_inscripciones
        ).pack(pady=10)

    def cargar_inscripciones(self):
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = self.inscripcion_service.listar()

        if not registros:
            messagebox.showinfo("Información", "No hay inscripciones registradas")
            return

        for ins in registros:
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ins["cedula_postulante"],
                    ins["nombre_postulante"],
                    ins["carrera_seleccionada"],
                    ins["estado_inscripcion"]
                )
            )

import tkinter as tk
from tkinter import ttk, messagebox

from repository.inscripcion_repository_json import InscripcionRepositoryJSON
from servicios.inscripcion_service import InscripcionService


class AdminApp:
    """
    GUI del Administrador del Sistema de Admisión
    """

    def __init__(self, root, administrador):
        self.root = root
        self.administrador = administrador

        self.root.title("Panel Administrador - Sistema de Admisión")
        self.root.geometry("800x450")

        # USAR IMPLEMENTACIÓN CONCRETA
        self.inscripcion_service = InscripcionService(
            InscripcionRepositoryJSON()
        )

        self.crear_interfaz()
        self.cargar_inscripciones()

    # INTERFAZ 

    def crear_interfaz(self):
        ttk.Label(
            self.root,
            text=f"Administrador: {self.administrador.nombre}",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        # Botones superiores
        botones_frame = ttk.Frame(self.root)
        botones_frame.pack(pady=5)

        ttk.Button(
            botones_frame,
            text="Actualizar Inscripciones",
            command=self.cargar_inscripciones
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            botones_frame,
            text="Gestionar Periodos",
            command=self.gestionar_periodos
        ).grid(row=0, column=1, padx=10)

        ttk.Button(
            botones_frame,
            text="Cerrar Sesión",
            command=self.cerrar_sesion
        ).grid(row=0, column=2, padx=10)

        # Tabla de inscripciones
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

    #  FUNCIONALIDAD 

    def cargar_inscripciones(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = self.inscripcion_service.listar()

        if not registros:
            return  # No molestar al admin

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

    def gestionar_periodos(self):
        """
        Placeholder correcto para defensa académica.
        """
        messagebox.showinfo(
            "Gestión de Periodos",
            "Aquí el administrador podrá activar o cerrar periodos de admisión."
        )

    def cerrar_sesion(self):
        self.root.destroy()

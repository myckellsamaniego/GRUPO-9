"""
GUI del Postulante - Sistema de Admisión
"""
import tkinter as tk
from tkinter import messagebox, ttk

from models.inscripcion import Inscripcion
from servicios.inscripcion_service import InscripcionService
from repository.inscripcion_repository import InscripcionRepositoryJSON
from models.oferta_academica import OfertaAcademica
from excepciones.errores_inscripcion import InscripcionDuplicadaError, CuposAgotadosError


class PostulanteApp:
    """Interfaz gráfica para el postulante"""

    def __init__(self, root, postulante):
        self.root = root
        self.postulante = postulante

        self.root.title("Panel del Postulante - Sistema de Admisión ULEAM")
        self.root.geometry("700x550")

        # Servicio
        self.inscripcion_service = InscripcionService(
            InscripcionRepositoryJSON()
        )

        # Ofertas académicas disponibles
        self.ofertas = [
            OfertaAcademica("MED-001", "Medicina", 50),
            OfertaAcademica("ING-002", "Ingeniería en Sistemas", 50),
            OfertaAcademica("DER-003", "Derecho", 30),
            OfertaAcademica("ARQ-004", "Arquitectura", 15),
            OfertaAcademica("ENF-005", "Enfermería", 40),
            OfertaAcademica("ADM-006", "Administración de Empresas", 35)
        ]

        self.crear_interfaz()
        self.mostrar_estado_actual()

    def crear_interfaz(self):
        # Header con bienvenida
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=10, padx=10)

        nombre_completo = (
            f"{self.postulante.datos_personales.nombre} "
            f"{self.postulante.datos_personales.apellidos}"
        )
        
        ttk.Label(
            header_frame,
            text=f" Bienvenido/a {nombre_completo}",
            font=("Arial", 16, "bold")
        ).pack()

        ttk.Label(
            header_frame,
            text=f"Cédula: {self.postulante.datos_personales.cedula}",
            font=("Arial", 10)
        ).pack()

        # Estado de inscripción
        status_frame = ttk.LabelFrame(
            self.root, 
            text="Estado de Inscripción", 
            padding="10"
        )
        status_frame.pack(fill=tk.X, padx=10, pady=10)

        self.estado_label = ttk.Label(
            status_frame,
            text="Estado: Verificando...",
            font=("Arial", 12, "bold")
        )
        self.estado_label.pack()

        self.carrera_actual_label = ttk.Label(
            status_frame,
            text="",
            font=("Arial", 10)
        )
        self.carrera_actual_label.pack()

        # Frame de nueva inscripción
        self.inscripcion_frame = ttk.LabelFrame(
            self.root, 
            text="Realizar Nueva Inscripción", 
            padding="15"
        )
        self.inscripcion_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Instrucciones
        ttk.Label(
            self.inscripcion_frame,
            text="Complete los siguientes datos para inscribirse:",
            font=("Arial", 10)
        ).pack(pady=5)

        # Selección de carrera
        ttk.Label(
            self.inscripcion_frame, 
            text="Seleccione una carrera:"
        ).pack(pady=5)

        self.combo_ofertas = ttk.Combobox(
            self.inscripcion_frame,
            values=[f"{o.nombre} - Cupos: {o.cupos}" for o in self.ofertas],
            state="readonly",
            width=45,
            font=("Arial", 10)
        )
        self.combo_ofertas.pack(pady=5)

        # Contraseña para inscripción
        ttk.Label(
            self.inscripcion_frame, 
            text="Contraseña de inscripción:"
        ).pack(pady=5)
        
        self.password_entry = ttk.Entry(
            self.inscripcion_frame, 
            show="*", 
            width=47,
            font=("Arial", 10)
        )
        self.password_entry.pack(pady=5)

        ttk.Label(
            self.inscripcion_frame,
            text="(Mínimo 6 caracteres)",
            font=("Arial", 8),
            foreground="gray"
        ).pack()

        # Botones principales
        botones_frame = ttk.Frame(self.root)
        botones_frame.pack(pady=15)

        self.btn_inscribir = ttk.Button(
            botones_frame,
            text=" Inscribirse",
            command=self.inscribirse,
            width=20
        )
        self.btn_inscribir.grid(row=0, column=0, padx=5)

        ttk.Button(
            botones_frame,
            text=" Actualizar Estado",
            command=self.mostrar_estado_actual,
            width=20
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            botones_frame,
            text=" Cerrar Sesión",
            command=self.cerrar_sesion,
            width=20
        ).grid(row=0, column=2, padx=5)

    def mostrar_estado_actual(self):
        """Verifica y muestra el estado de inscripción del postulante"""
        cedula = self.postulante.datos_personales.cedula
        inscripcion = self.inscripcion_service.buscar_por_cedula(cedula)

        if inscripcion:
            # Ya tiene inscripción
            estado = inscripcion['estado_inscripcion']
            carrera = inscripcion['carrera_seleccionada']
            
            # Configurar color según estado
            if estado == "APROBADA":
                color = "green"
                icono = ""
            elif estado == "RECHAZADA":
                color = "red"
                icono = ""
            else:
                color = "orange"
                icono = ""
            
            self.estado_label.config(
                text=f"{icono} Estado: {estado}",
                foreground=color
            )
            self.carrera_actual_label.config(
                text=f"Carrera: {carrera}"
            )
            
            # Deshabilitar formulario de inscripción
            self.combo_ofertas.config(state="disabled")
            self.password_entry.config(state="disabled")
            self.btn_inscribir.config(state="disabled")
            
            # Cambiar título del frame
            self.inscripcion_frame.config(text="Ya tiene una inscripción registrada")
            
        else:
            # No tiene inscripción
            self.estado_label.config(
                text=" Sin inscripción registrada",
                foreground="blue"
            )
            self.carrera_actual_label.config(text="")
            
            # Habilitar formulario
            self.combo_ofertas.config(state="readonly")
            self.password_entry.config(state="normal")
            self.btn_inscribir.config(state="normal")
            
            self.inscripcion_frame.config(text="Realizar Nueva Inscripción")

    def inscribirse(self):
        """Procesa la inscripción del postulante"""
        try:
            seleccion = self.combo_ofertas.get()

            if not seleccion:
                raise ValueError("Debe seleccionar una carrera")

            password = self.password_entry.get()
            
            if not password:
                raise ValueError("Debe ingresar una contraseña para la inscripción")
            
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")

            # Extraer nombre de la oferta
            nombre_oferta = seleccion.split(" - Cupos:")[0]

            # Buscar oferta
            oferta = next(
                (o for o in self.ofertas if o.nombre == nombre_oferta),
                None
            )

            if not oferta:
                raise ValueError("Oferta no válida")

            # Crear inscripción
            inscripcion = Inscripcion(self.postulante, oferta, password)

            # Registrar
            self.inscripcion_service.registrar(inscripcion)

            messagebox.showinfo(
                " Inscripción Exitosa",
                f"Su inscripción ha sido registrada exitosamente.\n\n"
                f"Carrera: {oferta.nombre}\n"
                f"Estado: {inscripcion.estado}\n\n"
                f"Recibirá notificación cuando sea aprobada."
            )

            # Actualizar estado
            self.mostrar_estado_actual()
            
            # Limpiar campos
            self.password_entry.delete(0, tk.END)

        except InscripcionDuplicadaError as e:
            messagebox.showerror(" Error", str(e))
        except CuposAgotadosError as e:
            messagebox.showerror(" Sin Cupos", str(e))
        except ValueError as e:
            messagebox.showerror(" Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror(" Error Inesperado", str(e))

    def cerrar_sesion(self):
        """Cierra la sesión del postulante"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar sesión?"
        )
        if respuesta:
            self.root.destroy()
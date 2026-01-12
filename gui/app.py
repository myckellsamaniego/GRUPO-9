import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk # Asegúrate de instalar pillow: pip install Pillow

from models.datos_personales import DatosPersonales
from models.oferta_academica import OfertaAcademica
from models.inscripcion import Inscripcion
from models.postulante import Postulante
from repository.inscripcion_repository import InscripcionRepositoryJSON
from servicios.inscripcion_service import InscripcionService
from strategy.validador_datos_completos import ValidadorDatosCompletos
from strategy.validador_cupos import ValidadorCupos
from factory.fabrica_usuarios import FabricaUsuarios
from excepciones.errores_inscripcion import InscripcionDuplicadaError, CuposAgotadosError

class AdmisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Admisión ULEAM 2026")
        self.root.geometry("800x650") # Tamaño de la ventana

        self.service = InscripcionService(InscripcionRepositoryJSON())
        self.fabrica_usuarios = FabricaUsuarios()
        self.validador_datos = ValidadorDatosCompletos()
        self.validador_cupos = ValidadorCupos()

        # Ofertas académicas de la ULEAM
        self.ofertas_academicas = [
            OfertaAcademica("MED-001", "Medicina (Manta)", 2),
            OfertaAcademica("ING-002", "Ingeniería en Sistemas (Manta)", 50),
            OfertaAcademica("DER-003", "Derecho (Chone)", 30),
            OfertaAcademica("ARQ-004", "Arquitectura (Manta)", 15)
        ]

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cargar y mostrar logo de la ULEAM
        try:
            img = Image.open("uleam_logo.png")
            img = img.resize((150, 150), Image.LANCZOS) # Redimensionar
            self.photo = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(main_frame, image=self.photo)
            logo_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showwarning("Error de Imagen", "No se encontró 'uleam_logo.png'. Asegúrate de que está en la misma carpeta que main.py.")
            logo_label = ttk.Label(main_frame, text="LOGO ULEAM")
            logo_label.pack(pady=10)


        ttk.Label(main_frame, text="REGISTRO DE POSTULANTE", font=("Arial", 16, "bold")).pack(pady=5)

        # Frame para los campos de entrada
        form_frame = ttk.Frame(main_frame, padding="10")
        form_frame.pack(fill=tk.X, pady=10)

        # Campos de entrada
        labels = ["Cédula:", "Nombre:", "Apellidos:", "Celular:", "Correo:", "Dirección:", "Etnia:", "¿Discapacidad?"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            if text == "¿Discapacidad?":
                self.entries[text] = ttk.Checkbutton(form_frame)
                self.entries[text].grid(row=i, column=1, sticky=tk.W, pady=2, padx=5)
            else:
                entry = ttk.Entry(form_frame, width=40)
                entry.grid(row=i, column=1, sticky=tk.EW, pady=2, padx=5)
                self.entries[text] = entry
        
        # Selección de Carrera
        ttk.Label(form_frame, text="Carrera:").grid(row=len(labels), column=0, sticky=tk.W, pady=5, padx=5)
        self.carrera_var = tk.StringVar()
        carreras_nombres = [oferta.nombre for oferta in self.ofertas_academicas]
        self.carrera_menu = ttk.Combobox(form_frame, textvariable=self.carrera_var, values=carreras_nombres, state="readonly", width=38)
        self.carrera_menu.grid(row=len(labels), column=1, sticky=tk.EW, pady=5, padx=5)
        self.carrera_menu.set("Seleccione una carrera")

        # Botón de Inscripción
        ttk.Button(main_frame, text="Realizar Inscripción", command=self.inscribir_postulante).pack(pady=20)

        # Área para mostrar inscripciones (opcional, para depuración)
        ttk.Label(main_frame, text="Inscripciones Registradas:", font=("Arial", 12, "bold")).pack(pady=5)
        self.inscripciones_text = tk.Text(main_frame, height=8, width=70, state=tk.DISABLED)
        self.inscripciones_text.pack()
        self.mostrar_inscripciones_existentes()

    def mostrar_inscripciones_existentes(self):
        self.inscripciones_text.config(state=tk.NORMAL)
        self.inscripciones_text.delete(1.0, tk.END)
        registros = self.service.repositorio.listar()
        if not registros:
            self.inscripciones_text.insert(tk.END, "No hay inscripciones registradas.\n")
        else:
            for reg in registros:
                self.inscripciones_text.insert(tk.END, f"Cédula: {reg['cedula_postulante']}, Carrera: {reg['carrera_seleccionada']}, Estado: {reg['estado_inscripcion']}\n")
        self.inscripciones_text.config(state=tk.DISABLED)


    def inscribir_postulante(self):
        try:
            cedula = self.entries["Cédula:"].get()
            nombre = self.entries["Nombre:"].get()
            apellidos = self.entries["Apellidos:"].get()
            celular = self.entries["Celular:"].get()
            correo = self.entries["Correo:"].get()
            direccion = self.entries["Dirección:"].get()
            etnia = self.entries["Etnia:"].get()
            discapacidad_val = self.entries["¿Discapacidad?"].instate(['selected']) # Verifica el estado del Checkbutton
            carrera_nombre = self.carrera_var.get()

            # Validar campos obligatorios de la GUI
            if not all([cedula, nombre, apellidos, correo, carrera_nombre != "Seleccione una carrera"]):
                messagebox.showerror("Error de Datos", "Por favor, complete todos los campos obligatorios y seleccione una carrera.")
                return

            # Buscar la oferta académica seleccionada
            oferta_seleccionada = next((o for o in self.ofertas_academicas if o.nombre == carrera_nombre), None)
            if not oferta_seleccionada:
                messagebox.showerror("Error", "Carrera seleccionada no válida.")
                return

            # Crear objetos del modelo
            datos_personales = DatosPersonales(nombre, apellidos, cedula, direccion, celular, correo, etnia, discapacidad_val)
            postulante = self.fabrica_usuarios.crear_usuario("Postulante", datos_personales=datos_personales)
            
            inscripcion = Inscripcion(postulante, oferta_seleccionada, self.validador_datos, self.validador_cupos)

            # Registrar la inscripción a través del servicio
            self.service.registrar(inscripcion)
            
            messagebox.showinfo("Éxito", f"Inscripción de {nombre} {apellidos} a {carrera_nombre} realizada con éxito. Estado: {inscripcion.estado}")
            self.mostrar_inscripciones_existentes() # Actualizar la lista

        except InscripcionDuplicadaError as e:
            messagebox.showerror("Error de Inscripción", str(e))
        except CuposAgotadosError as e:
            messagebox.showerror("Error de Inscripción", str(e))
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
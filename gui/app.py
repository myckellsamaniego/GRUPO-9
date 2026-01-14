"""
GUI Principal - Sistema de Inscripción de Postulantes
"""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

from models.datos_personales import DatosPersonales
from models.oferta_academica import OfertaAcademica
from models.inscripcion import Inscripcion
from repository.inscripcion_repository import InscripcionRepositoryJSON
from servicios.inscripcion_service import InscripcionService
from factory.fabrica_usuarios import FabricaUsuarios
from excepciones.errores_inscripcion import (
    InscripcionDuplicadaError, 
    CuposAgotadosError,
    DatosIncompletosError
)


class AdmisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Admisión ULEAM 2026")
        self.root.geometry("800x700")

        # Servicios
        self.service = InscripcionService(InscripcionRepositoryJSON())
        self.fabrica_usuarios = FabricaUsuarios()

        # Ofertas académicas de la ULEAM
        self.ofertas_academicas = [
            OfertaAcademica("MED-001", "Medicina (Manta)", 50),
            OfertaAcademica("ING-002", "Ingeniería en Sistemas (Manta)", 50),
            OfertaAcademica("DER-003", "Derecho (Chone)", 30),
            OfertaAcademica("ARQ-004", "Arquitectura (Manta)", 15),
            OfertaAcademica("ENF-005", "Enfermería (Manta)", 40),
            OfertaAcademica("ADM-006", "Administración de Empresas (Manta)", 35)
        ]

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo
        try:
            img = Image.open("uleam_logo.png")
            img = img.resize((150, 150), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(main_frame, image=self.photo)
            logo_label.pack(pady=10)
        except FileNotFoundError:
            logo_label = ttk.Label(
                main_frame, 
                text="🎓 ULEAM", 
                font=("Arial", 20, "bold")
            )
            logo_label.pack(pady=10)

        ttk.Label(
            main_frame, 
            text="REGISTRO DE POSTULANTE", 
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        # Frame para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Postulante", padding="10")
        form_frame.pack(fill=tk.X, pady=10, padx=10)

        # Campos de entrada
        labels = [
            "Cédula:", 
            "Nombre:", 
            "Apellidos:", 
            "Celular:", 
            "Correo:", 
            "Dirección:", 
            "Etnia:", 
            "Contraseña:", 
            "¿Discapacidad?"
        ]
        
        self.entries = {}
        
        for i, text in enumerate(labels):
            ttk.Label(form_frame, text=text).grid(
                row=i, column=0, sticky=tk.W, pady=3, padx=5
            )
            
            if text == "¿Discapacidad?":
                var = tk.BooleanVar()
                check = ttk.Checkbutton(form_frame, variable=var)
                check.grid(row=i, column=1, sticky=tk.W, pady=3, padx=5)
                self.entries[text] = var
            else:
                show = "*" if text == "Contraseña:" else None
                entry = ttk.Entry(form_frame, width=40, show=show)
                entry.grid(row=i, column=1, sticky=tk.EW, pady=3, padx=5)
                self.entries[text] = entry

        # Selección de Carrera
        ttk.Label(form_frame, text="Carrera:").grid(
            row=len(labels), column=0, sticky=tk.W, pady=5, padx=5
        )
        
        self.carrera_var = tk.StringVar()
        carreras_display = [
            f"{oferta.nombre} (Cupos: {oferta.cupos})" 
            for oferta in self.ofertas_academicas
        ]
        self.carrera_menu = ttk.Combobox(
            form_frame, 
            textvariable=self.carrera_var, 
            values=carreras_display, 
            state="readonly", 
            width=38
        )
        self.carrera_menu.grid(row=len(labels), column=1, sticky=tk.EW, pady=5, padx=5)
        self.carrera_menu.set("Seleccione una carrera")

        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        ttk.Button(
            buttons_frame, 
            text="Realizar Inscripción", 
            command=self.inscribir_postulante
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons_frame, 
            text="Limpiar Formulario", 
            command=self.limpiar_formulario
        ).grid(row=0, column=1, padx=5)

        # Área de inscripciones
        ttk.Label(
            main_frame, 
            text="Inscripciones Registradas:", 
            font=("Arial", 12, "bold")
        ).pack(pady=5)
        
        # Frame con scrollbar para la lista
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.inscripciones_text = tk.Text(
            list_frame, 
            height=8, 
            width=70, 
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.inscripciones_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.inscripciones_text.yview)
        
        self.mostrar_inscripciones_existentes()

    def mostrar_inscripciones_existentes(self):
        """Muestra todas las inscripciones registradas"""
        self.inscripciones_text.config(state=tk.NORMAL)
        self.inscripciones_text.delete(1.0, tk.END)
        
        registros = self.service.listar()
        
        if not registros:
            self.inscripciones_text.insert(
                tk.END, 
                "No hay inscripciones registradas.\n"
            )
        else:
            for reg in registros:
                estado_color = ""
                if reg['estado_inscripcion'] == "APROBADA":
                    estado_color = ""
                elif reg['estado_inscripcion'] == "RECHAZADA":
                    estado_color = ""
                else:
                    estado_color = ""
                
                self.inscripciones_text.insert(
                    tk.END,
                    f"{estado_color} Cédula: {reg['cedula_postulante']} | "
                    f"{reg['nombre_postulante']} | "
                    f"Carrera: {reg['carrera_seleccionada']} | "
                    f"Estado: {reg['estado_inscripcion']}\n"
                )
        
        self.inscripciones_text.config(state=tk.DISABLED)

    def inscribir_postulante(self):
        """Procesa la inscripción de un nuevo postulante"""
        try:
            # Obtener datos del formulario
            cedula = self.entries["Cédula:"].get().strip()
            nombre = self.entries["Nombre:"].get().strip()
            apellidos = self.entries["Apellidos:"].get().strip()
            celular = self.entries["Celular:"].get().strip()
            correo = self.entries["Correo:"].get().strip()
            direccion = self.entries["Dirección:"].get().strip()
            etnia = self.entries["Etnia:"].get().strip()
            password = self.entries["Contraseña:"].get()
            discapacidad = self.entries["¿Discapacidad?"].get()
            carrera_seleccion = self.carrera_var.get()

            # Validar campos obligatorios
            if not all([cedula, nombre, apellidos, correo, password]):
                raise DatosIncompletosError(
                    "Complete todos los campos obligatorios:\n"
                    "• Cédula\n• Nombre\n• Apellidos\n• Correo\n• Contraseña"
                )

            if carrera_seleccion == "Seleccione una carrera":
                raise ValueError("Debe seleccionar una carrera")

            # Validar formato de contraseña
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")

            # Extraer nombre de carrera (quitar el texto de cupos)
            nombre_carrera = carrera_seleccion.split(" (Cupos:")[0]

            # Buscar oferta seleccionada
            oferta_seleccionada = next(
                (o for o in self.ofertas_academicas if o.nombre == nombre_carrera),
                None
            )
            
            if not oferta_seleccionada:
                raise ValueError("Carrera seleccionada no válida")

            # Crear datos personales
            datos_personales = DatosPersonales(
                nombre=nombre,
                apellidos=apellidos,
                cedula=cedula,
                direccion=direccion,
                celular=celular,
                correo=correo,
                etnia=etnia,
                discapacidad=discapacidad
            )

            # Crear postulante
            postulante = self.fabrica_usuarios.crear_usuario(
                "Postulante",
                correo=correo,
                password=password,
                datos_personales=datos_personales
            )

            # Crear inscripción
            inscripcion = Inscripcion(postulante, oferta_seleccionada, password)

            # Registrar a través del servicio
            self.service.registrar(inscripcion)

            messagebox.showinfo(
                " Inscripción Exitosa",
                f"Inscripción de {nombre} {apellidos} realizada con éxito.\n\n"
                f"Carrera: {oferta_seleccionada.nombre}\n"
                f"Estado: {inscripcion.estado}\n"
                f"Cupos restantes: {oferta_seleccionada.cupos}"
            )

            # Limpiar formulario
            self.limpiar_formulario()
            
            # Actualizar lista
            self.mostrar_inscripciones_existentes()
            
            # Actualizar cupos en el combobox
            self.actualizar_combo_carreras()

        except InscripcionDuplicadaError as e:
            messagebox.showerror(" Error de Inscripción", str(e))
        except CuposAgotadosError as e:
            messagebox.showerror(" Error de Cupos", str(e))
        except DatosIncompletosError as e:
            messagebox.showerror(" Datos Incompletos", str(e))
        except ValueError as e:
            messagebox.showerror(" Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror(" Error Inesperado", f"Ocurrió un error: {e}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        for key, entry in self.entries.items():
            if key == "¿Discapacidad?":
                entry.set(False)
            else:
                entry.delete(0, tk.END)
        self.carrera_menu.set("Seleccione una carrera")

    def actualizar_combo_carreras(self):
        """Actualiza el combobox de carreras con los cupos actuales"""
        carreras_display = [
            f"{oferta.nombre} (Cupos: {oferta.cupos})" 
            for oferta in self.ofertas_academicas
        ]
        self.carrera_menu['values'] = carreras_display


if __name__ == "__main__":
    root = tk.Tk()
    app = AdmisionApp(root)
    root.mainloop()
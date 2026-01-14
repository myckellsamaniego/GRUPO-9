"""
Ventana de Registro de Nuevos Postulantes
"""
import tkinter as tk
from tkinter import messagebox, ttk

from models.datos_personales import DatosPersonales
from factory.fabrica_usuarios import FabricaUsuarios


class RegistroApp:
    """Ventana de registro de nuevos postulantes"""

    def __init__(self, root, usuario_repo):
        self.root = root
        self.usuario_repo = usuario_repo
        self.fabrica = FabricaUsuarios()

        self.root.title("Crear Cuenta - Postulante")
        self.root.geometry("400x620")
        self.root.resizable(False, False)

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        ttk.Label(
            main_frame,
            text="Registro de Nuevo Postulante",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos Personales", padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.entries = {}

        campos = [
            ("Nombre*:", "Nombre"),
            ("Apellidos*:", "Apellidos"),
            ("Cédula*:", "Cedula"),
            ("Celular:", "Celular"),
            ("Dirección:", "Direccion"),
            ("Correo*:", "Correo"),
            ("Contraseña*:", "Password"),
            ("Confirmar Contraseña*:", "Confirmar")
        ]

        for i, (label, key) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=5
            )
            
            if "Contraseña" in label or "Confirmar" in label:
                entry = ttk.Entry(form_frame, show="*", width=25)
            else:
                entry = ttk.Entry(form_frame, width=25)
            
            entry.grid(row=i, column=1, sticky=tk.EW, pady=5, padx=5)
            self.entries[key] = entry

        # Configurar expansión de columnas
        form_frame.columnconfigure(1, weight=1)

        # Nota
        ttk.Label(
            main_frame,
            text="* Campos obligatorios",
            font=("Arial", 8),
            foreground="gray"
        ).pack(pady=5)

        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=15)

        ttk.Button(
            buttons_frame,
            text=" Crear Cuenta",
            command=self.crear_cuenta,
            width=18
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons_frame,
            text="✗ Cancelar",
            command=self.root.destroy,
            width=18
        ).grid(row=0, column=1, padx=5)

    def crear_cuenta(self):
        """Procesa la creación de una nueva cuenta"""
        try:
            # Obtener valores
            nombre = self.entries["Nombre"].get().strip()
            apellidos = self.entries["Apellidos"].get().strip()
            cedula = self.entries["Cedula"].get().strip()
            celular = self.entries["Celular"].get().strip()
            direccion = self.entries["Direccion"].get().strip()
            correo = self.entries["Correo"].get().strip()
            password = self.entries["Password"].get()
            confirmar = self.entries["Confirmar"].get()

            # Validaciones
            if not all([nombre, apellidos, cedula, correo, password]):
                raise ValueError(
                    "Complete todos los campos obligatorios:\n"
                    "• Nombre\n"
                    "• Apellidos\n"
                    "• Cédula\n"
                    "• Correo\n"
                    "• Contraseña"
                )

            if password != confirmar:
                raise ValueError("Las contraseñas no coinciden")

            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")

            # Validar formato de correo básico
            if "@" not in correo or "." not in correo:
                raise ValueError("Formato de correo inválido")

            # Validar que la cédula sea numérica
            if not cedula.isdigit():
                raise ValueError("La cédula debe contener solo números")

            if len(cedula) != 10:
                raise ValueError("La cédula debe tener 10 dígitos")

            # Verificar si el correo ya existe
            if self.usuario_repo.buscar_por_correo(correo):
                raise ValueError("Ya existe una cuenta con ese correo electrónico")

            # Crear datos personales
            datos = DatosPersonales(
                nombre=nombre,
                apellidos=apellidos,
                cedula=cedula,
                direccion=direccion,
                celular=celular,
                correo=correo,
                etnia="",
                discapacidad=False
            )

            # Crear postulante
            postulante = self.fabrica.crear_usuario(
                "Postulante",
                correo=correo,
                password=password,
                datos_personales=datos
            )

            # Guardar en el repositorio
            self.usuario_repo.agregar(postulante)

            messagebox.showinfo(
                " Cuenta Creada",
                f"Cuenta creada exitosamente para:\n\n"
                f"{nombre} {apellidos}\n"
                f"Correo: {correo}\n\n"
                f"Ya puede iniciar sesión con sus credenciales"
            )
            
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
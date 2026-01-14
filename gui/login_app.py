import tkinter as tk
from tkinter import messagebox

from gui.app_admin import AdminApp
from gui.app_postulante import PostulanteApp
from gui.registro import RegistroApp


class LoginApp:
    def __init__(self, root, auth_service):
        self.root = root
        self.auth_service = auth_service

        self.root.title("Inicio de Sesión")
        self.root.geometry("300x220")

        tk.Label(root, text="Correo").pack(pady=5)
        self.correo = tk.Entry(root)
        self.correo.pack()

        tk.Label(root, text="Contraseña").pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(
            root,
            text="Ingresar",
            command=self.login
        ).pack(pady=15)

        tk.Button(
            root,
            text="Crear cuenta",
            command=self.abrir_registro
        ).pack()

    def login(self):
        try:
            # Autenticación correcta (SERVICE)
            usuario = self.auth_service.login(
                self.correo.get(),
                self.password.get()
            )

            # Cerrar login
            self.root.destroy()

            root = tk.Tk()

            # Decisión REAL por rol
            if usuario.obtener_tipo() == "ADMIN":
                AdminApp(root, usuario)

            elif usuario.obtener_tipo() == "Postulante":
                PostulanteApp(root, usuario)

            else:
                raise ValueError("Rol de usuario no reconocido")

            root.mainloop()

        except ValueError as e:
            messagebox.showerror("Error de autenticación", str(e))

    def abrir_registro(self):
        ventana = tk.Toplevel(self.root)
        RegistroApp(
            ventana,
            self.auth_service._usuario_repository
        )
"""
Pantalla de Inicio de Sesión del Sistema
"""
import tkinter as tk
from tkinter import messagebox, ttk

from gui.app_admin import AdminApp
from gui.app_postulante import PostulanteApp
from gui.registro import RegistroApp


class LoginApp:
    """Pantalla de inicio de sesión del sistema"""

    def __init__(self, root, auth_service):
        self.root = root
        self.auth_service = auth_service

        self.root.title("Sistema de Admisión ULEAM - Login")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        # Centrar ventana
        self.centrar_ventana()

        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Título
        ttk.Label(
            main_frame,
            text=" Sistema de Admisión",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        ttk.Label(
            main_frame,
            text="ULEAM 2026",
            font=("Arial", 14)
        ).pack(pady=5)

        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        # Formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=15)

        # Correo
        ttk.Label(form_frame, text="Correo Electrónico:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=8
        )
        self.correo = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.correo.grid(row=0, column=1, pady=8, padx=10)
        self.correo.focus()

        # Contraseña
        ttk.Label(form_frame, text="Contraseña:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=8
        )
        self.password = ttk.Entry(form_frame, show="●", width=30, font=("Arial", 10))
        self.password.grid(row=1, column=1, pady=8, padx=10)

        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(
            buttons_frame,
            text=" Ingresar",
            command=self.login,
            width=18
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            buttons_frame,
            text=" Crear Cuenta",
            command=self.abrir_registro,
            width=18
        ).grid(row=0, column=1, padx=8)

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())

        # Separador
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Info de credenciales de admin
        info_frame = ttk.Frame(main_frame)
        info_frame.pack()

        ttk.Label(
            info_frame,
            text=" Credenciales de Administrador:",
            font=("Arial", 9, "bold"),
            foreground="#555"
        ).pack()

        ttk.Label(
            info_frame,
            text="admin@uleam.edu.ec / admin123",
            font=("Arial", 8),
            foreground="gray"
        ).pack()

    def login(self):
        """Procesa el inicio de sesión"""
        try:
            correo = self.correo.get().strip()
            password = self.password.get()

            if not correo or not password:
                raise ValueError("Complete todos los campos")

            # Validar formato de correo
            if "@" not in correo:
                raise ValueError("Ingrese un correo electrónico válido")

            # Autenticar usuario
            usuario = self.auth_service.login(correo, password)

            # Cerrar ventana de login
            self.root.destroy()

            # Abrir ventana según el tipo de usuario
            root = tk.Tk()

            if usuario.obtener_tipo() == "ADMIN":
                AdminApp(root, usuario)
            elif usuario.obtener_tipo() == "Postulante":
                PostulanteApp(root, usuario)
            else:
                raise ValueError("Tipo de usuario no reconocido")

            root.mainloop()

        except ValueError as e:
            messagebox.showerror(" Error de Autenticación", str(e))
            # Limpiar campo de contraseña
            self.password.delete(0, tk.END)
            self.password.focus()

    def abrir_registro(self):
        """Abre la ventana de registro"""
        ventana = tk.Toplevel(self.root)
        RegistroApp(ventana, self.auth_service._usuario_repository)
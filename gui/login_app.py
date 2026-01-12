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
            if usuario.obtener_tipo() == "Administrador":
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

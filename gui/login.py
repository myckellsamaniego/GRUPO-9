import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self, root, auth_service):
        self.root = root
        self.auth_service = auth_service
        self.root.title("Inicio de Sesión")

        tk.Label(root, text="Correo").pack()
        self.correo = tk.Entry(root)
        self.correo.pack()

        tk.Label(root, text="Contraseña").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Ingresar", command=self.login).pack(pady=10)

    def login(self):
        try:
            usuario = self.auth_service.login(
                self.correo.get(),
                self.password.get()
            )

            if usuario.obtener_tipo() == "ADMIN":
                messagebox.showinfo("Acceso", "Bienvenido Administrador")
                # abrir ventana admin

            elif usuario.obtener_tipo() == "POSTULANTE":
                messagebox.showinfo("Acceso", "Bienvenido Postulante")
                # abrir ventana postulante

        except ValueError as e:
            messagebox.showerror("Error", str(e))

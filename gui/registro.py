import tkinter as tk
from tkinter import messagebox

from models.datos_personales import DatosPersonales
from factory.fabrica_usuarios import FabricaUsuarios


class RegistroApp:
    def __init__(self, root, usuario_repo):
        self.root = root
        self.usuario_repo = usuario_repo
        self.fabrica = FabricaUsuarios()

        self.root.title("Crear Cuenta - Postulante")
        self.root.geometry("350x450")

        self.entries = {}

        campos = [
            "Nombre",
            "Apellidos",
            "Cédula",
            "Correo",
            "Contraseña"
        ]

        for campo in campos:
            tk.Label(root, text=campo).pack(pady=3)
            entry = tk.Entry(root, show="*" if campo == "Contraseña" else None)
            entry.pack()
            self.entries[campo] = entry

        tk.Button(
            root,
            text="Crear Cuenta",
            command=self.crear_cuenta
        ).pack(pady=15)

    def crear_cuenta(self):
        try:
            # Verificar si el correo ya existe
            if self.usuario_repo.buscar_por_correo(self.entries["Correo"].get()):
                raise ValueError("Ya existe una cuenta con ese correo")

            datos = DatosPersonales(
                nombre=self.entries["Nombre"].get(),
                apellidos=self.entries["Apellidos"].get(),
                cedula=self.entries["Cédula"].get(),
                direccion="",
                celular="",
                correo=self.entries["Correo"].get(),
                etnia="",
                discapacidad=False
            )

            postulante = self.fabrica.crear_usuario(
                "Postulante",
                datos_personales=datos,
                password=self.entries["Contraseña"].get()
            )

            self.usuario_repo.agregar(postulante)

            messagebox.showinfo("Éxito", "Cuenta creada correctamente")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

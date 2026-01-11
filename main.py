import tkinter as tk

from gui.login import LoginApp
from repository.usuario_repository import UsuarioRepository
from servicios.autenticacion_servicios import AutenticacionServicios
from models.administrador import Administrador


def main():
    # ===== Repositorio de usuarios =====
    usuario_repo = UsuarioRepository()

    # ===== Administrador inicial del sistema =====
    usuario_repo.agregar(
        Administrador(
            identificacion="ADM001",
            nombre="Admin Principal",
            correo="admin@uleam.edu.ec",
            password="admin123"
        )
    )

    # ===== Servicio de autenticación =====
    auth_service = AutenticacionServicios(usuario_repo)

    # ===== Lanzar Login =====
    root = tk.Tk()
    LoginApp(root, auth_service)
    root.mainloop()


if __name__ == "__main__":
    main()

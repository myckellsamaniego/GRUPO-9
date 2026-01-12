import tkinter as tk

from repository.usuario_repository_json import UsuarioRepositoryJSON
from servicios.autenticacion_servicios import AutenticacionService
from factory.fabrica_usuarios import FabricaUsuarios
from gui.login_app import LoginApp


def inicializar_admin(repo):
    """
    Crea el administrador inicial SOLO si no existe.
    Simula el administrador creado por el sistema.
    """

    admin_correo = "admin@uleam.edu.ec"

    if repo.buscar_por_correo(admin_correo):
        return  # Ya existe, no duplicar

    fabrica = FabricaUsuarios()

    admin = fabrica.crear_usuario(
        tipo_usuario="Administrador",
        identificacion="ADM001",
        nombre="Administrador Principal",
        correo=admin_correo,
        password="admin123",
        admin_id="ADMIN-001"
    )

    repo.agregar(admin)


def main():
    # Repository (persistencia JSON)
    usuario_repo = UsuarioRepositoryJSON("usuarios.json")

    # Admin inicial del sistema
    inicializar_admin(usuario_repo)

    # Servicio de autenticación
    auth_service = AutenticacionService(usuario_repo)

    # GUI
    root = tk.Tk()
    LoginApp(root, auth_service)
    root.mainloop()


if __name__ == "__main__":
    main()

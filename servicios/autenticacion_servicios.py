class AutenticacionServicios:
    def __init__(self, usuario_repository):
        self._repo = usuario_repository

    def login(self, correo:str, password:str):
        usuario = self._repo.buscar_por_correo(correo)

        if not usuario:
            raise ValueError("Usuario no encontrado")

        if not usuario.validar_password(password):
            raise ValueError("Contraseña incorrecta")

        return usuario  # ← aquí ya viene con su rol

class AutenticacionService:
    """
    SERVICE:
    Contiene la lógica de autenticación del sistema.
    """

    def __init__(self, usuario_repository):
        self._usuario_repository = usuario_repository

    def login(self, correo: str, password: str):
        """
        Valida credenciales y retorna el usuario autenticado.
        """
        if not correo or not password:
            raise ValueError("Correo y contraseña son obligatorios")

        usuario = self._usuario_repository.buscar_por_correo(correo)

        if not usuario:
            raise ValueError("Usuario no registrado")

        if usuario.password != password:
            raise ValueError("Contraseña incorrecta")

        return usuario

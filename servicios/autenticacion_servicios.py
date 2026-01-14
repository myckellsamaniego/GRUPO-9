"""
Servicio de Autenticación
Maneja login y validación de usuarios
"""


class AutenticacionService:
    """
    Servicio para autenticar usuarios en el sistema
    """

    def __init__(self, usuario_repository):
        """
        Args:
            usuario_repository: Repositorio de usuarios para acceso a datos
        """
        self._usuario_repository = usuario_repository

    def login(self, correo: str, password: str):
        """
        Autentica un usuario con correo y contraseña
        
        Args:
            correo: Correo electrónico del usuario
            password: Contraseña del usuario
            
        Returns:
            Usuario autenticado (Postulante o Administrador)
            
        Raises:
            ValueError: Si las credenciales son inválidas
        """
        # Buscar usuario por correo
        usuario = self._usuario_repository.buscar_por_correo(correo)
        
        if not usuario:
            raise ValueError("Usuario no encontrado. Verifique su correo electrónico.")
        
        # Verificar contraseña
        if usuario.password != password:
            raise ValueError("Contraseña incorrecta. Intente nuevamente.")
        
        return usuario

    def validar_credenciales(self, correo: str, password: str) -> bool:
        """
        Valida si las credenciales son correctas sin retornar el usuario
        
        Args:
            correo: Correo electrónico
            password: Contraseña
            
        Returns:
            True si las credenciales son válidas, False en caso contrario
        """
        try:
            self.login(correo, password)
            return True
        except ValueError:
            return False

    def cambiar_password(self, correo: str, password_actual: str, password_nueva: str):
        """
        Cambia la contraseña de un usuario
        
        Args:
            correo: Correo del usuario
            password_actual: Contraseña actual
            password_nueva: Nueva contraseña
            
        Raises:
            ValueError: Si la contraseña actual es incorrecta
        """
        # Verificar credenciales actuales
        usuario = self.login(correo, password_actual)
        
        # Validar nueva contraseña
        if len(password_nueva) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres")
        
        # Actualizar contraseña
        usuario._password = password_nueva
        self._usuario_repository.actualizar(usuario)

    def existe_correo(self, correo: str) -> bool:
        """
        Verifica si un correo ya está registrado
        
        Args:
            correo: Correo a verificar
            
        Returns:
            True si el correo existe, False en caso contrario
        """
        return self._usuario_repository.buscar_por_correo(correo) is not None
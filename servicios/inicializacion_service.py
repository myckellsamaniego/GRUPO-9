from models.administrador import Administrador

class InicializacionService:
    """
    SERVICE:
    Inicializa datos base del sistema (admin principal).
    """

    def __init__(self, usuario_repository):
        self._usuario_repository = usuario_repository

    def crear_admin_inicial(self):
        """
        Crea el administrador principal solo si no existe.
        """
        correo_admin = "admin@uleam.edu.ec"

        admin_existente = self._usuario_repository.buscar_por_correo(correo_admin)

        if admin_existente:
            return  # Ya existe, no hace nada

        admin = Administrador(
            identificacion="ADM001",
            nombre="Administrador Principal",
            correo=correo_admin,
            password="admin123",
            admin_id="ADMIN-001"
        )

        self._usuario_repository.agregar(admin)

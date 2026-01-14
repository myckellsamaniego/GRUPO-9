"""
Servicio de Inicialización del Sistema
Crea datos iniciales necesarios
"""
from models.administrador import Administrador


class InicializacionService:
    """
    Servicio para inicializar datos del sistema
    """

    def __init__(self, usuario_repository):
        self._usuario_repository = usuario_repository

    def crear_admin_inicial(self):
        """
        Crea un administrador por defecto si no existe ninguno
        
        Credenciales por defecto:
        - Correo: admin@uleam.edu.ec
        - Password: admin123
        """
        correo_admin = "admin@uleam.edu.ec"
        
        # Verificar si ya existe
        admin_existente = self._usuario_repository.buscar_por_correo(correo_admin)
        
        if admin_existente:
            print(f"  ℹ️  Administrador '{correo_admin}' ya existe")
            return admin_existente
        
        # Crear nuevo administrador
        admin = Administrador(
            correo=correo_admin,
            password="admin123",
            identificacion="1234567890",
            nombre="Administrador del Sistema",
            admin_id="ADMIN001"
        )
        
        # Guardar
        self._usuario_repository.agregar(admin)
        print(f"  ✓ Administrador '{correo_admin}' creado exitosamente")
        
        return admin

    def verificar_integridad_datos(self):
        """
        Verifica que los datos del sistema estén correctos
        """
        # Aquí podrías agregar más validaciones
        pass
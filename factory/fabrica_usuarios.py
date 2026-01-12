from models.postulante import Postulante
from models.administrador import Administrador

class FabricaUsuarios:
    """
    FACTORY METHOD:
    Centraliza la creación de usuarios del sistema.

    - crear_usuario(): cuando el sistema CREA usuarios nuevos
    - crear_desde_dict(): cuando el sistema RECONSTRUYE desde JSON
    """

    # ===== CASO 1: creación normal (GUI, registro) =====
    def crear_usuario(self, tipo_usuario: str, **kwargs):

        if tipo_usuario == "Postulante":
            return Postulante(kwargs["datos_personales"])

        elif tipo_usuario == "Administrador":
            return Administrador(
                kwargs["identificacion"],
                kwargs["nombre"],
                kwargs["admin_id"]
            )

        else:
            raise ValueError(f"Tipo de usuario no válido: '{tipo_usuario}'")

    # ===== CASO 2: reconstrucción desde persistencia =====
    def crear_desde_dict(self, data: dict):

        if data["tipo"] == "ADMIN":
            return Administrador(
                identificacion=data["identificacion"],
                nombre=data["nombre"],
                admin_id=data["admin_id"]
            )

        elif data["tipo"] == "POSTULANTE":
            return Postulante(
                datos_personales=data["datos_personales"]  # luego se reconstruye
            )

        else:
            raise ValueError("Tipo de usuario desconocido en persistencia")

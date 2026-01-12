from models.postulante import Postulante
from models.administrador import Administrador

class FabricaUsuarios:
    """
    FACTORY METHOD:
    Centraliza la creación de usuarios del sistema.

    - crear_usuario(): creación desde GUI (registro)
    - crear_desde_dict(): reconstrucción desde JSON
    """

    # ===== CASO 1: creación normal (GUI, registro) =====
    def crear_usuario(self, tipo_usuario: str, **kwargs):

        if tipo_usuario == "Postulante":
            return Postulante(
                correo=kwargs["correo"],
                password=kwargs["password"],
                datos_personales=kwargs["datos_personales"]
            )

        elif tipo_usuario == "Administrador":
            return Administrador(
                identificacion=kwargs["identificacion"],
                nombre=kwargs["nombre"],
                correo=kwargs["correo"],
                password=kwargs["password"],
                admin_id=kwargs["admin_id"]
            )

        else:
            raise ValueError(f"Tipo de usuario no válido: '{tipo_usuario}'")

    # ===== CASO 2: reconstrucción desde persistencia =====
    def crear_desde_dict(self, data: dict):

        if data["tipo"] == "ADMIN":
            return Administrador(
                identificacion=data["identificacion"],
                nombre=data["nombre"],
                correo=data["correo"],
                password=data["password"],
                admin_id=data["admin_id"]
            )

        elif data["tipo"] == "POSTULANTE":
            return Postulante(
                correo=data["correo"],
                password=data["password"],
                datos_personales=None  # se reconstruyen después
            )

        else:
            raise ValueError("Tipo de usuario desconocido en persistencia")

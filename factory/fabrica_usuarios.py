from models.postulante import Postulante
from models.administrador import Administrador

# ====== Fábrica con Factory Method ======
class FabricaUsuarios:
    """
    FACTORY METHOD:
    Centraliza la creación de usuarios del sistema.
    """

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

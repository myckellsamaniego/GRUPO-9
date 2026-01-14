from models.postulante import Postulante
from models.administrador import Administrador
from models.datos_personales import DatosPersonales


class FabricaUsuarios:
    """
    FACTORY METHOD:
    Centraliza la creación de usuarios del sistema.
    
    Métodos:
    - crear_usuario(): Creación desde GUI (registro)
    - crear_desde_dict(): Reconstrucción desde JSON
    """

    def crear_usuario(self, tipo_usuario: str, **kwargs):
        """
        Crea un usuario desde la interfaz de usuario
        
        Args:
            tipo_usuario: "Postulante" o "Administrador"
            **kwargs: Parámetros necesarios para crear el usuario
            
        Returns:
            Instancia de Usuario (Postulante o Administrador)
            
        Raises:
            ValueError: Si el tipo de usuario no es válido
        """
        
        if tipo_usuario == "Postulante":
            # El correo puede venir explícitamente o desde datos_personales
            correo = kwargs.get("correo")
            if not correo and "datos_personales" in kwargs:
                correo = kwargs["datos_personales"].correo
            
            return Postulante(
                correo=correo,
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

    def crear_desde_dict(self, data: dict):
        """
        Reconstruye un usuario desde datos JSON
        
        Args:
            data: Diccionario con los datos del usuario
            
        Returns:
            Instancia de Usuario reconstruida
            
        Raises:
            ValueError: Si el tipo de usuario es desconocido
        """
        
        if data["tipo"] == "ADMIN":
            return Administrador(
                identificacion=data["identificacion"],
                nombre=data["nombre"],
                correo=data["correo"],
                password=data["password"],
                admin_id=data["admin_id"]
            )

        elif data["tipo"] == "POSTULANTE":
            # Reconstruir datos personales desde el diccionario
            datos_personales = DatosPersonales.from_dict(data["datos_personales"])
            
            return Postulante(
                correo=data["correo"],
                password=data["password"],
                datos_personales=datos_personales
            )

        else:
            raise ValueError(f"Tipo de usuario desconocido en persistencia: {data['tipo']}")
from models.usuario import Usuario

class Administrador(Usuario):

    def __init__(
        self,
        correo: str,
        password: str,
        identificacion: str,
        nombre: str,
        admin_id: str
    ):
        super().__init__(correo, password)

        if not admin_id:
            raise ValueError("El ID del administrador es obligatorio")

        self._identificacion = identificacion
        self._nombre = nombre
        self._admin_id = admin_id

    @property
    def admin_id(self):
        return self._admin_id

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    def obtener_tipo(self) -> str:
        return "ADMIN"

    def to_dict(self) -> dict:
        """Convierte el administrador a diccionario para persistencia"""
        return {
            "tipo": "ADMIN",
            "correo": self._correo,
            "password": self._password,
            "identificacion": self._identificacion,
            "nombre": self._nombre,
            "admin_id": self._admin_id
        }
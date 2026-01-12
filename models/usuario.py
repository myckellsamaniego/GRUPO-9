from abc import ABC, abstractmethod

class Usuario(ABC):
    """
    Clase base de autenticación del sistema
    """

    def __init__(self, correo: str, password: str):
        if not correo or not password:
            raise ValueError("Correo y contraseña son obligatorios")

        self._correo = correo
        self._password = password

    @property
    def correo(self):
        return self._correo

    @property
    def password(self):
        return self._password

    @abstractmethod
    def obtener_tipo(self) -> str:
        pass

    def __str__(self):
        return f"{self.obtener_tipo()} - {self.correo}"

from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, identificacion: str, nombre: str):
        if not identificacion or not nombre:
            raise ValueError("La identificación y el nombre son obligatorios")

        self._identificacion = identificacion
        self._nombre = nombre

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def obtener_tipo(self) -> str:
        pass

    def __str__(self):
        return f"{self.obtener_tipo()} - {self.nombre} ({self.identificacion})"

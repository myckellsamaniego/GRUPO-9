from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nombres="", correo="", clave=""):
        self._nombres = nombres
        self._correo = correo
        self._clave = clave

    @property
    def nombres(self):
        return self._nombres

    @nombres.setter
    def nombres(self, value):
        self._nombres = value

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, value):
        self._correo = value

    @property
    def clave(self):
        return self._clave

    @clave.setter
    def clave(self, value):
        self._clave = value

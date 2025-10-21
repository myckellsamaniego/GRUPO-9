from abc import ABC, abstractmethod

class Usuario(ABC):
    
    def __init__(self, nombre, correo, clave, rol):
        self._nombre = nombre
        self._correo = correo
        self._clave = clave
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo):
        if nuevo:
            self._nombre = nuevo
    
    @property
    def correo(self):
        return self._correo
    
    @correo.setter
    def correo(self, nuevo):
        if nuevo:
            self._correo = nuevo
            
    @property
    def clave(self):
        return self._clave
    
    @clave.setter
    def clave(self, nuevo):
        if nuevo:
            self._clave = nuevo
            
    def Iniciar_Sesion(self):
        print(f"{self._nombre} ha iniciado sesión.")
        
    def Cerrar_Sesion(self):
        print(f"{self._nombre} ha cerrado sesión.")
        
    @abstractmethod
    def mostrar_informacion(self):
        pass

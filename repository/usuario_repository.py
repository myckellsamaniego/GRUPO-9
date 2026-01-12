from abc import ABC, abstractmethod

class UsuarioRepository(ABC):
    """
    REPOSITORY (INTERFAZ)
    """

    @abstractmethod
    def agregar(self, usuario):
        pass

    @abstractmethod
    def buscar_por_correo(self, correo):
        pass

    @abstractmethod
    def listar(self):
        pass

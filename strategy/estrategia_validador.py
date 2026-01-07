# strategy/estrategia_validador.py
from abc import ABC, abstractmethod

class EstrategiaValidador(ABC):
    @abstractmethod
    def validar(self, postulante, oferta) -> bool:
        pass

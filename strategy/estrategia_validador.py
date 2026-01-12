from abc import ABC, abstractmethod


class EstrategiaValidador(ABC):
    """
    Interfaz base para todas las estrategias de validación.
    Cada estrategia valida UNA regla específica del proceso.
    """

    @abstractmethod
    def validar(self, contexto: dict):
        """
        Valida una regla específica usando el contexto del proceso.

        El contexto puede contener:
        - 'postulante'
        - 'periodo'
        - 'sede'
        - 'oferta'
        - 'inscripcion' (si aplica)

        Si la validación falla, debe lanzar una excepción.
        """
        pass

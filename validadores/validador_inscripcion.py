from abc import ABC, abstractmethod

# ============================================================
# PATRÓN STRATEGY (INTERFAZ)
# ------------------------------------------------------------
# Esta clase define el CONTRATO que deben cumplir todos
# los validadores de inscripción.
#
# Inscripcion NO sabe qué regla se usa, solo sabe que
# existe un método llamado "validar".
#
# Esto desacopla el proceso de inscripción de las reglas.
# ============================================================

class ValidadorInscripcion(ABC):

    @abstractmethod
    def validar(self, postulante, oferta) -> bool:
        """
        Método que TODA estrategia de validación debe implementar.

        Retorna:
        - True  -> si la inscripción cumple la regla
        - False -> si no la cumple
        """
        pass

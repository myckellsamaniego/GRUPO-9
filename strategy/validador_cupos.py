from strategy.estrategia_validador import EstrategiaValidador

class ValidadorCupos(EstrategiaValidador):
    """
    ESTRATEGIA CONCRETA
    Valida que existan cupos disponibles en la oferta académica.
    """

    def validar(self, postulante, oferta) -> bool:
        return oferta.cupos > 0

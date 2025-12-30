from validators.validador_inscripcion import ValidadorInscripcion

# ============================================================
# IMPLEMENTACIÓN CONCRETA DEL STRATEGY
# ------------------------------------------------------------
# Esta regla valida que la oferta académica tenga cupos
# disponibles al momento de la inscripción.
# ============================================================

class ValidadorCupos(ValidadorInscripcion):

    def validar(self, postulante, oferta) -> bool:
        return oferta.cupos > 0

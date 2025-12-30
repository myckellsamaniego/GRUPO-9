from validators.validador_inscripcion import ValidadorInscripcion

# ============================================================
# IMPLEMENTACIÓN CONCRETA DEL STRATEGY
# ------------------------------------------------------------
# Esta clase representa UNA REGLA ESPECÍFICA:
# "El postulante debe tener datos personales completos"
#
# Implementa la interfaz ValidadorInscripcion
# ============================================================

class ValidadorDatosCompletos(ValidadorInscripcion):

    def validar(self, postulante, oferta) -> bool:
        datos = postulante.datos_personales

        # Regla simple: verificar que los campos obligatorios existan
        return all([
            datos.nombre,
            datos.apellidos,
            datos.cedula,
            datos.correo
        ])

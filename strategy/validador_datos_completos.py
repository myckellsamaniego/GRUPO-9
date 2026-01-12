from strategy.estrategia_validador import EstrategiaValidador
from excepciones.errores_inscripcion import ErrorDatosIncompletos


class ValidadorDatosCompletos(EstrategiaValidador):
    """
    Valida que el postulante tenga los datos personales
    completos y correctos para el proceso de inscripción.
    """

    def validar(self, contexto: dict):
        #  Verificar que el postulante exista en el contexto
        postulante = contexto.get("postulante")

        if postulante is None:
            raise ErrorDatosIncompletos(
                "No se encontró información del postulante"
            )

        # Validaciones
        if not postulante.nombres or not postulante.apellidos:
            raise ErrorDatosIncompletos(
                "El postulante debe tener nombres y apellidos completos"
            )

        if not postulante.cedula:
            raise ErrorDatosIncompletos(
                "El postulante debe registrar su cédula"
            )

        if not postulante.fecha_nacimiento:
            raise ErrorDatosIncompletos(
                "El postulante debe registrar su fecha de nacimiento"
            )

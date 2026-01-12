from strategy.estrategia_validador import EstrategiaValidador
from excepciones.errores_postulacion import (
    PostulacionError,
    PostulacionDuplicadaError,
    PeriodoNoActivoError
)


class ValidadorPostulacion(EstrategiaValidador):
    """
    Valida las reglas del proceso de postulación al examen.
    """

    def validar(self, contexto: dict):

        #  Validar estructura del contexto
        inscripcion = contexto.get("inscripcion")
        periodo = contexto.get("periodo")
        repositorio = contexto.get("repositorio_postulaciones")

        if inscripcion is None:
            raise PostulacionError(
                "No se puede postular sin una inscripción válida"
            )

        if periodo is None:
            raise PostulacionError(
                "No se ha definido un periodo de postulación"
            )

        #  El periodo debe estar activo
        if not periodo.activo:
            raise PeriodoNoActivoError(
                "El periodo de postulación no se encuentra activo"
            )

        #  No debe existir una postulación previa
        if repositorio and repositorio.existe_postulacion(
            inscripcion.postulante,
            periodo
        ):
            raise PostulacionDuplicadaError(
                "El postulante ya está postulado en este periodo"
            )

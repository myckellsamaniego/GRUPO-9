from strategy.estrategia_validador import EstrategiaValidador
from excepciones.errores_inscripcion import ErrorPostulacionNoValida


class ValidadorPostulacion(EstrategiaValidador):
    """
    Valida que una postulación al examen sea válida
    según las reglas del proceso SENESCYT.
    """

    def validar(self, contexto: dict):

        inscripcion = contexto.get("inscripcion")
        periodo = contexto.get("periodo")
        repo = contexto.get("repositorio_postulaciones")

        # Debe existir inscripción
        if inscripcion is None:
            raise ErrorPostulacionNoValida(
                "No se puede postular sin una inscripción previa"
            )

        # El periodo debe existir y estar activo
        if periodo is None or not periodo.activo:
            raise ErrorPostulacionNoValida(
                "El periodo de postulación no está activo"
            )

        # No debe existir una postulación previa
        if repo and repo.existe_postulacion(
            inscripcion.postulante,
            periodo
        ):
            raise ErrorPostulacionNoValida(
                "El postulante ya se encuentra postulado en este periodo"
            )

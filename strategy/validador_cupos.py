from strategy.estrategia_validador import EstrategiaValidador
from excepciones.errores_inscripcion import ErrorCuposNoDisponibles


class ValidadorCupos(EstrategiaValidador):
    """
    Valida que exista disponibilidad para rendir el examen
    en la sede y periodo seleccionados.
    """

    def validar(self, contexto: dict):
        sede = contexto.get("sede")
        periodo = contexto.get("periodo")

        #  Validar que exista sede
        if sede is None:
            raise ErrorCuposNoDisponibles(
                "No se ha seleccionado una sede para rendir el examen"
            )

        # Validar que el periodo exista
        if periodo is None:
            raise ErrorCuposNoDisponibles(
                "No se ha seleccionado un periodo válido"
            )

        # Validar que el periodo esté activo
        if not periodo.activo:
            raise ErrorCuposNoDisponibles(
                "El periodo de inscripción no se encuentra activo"
            )

        #  Validar que la sede esté habilitada
        if hasattr(sede, "habilitada") and not sede.habilitada:
            raise ErrorCuposNoDisponibles(
                "La sede seleccionada no está habilitada"
            )

        #  Validar disponibilidad (si aplica)
        if hasattr(sede, "cupo_disponible") and sede.cupo_disponible <= 0:
            raise ErrorCuposNoDisponibles(
                "No hay cupos disponibles en la sede seleccionada"
            )

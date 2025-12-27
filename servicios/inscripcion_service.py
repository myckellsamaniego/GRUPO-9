from excepciones.errores_incripcion import InscripcionDuplicadaError, CuposAgotadosError


class InscripcionService:

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def registrar(self, inscripcion):

        existente = self.repositorio.buscar_por_cedula(
            inscripcion.postulante.cedula
        )

        if existente:
            raise InscripcionDuplicadaError(
                "El postulante ya tiene una inscripción"
            )

        if inscripcion.oferta.cupos <= 0:
            raise CuposAgotadosError("No hay cupos disponibles")

        if inscripcion.validar():
            inscripcion.aprobar()
            self.repositorio.guardar(inscripcion)
        else:
            self.repositorio.guardar(inscripcion)

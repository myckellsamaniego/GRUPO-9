class PostulacionRepository:

    def __init__(self):
        self._postulaciones = []

    def guardar(self, postulacion):
        self._postulaciones.append(postulacion)

    def existe_postulacion(self, postulante, periodo):
        return any(
            p.inscripcion.postulante == postulante and
            p.periodo == periodo and
            p.estado == "REGISTRADA"
            for p in self._postulaciones
        )

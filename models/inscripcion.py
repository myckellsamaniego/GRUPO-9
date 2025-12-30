class Inscripcion:
    ESTADOS = ("PENDIENTE", "APROBADA", "RECHAZADA")

    def __init__(self, postulante, oferta, validador_datos, validador_cupos):
        self._postulante = postulante
        self._oferta = oferta
        self._validador_datos = validador_datos
        self._validador_cupos = validador_cupos
        self._estado = "PENDIENTE"

    @property
    def estado(self):
        return self._estado

    @property
    def postulante(self):
        return self._postulante

    @property
    def oferta(self):
        return self._oferta

    def validar(self):
        """
        TEMPLATE METHOD:
        Define el flujo fijo del proceso de inscripción.
        """
        if self._estado != "PENDIENTE":
            raise ValueError("La inscripción ya fue procesada")

        if not self._validador_datos.validar(self._postulante, self._oferta):
            self._rechazar()
            return

        if not self._validador_cupos.validar(self._postulante, self._oferta):
            self._rechazar()
            return

        self._aprobar()


    def _aprobar(self):
        self._oferta.ocupar_cupo()
        self._estado = "APROBADA"

    def _rechazar(self):
        self._estado = "RECHAZADA"


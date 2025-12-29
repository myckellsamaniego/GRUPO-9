class Inscripcion:
    ESTADOS = ("PENDIENTE", "APROBADA", "RECHAZADA")

    def __init__(self, postulante, oferta, validador):
        self._postulante = postulante
        self._oferta = oferta
        self._validador = validador
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
        if self._estado != "PENDIENTE":
            raise ValueError("La inscripción ya fue procesada")

        es_valida = self._validador.validar(self._postulante, self._oferta)

        if es_valida:
            self._aprobar()
        else:
            self._rechazar()

    def _aprobar(self):
        self._oferta.ocupar_cupo()
        self._estado = "APROBADA"

    def _rechazar(self):
        self._estado = "RECHAZADA"

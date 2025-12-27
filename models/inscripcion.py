class Inscripcion:

    def __init__(self, postulante, oferta, validador):
        self.postulante = postulante
        self.oferta = oferta
        self.validador = validador
        self.aprobada = False

    def validar(self):
        return self.validador.validar(self.postulante, self.oferta)

    def aprobar(self):
        if self.oferta.cupos > 0:
            self.aprobada = True
            self.oferta.cupos -= 1

class Postulacion:
    ESTADOS = ("REGISTRADA", "ANULADA")

    def __init__(self, inscripcion, periodo):
        self._inscripcion = inscripcion
        self._periodo = periodo
        self._estado = "REGISTRADA"

    @property
    def inscripcion(self):
        return self._inscripcion

    @property
    def periodo(self):
        return self._periodo

    @property
    def estado(self):
        return self._estado

    def anular(self):
        self._estado = "ANULADA"

    def to_dict(self):
        return {
            "cedula_postulante": self.inscripcion.postulante.datos_personales.cedula,
            "periodo": self.periodo.nombre,
            "estado_postulacion": self.estado
        }

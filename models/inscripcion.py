class Inscripcion:
    ESTADOS = ("PENDIENTE", "APROBADA", "RECHAZADA")

    def __init__(self, postulante, oferta, password):
        self._postulante = postulante
        self._oferta = oferta
        self._password = password
        self._estado = "PENDIENTE"

    @property
    def postulante(self):
        return self._postulante
    
    @property
    def oferta(self):
        return self._oferta

    @property
    def estado(self):
        return self._estado

    def to_dict(self):
        return {
            "cedula_postulante": self.postulante.datos_personales.cedula,
            "nombre_postulante": f"{self.postulante.datos_personales.nombre} {self.postulante.datos_personales.apellidos}",
            "carrera_seleccionada": self.oferta.nombre,
            "estado_inscripcion": self.estado,
            "password": self._password
        }

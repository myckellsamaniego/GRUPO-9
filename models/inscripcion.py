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
    
    @property
    def password(self):
        return self._password

    def aprobar(self):
        """Aprueba la inscripción"""
        if self._estado != "PENDIENTE":
            raise ValueError("Solo se pueden aprobar inscripciones pendientes")
        self._estado = "APROBADA"

    def rechazar(self):
        """Rechaza la inscripción"""
        if self._estado != "PENDIENTE":
            raise ValueError("Solo se pueden rechazar inscripciones pendientes")
        self._estado = "RECHAZADA"

    def to_dict(self):
        """Convierte la inscripción a diccionario para persistencia"""
        return {
            "cedula_postulante": self.postulante.datos_personales.cedula,
            "nombre_postulante": f"{self.postulante.datos_personales.nombre} {self.postulante.datos_personales.apellidos}",
            "correo_postulante": self.postulante.correo,
            "datos_personales": self.postulante.datos_personales.to_dict(),
            "codigo_oferta": self.oferta.codigo,
            "carrera_seleccionada": self.oferta.nombre,
            "cupos_oferta": self.oferta.cupos,
            "estado_inscripcion": self.estado,
            "password": self._password
        }
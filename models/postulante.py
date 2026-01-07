from models.usuario import Usuario
from models.datos_personales import DatosPersonales


class Postulante(Usuario):
    def __init__(self, datos_personales: DatosPersonales):
        super().__init__(
            identificacion=datos_personales.cedula,
            nombre=datos_personales.nombre
        )
        self._datos_personales = datos_personales

    @property
    def datos_personales(self) -> DatosPersonales:
        return self._datos_personales

    def obtener_tipo(self) -> str:
        return "Postulante"

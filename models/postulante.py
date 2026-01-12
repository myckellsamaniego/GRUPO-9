from models.usuario import Usuario
from models.datos_personales import DatosPersonales

class Postulante(Usuario):
    """
    Representa a un postulante que se inscribe al proceso de admisión.
    """

    def __init__(
        self,
        correo: str,
        password: str,
        datos_personales: DatosPersonales
    ):
        super().__init__(correo, password)

        if not datos_personales:
            raise ValueError("Los datos personales son obligatorios")

        self._datos_personales = datos_personales

    @property
    def datos_personales(self) -> DatosPersonales:
        return self._datos_personales

    def obtener_tipo(self) -> str:
        return "Postulante"

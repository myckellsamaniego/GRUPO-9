from models.usuario import Usuario

class Postulante(Usuario):
    def __init__(self, identificacion: str, nombre: str, promedio: float):
        super().__init__(identificacion, nombre)
        self._promedio = promedio

    @property
    def promedio(self):
        return self._promedio

    def obtener_tipo(self) -> str:
        return "Postulante"

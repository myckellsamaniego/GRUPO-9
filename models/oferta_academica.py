class OfertaAcademica:
    def __init__(self, codigo: str, nombre: str, cupos: int):
        self._codigo = codigo
        self._nombre = nombre
        self._cupos = cupos

    @property
    def cupos(self):
        return self._cupos

    def reducir_cupo(self):
        if self._cupos <= 0:
            raise ValueError("No hay cupos disponibles")
        self._cupos -= 1

class OfertaAcademica:
    def __init__(self, codigo: str, nombre: str, cupos: int):
        if not codigo or not nombre:
            raise ValueError("El código y nombre de la oferta son obligatorios")
        if cupos < 0:
            raise ValueError("Los cupos no pueden ser negativos")

        self._codigo = codigo
        self._nombre = nombre
        self._cupos = cupos

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def cupos(self):
        return self._cupos

    def ocupar_cupo(self):
        if self._cupos <= 0:
            raise ValueError("No hay cupos disponibles")
        self._cupos -= 1

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
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cupos(self) -> int:
        return self._cupos

    def hay_cupos(self) -> bool:
        return self._cupos > 0

    def ocupar_cupo(self):
        if not self.hay_cupos():
            raise ValueError("No hay cupos disponibles")
        self._cupos -= 1

class InscripcionError(Exception):
    pass


class InscripcionDuplicadaError(InscripcionError):
    pass


class CuposAgotadosError(InscripcionError):
    pass

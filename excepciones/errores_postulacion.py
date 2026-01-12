class PostulacionError(Exception):
    """Error base del proceso de postulación"""
    pass


class PostulacionNoValidaError(PostulacionError):
    """La postulación no cumple las reglas del proceso"""
    pass


class PostulacionDuplicadaError(PostulacionError):
    """El postulante ya está postulado en el periodo"""
    pass


class PeriodoNoActivoError(PostulacionError):
    """El periodo no se encuentra activo"""
    pass

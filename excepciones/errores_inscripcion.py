class InscripcionError(Exception):
    """Error base del proceso de inscripción"""
    pass


class InscripcionDuplicadaError(InscripcionError):
    """El postulante ya se encuentra inscrito"""
    pass


class CuposAgotadosError(InscripcionError):
    """No existen cupos disponibles en la oferta"""
    pass


class DatosIncompletosError(InscripcionError):
    """Faltan datos personales obligatorios"""
    pass

class ErrorDatosIncompletos(Exception):
    """
    Se lanza cuando el postulante no ha completado sus datos personales.
    """
    pass

class ErrorCuposNoDisponibles(Exception):
    """
    Se lanza cuando la oferta académica no tiene cupos disponibles.
    """
    pass

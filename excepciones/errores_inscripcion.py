"""
Excepciones personalizadas para el proceso de inscripción
"""

class InscripcionError(Exception):
    """Error base del proceso de inscripción"""
    pass


class InscripcionDuplicadaError(InscripcionError):
    """El postulante ya se encuentra inscrito"""
    pass


class CuposAgotadosError(InscripcionError):
    """No existen cupos disponibles en la oferta académica"""
    pass


class DatosIncompletosError(InscripcionError):
    """Faltan datos personales obligatorios del postulante"""
    pass


class CuposNoDisponiblesError(InscripcionError):
    """No hay cupos disponibles en la sede o periodo seleccionado"""
    pass


class OfertaNoDisponibleError(InscripcionError):
    """La oferta académica no está disponible para inscripción"""
    pass
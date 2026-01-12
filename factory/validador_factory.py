from typing import List
from strategy.estrategia_validador import EstrategiaValidador
from strategy.validador_datos_completos import ValidadorDatosCompletos
from strategy.validador_cupos import ValidadorCupos
from strategy.validador_postulacion import ValidadorPostulacion


class ValidadorProcesoInscripcion:

    def __init__(self, validadores: List[EstrategiaValidador]):
        self._validadores = validadores

    def validar(self, contexto: dict):
        """
        Ejecuta todos los validadores.
        Si uno falla, se lanza la excepción y se detiene el proceso.

        El contexto debe contener:
        - 'postulante'
        - 'periodo'
        - 'sede'
        - 'oferta' (si aplica)
        """
        for validador in self._validadores:
            validador.validar(contexto)


class ValidadorFactory:
    @staticmethod
    def crear_validador_inscripcion() -> ValidadorProcesoInscripcion:
        """
        Construye el validador completo para INSCRIPCIÓN.
        """
        validadores = [
            ValidadorDatosCompletos(),
            ValidadorCupos(),
        ]
        return ValidadorProcesoInscripcion(validadores)
    @staticmethod
    def crear_validador_postulacion():
        return ValidadorProcesoInscripcion([
            ValidadorPostulacion()
    ])


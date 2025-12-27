from abc import ABC, abstractmethod

# Interfaz del producto
class ValidadorInscripcion(ABC):

    @abstractmethod
    def validar(self, postulante, oferta):
        pass


# Implementaciones concretas del Validador
class ValidacionRegular(ValidadorInscripcion):

    def validar(self, postulante, oferta):
        # Reglas para inscripción regular
        return postulante.promedio >= 7 and oferta.cupos > 0


class ValidacionExtraordinaria(ValidadorInscripcion):

    def validar(self, postulante, oferta):
        # Reglas para inscripción extraordinaria
        return postulante.promedio >= 5 and oferta.cupos > 0


# Fábrica con Factory Method
class ValidadorFactory:

    def crear_validador(self, tipo_validacion: str) -> ValidadorInscripcion:
        if tipo_validacion == "regular":
            return ValidacionRegular()
        elif tipo_validacion == "extraordinaria":
            return ValidacionExtraordinaria()
        else:
            raise ValueError(f"Tipo de validación no válido: '{tipo_validacion}'")


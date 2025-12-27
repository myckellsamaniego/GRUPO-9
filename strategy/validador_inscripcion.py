from abc import ABC, abstractmethod

#  Interfaz de la estrategia 
class ValidadorInscripcion(ABC):

    @abstractmethod
    def validar(self, postulante, oferta):
        pass


#  Estrategias concretas 
class ValidacionRegular(ValidadorInscripcion):

    def validar(self, postulante, oferta):
        # Regla para inscripción regular
        return postulante.promedio >= 7 and oferta.cupos > 0


class ValidacionExtraordinaria(ValidadorInscripcion):

    def validar(self, postulante, oferta):
        # Regla para inscripción extraordinaria
        return postulante.promedio >= 5 and oferta.cupos > 0


#  Contexto que usa la estrategia 
class Inscripcion:

    def __init__(self, postulante, oferta, estrategia: ValidadorInscripcion):
        self.postulante = postulante
        self.oferta = oferta
        self.estrategia = estrategia
        self.aprobada = False

    def validar(self):
        return self.estrategia.validar(self.postulante, self.oferta)



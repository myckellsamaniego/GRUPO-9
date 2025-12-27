from abc import ABC, abstractmethod


#  Interfaz del Repository 
class InscripcionRepository(ABC):

    @abstractmethod
    def guardar(self, inscripcion):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_postulante(self, identificacion):
        pass

    @abstractmethod
    def listar_aprobadas(self):
        pass

    @abstractmethod
    def eliminar(self, identificacion):
        pass


#  Implementación en memoria 
class InscripcionRepositoryMemoria(InscripcionRepository):

    def __init__(self):
        self._inscripciones = []

    def guardar(self, inscripcion):
        self._inscripciones.append(inscripcion)

    def listar(self):
        return self._inscripciones

    def buscar_por_postulante(self, identificacion):
        for inscripcion in self._inscripciones:
            if inscripcion.postulante.identificacion == identificacion:
                return inscripcion
        return None

    def listar_aprobadas(self):
        return [i for i in self._inscripciones if i.aprobada]

    def eliminar(self, identificacion):
        self._inscripciones = [
            i for i in self._inscripciones
            if i.postulante.identificacion != identificacion
        ]
from abc import ABC, abstractmethod
import json
import os

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
class InscripcionRepositoryJSON:
    def __init__(self, archivo="inscripciones.json"):
        self.archivo = archivo

    def guardar(self, inscripcion):
        datos = self.listar()
        datos.append(inscripcion.to_dict())
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def listar(self):
        if not os.path.exists(self.archivo): return []
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError: # Maneja el caso de un archivo JSON vacío o corrupto
            return []
from abc import ABC, abstractmethod
import json
import os


# ========== INTERFAZ DEL REPOSITORY ==========
class InscripcionRepository(ABC):
    """Interfaz base para el repositorio de inscripciones"""

    @abstractmethod
    def guardar(self, inscripcion):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_cedula(self, cedula):
        pass

    @abstractmethod
    def listar_aprobadas(self):
        pass

    @abstractmethod
    def eliminar(self, cedula):
        pass

    @abstractmethod
    def actualizar_dict(self, cedula, inscripcion_dict):
        pass


# ========== IMPLEMENTACIÓN EN MEMORIA ==========
class InscripcionRepositoryMemoria(InscripcionRepository):
    """Implementación en memoria (para testing)"""

    def __init__(self):
        self._inscripciones = []

    def guardar(self, inscripcion):
        self._inscripciones.append(inscripcion)

    def listar(self):
        """Retorna lista de objetos Inscripcion"""
        return list(self._inscripciones)

    def buscar_por_cedula(self, cedula):
        for inscripcion in self._inscripciones:
            if inscripcion.postulante.datos_personales.cedula == cedula:
                return inscripcion
        return None

    def listar_aprobadas(self):
        return [i for i in self._inscripciones if i.estado == "APROBADA"]

    def eliminar(self, cedula):
        self._inscripciones = [
            i for i in self._inscripciones
            if i.postulante.datos_personales.cedula != cedula
        ]

    def actualizar_dict(self, cedula, inscripcion_dict):
        """En memoria, esto no aplica de la misma forma"""
        inscripcion = self.buscar_por_cedula(cedula)
        if inscripcion:
            inscripcion._estado = inscripcion_dict["estado_inscripcion"]


# ========== IMPLEMENTACIÓN JSON ==========
class InscripcionRepositoryJSON(InscripcionRepository):
    """
    Implementación con persistencia en archivo JSON.
    
    IMPORTANTE: Este repositorio trabaja con diccionarios, no con objetos.
    Los métodos retornan dicts que representan inscripciones.
    """
    
    def __init__(self, archivo="inscripciones.json"):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            self._crear_archivo_vacio()

    def _crear_archivo_vacio(self):
        """Crea un archivo JSON vacío"""
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def _leer_json(self):
        """Lee el archivo y retorna lista de diccionarios"""
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _guardar_json(self, datos):
        """Guarda la lista de diccionarios en JSON"""
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def guardar(self, inscripcion):
        """
        Guarda una inscripción en formato JSON
        
        Args:
            inscripcion: Objeto Inscripcion a guardar
        """
        datos = self._leer_json()
        datos.append(inscripcion.to_dict())
        self._guardar_json(datos)

    def listar(self):
        """
        Lista todas las inscripciones
        
        Returns:
            Lista de diccionarios que representan inscripciones
        """
        return self._leer_json()

    def buscar_por_cedula(self, cedula):
        """
        Busca una inscripción por cédula del postulante
        
        Args:
            cedula: Cédula del postulante
            
        Returns:
            Diccionario de la inscripción o None si no existe
        """
        datos = self._leer_json()
        for insc in datos:
            if insc["cedula_postulante"] == cedula:
                return insc
        return None

    def listar_aprobadas(self):
        """Lista solo las inscripciones aprobadas"""
        datos = self._leer_json()
        return [i for i in datos if i["estado_inscripcion"] == "APROBADA"]

    def listar_por_estado(self, estado):
        """Lista inscripciones por estado específico"""
        datos = self._leer_json()
        return [i for i in datos if i["estado_inscripcion"] == estado]

    def eliminar(self, cedula):
        """
        Elimina una inscripción por cédula
        
        Args:
            cedula: Cédula del postulante a eliminar
        """
        datos = self._leer_json()
        datos = [d for d in datos if d["cedula_postulante"] != cedula]
        self._guardar_json(datos)

    def actualizar_dict(self, cedula, inscripcion_dict):
        """
        Actualiza una inscripción existente
        
        Args:
            cedula: Cédula del postulante
            inscripcion_dict: Diccionario con los datos actualizados
        """
        datos = self._leer_json()
        
        for i, insc in enumerate(datos):
            if insc["cedula_postulante"] == cedula:
                datos[i] = inscripcion_dict
                self._guardar_json(datos)
                return
        
        raise ValueError(f"Inscripción con cédula {cedula} no encontrada")
"""
Repositorio de Sedes - Persistencia en JSON
"""
import json
import os
from typing import List
from models.sede import Sede


class SedeRepositoryJSON:
    """Repositorio para gestionar sedes del sistema"""

    def __init__(self, archivo: str = "data/sedes.json"):
        self.archivo = archivo
        self._sedes = []
        self._cargar_desde_archivo()

    def _cargar_desde_archivo(self):
        """Carga sedes desde el archivo JSON"""
        if not os.path.exists(self.archivo):
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            self._crear_sedes_iniciales()
            return
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self._sedes = [
                    Sede(
                        nombre=d['nombre'],
                        direccion=d['direccion'],
                        ciudad=d['ciudad'],
                        capacidad=d['capacidad']
                    )
                    for d in datos
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self._crear_sedes_iniciales()

    def _crear_sedes_iniciales(self):
        """Crea sedes iniciales del sistema"""
        sedes_iniciales = [
            Sede("Campus Manta", "Av. Circunvalación, Vía San Mateo", "Manta", 500),
            Sede("Campus Chone", "Av. Universitaria", "Chone", 300),
            Sede("Campus Bahía", "Calle Principal s/n", "Bahía de Caráquez", 200),
            Sede("Campus Pedernales", "Av. Central", "Pedernales", 150),
        ]
        self._sedes = sedes_iniciales
        self._guardar_en_archivo()

    def _guardar_en_archivo(self):
        """Guarda sedes en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        
        datos = [
            {
                "nombre": sede.nombre,
                "direccion": sede.direccion,
                "ciudad": sede.ciudad,
                "capacidad": sede.capacidad
            }
            for sede in self._sedes
        ]
        
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def agregar(self, sede: Sede) -> None:
        """Agrega una nueva sede"""
        # Verificar que no exista una sede con el mismo nombre
        if any(s.nombre == sede.nombre for s in self._sedes):
            raise ValueError(f"Ya existe una sede con el nombre '{sede.nombre}'")
        
        self._sedes.append(sede)
        self._guardar_en_archivo()

    def listar_todas(self) -> List[Sede]:
        """Retorna todas las sedes"""
        return list(self._sedes)

    def buscar_por_nombre(self, nombre: str):
        """Busca una sede por nombre"""
        for sede in self._sedes:
            if sede.nombre.lower() == nombre.lower():
                return sede
        return None

    def actualizar(self, nombre: str, direccion: str = None, capacidad: int = None) -> None:
        """Actualiza una sede existente"""
        sede = self.buscar_por_nombre(nombre)
        if not sede:
            raise ValueError(f"Sede '{nombre}' no encontrada")
        
        sede.actualizar(direccion, capacidad)
        self._guardar_en_archivo()

    def eliminar(self, nombre: str) -> bool:
        """Elimina una sede por nombre"""
        for i, sede in enumerate(self._sedes):
            if sede.nombre.lower() == nombre.lower():
                self._sedes.pop(i)
                self._guardar_en_archivo()
                return True
        return False

    def contar_sedes(self) -> int:
        """Retorna el número total de sedes"""
        return len(self._sedes)
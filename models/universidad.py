from typing import List
from models.oferta_academica import OfertaAcademica
from models.periodo import Periodo


class Universidad:
  
    def __init__(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre de la universidad es obligatorio")

        self._nombre = nombre
        self._ofertas_academicas: List[OfertaAcademica] = []
        self._periodos: List[Periodo] = []

    @property
    def nombre(self) -> str:
        return self._nombre

    def agregar_periodo(self, periodo: Periodo):
        self._periodos.append(periodo)

    def agregar_oferta(self, oferta: OfertaAcademica):
        self._ofertas_academicas.append(oferta)

    def consultar_ofertas(self) -> list[OfertaAcademica]:
        # Se retorna una copia para evitar modificaciones externas
        return list(self._ofertas_academicas)

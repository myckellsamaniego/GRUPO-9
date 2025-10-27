class OfertaAcademica:
    def __init__(self, id_oferta, nombre_carrera, capacidad, estado):
        self._id_oferta = id_oferta
        self._nombre_carrera = nombre_carrera
        self._capacidad = capacidad
        self._estado = estado
    
    @property
    def nombre_carrera(self):
        return self._nombre_carrera
    
    def Actualizar_Cupos(self, nuevo):
        self._capacidad = nuevo
        print(f"La carrera '{self._nombre_carrera}' ahora tiene {self._capacidad} cupos disponibles.")
    
    def Consultar_Cupos(self):
        return f"{self._nombre_carrera}: {self._capacidad} cupos ({self._estado})"

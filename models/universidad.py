class Universidad:
    def __init__(self, nombre):
        self._nombre = nombre
        self._ofertas_academicas = []
        self._periodos = []
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo):
        if nuevo:
            self._nombre = nuevo
    
    def Crear_Periodo(self, periodo):
        self._periodos.append(periodo)
        print(f"Periodo '{periodo.nombre}' registrado en {self._nombre}.")
    
    def Oferta_Academica(self, oferta):
        self._ofertas_academicas.append(oferta)
        print(f"Oferta '{oferta.nombre_carrera}' agregada a la universidad {self._nombre}.")
    
    def Consultar_Ofertas(self):
        return [o.nombre_carrera for o in self._ofertas_academicas]

class OfertaAcademica:
    def __init__(self, id_oferta=None, nombre_carrera=None, capacidad=None, estado=None):
        self._id_oferta = id_oferta
        self._nombre_carrera = nombre_carrera
        self._capacidad = capacidad
        self._estado = estado
    
    @property
    def nombre_carrera(self):
        return self._nombre_carrera
    
    # FIX: Nuevo método para registrar la oferta
    def Registrar_Oferta(self):
        print("--- REGISTRO DE NUEVA OFERTA ---")
        self._nombre_carrera = input("Ingrese nombre de la carrera: ")
        self._capacidad = input("Ingrese capacidad (cupos): ")
        self._estado = input("Ingrese estado (Abierta/Cerrada): ")
        print(f"Oferta '{self._nombre_carrera}' registrada con {self._capacidad} cupos.")

    def Actualizar_Cupos(self, nuevo):
        # Aseguramos que haya un nombre para la impresión
        if self._nombre_carrera is None:
             self._nombre_carrera = "Carrera Desconocida"
             
        self._capacidad = nuevo
        print(f"La carrera '{self._nombre_carrera}' ahora tiene {self._capacidad} cupos disponibles.")
    
    def Consultar_Cupos(self):
        return f"{self._nombre_carrera}: {self._capacidad} cupos ({self._estado})"
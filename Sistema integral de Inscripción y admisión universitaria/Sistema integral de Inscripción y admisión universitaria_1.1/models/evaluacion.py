class Evaluacion:
    def __init__(self, id_evaluacion=None, fecha=None, hora=None, lugar=None, tipo=None):
        self._id_evaluacion = id_evaluacion
        self._fecha = fecha
        self._hora = hora
        self._lugar = lugar
        self._tipo = tipo 
    
    def Programar(self):
        print("--- PROGRAMAR NUEVA EVALUACIÓN ---")
        self._id_evaluacion = input("Ingrese ID de la evaluación: ")
        self._fecha = input("Ingrese Fecha (YYYY-MM-DD): ")
        self._hora = input("Ingrese Hora: ")
        self._lugar = input("Ingrese Lugar: ") 
        self._tipo = input("Ingrese Tipo (Presencial/Virtual): ")
        print(f"Evaluación {self._id_evaluacion} programada el {self._fecha} en {self._lugar}.")
    def Modificar(self):
        print(f"--- MODIFICANDO EVALUACIÓN {self._id_evaluacion} ---")
        nueva_fecha = input("Nueva Fecha (deje vacío para no cambiar): ")
        if nueva_fecha: self._fecha = nueva_fecha
        
        nueva_hora = input("Nueva Hora (deje vacío para no cambiar): ")
        if nueva_hora: self._hora = nueva_hora
        
        nuevo_lugar = input("Nuevo Lugar (deje vacío para no cambiar): ")
        if nuevo_lugar: self._lugar = nuevo_lugar
        
        nuevo_tipo = input("Nuevo Tipo (deje vacío para no cambiar): ")
        if nuevo_tipo: self._tipo = nuevo_tipo
        
        print(f"Evaluación {self._id_evaluacion} modificada correctamente. Nueva fecha: {self._fecha}")
    
    def Consultar(self):
        return f"Evaluación {self._id_evaluacion}: {self._fecha} {self._hora} en {self._lugar} ({self._tipo})"
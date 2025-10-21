class Evaluacion:
    def __init__(self, id_evaluacion, fecha, hora, lugar, tipo):
        self._id_evaluacion = id_evaluacion
        self._fecha = fecha
        self._hora = hora
        self._lugar = lugar
        self._tipo = tipo  # Presencial / Virtual
    
    def Programar(self):
        print(f"Evaluación {self._id_evaluacion} programada el {self._fecha} ({self._tipo}).")
    
    def Modificar(self, fecha=None, hora=None, lugar=None):
        if fecha: self._fecha = fecha
        if hora: self._hora = hora
        if lugar: self._lugar = lugar
        print(f"Evaluación {self._id_evaluacion} modificada correctamente.")
    
    def Consultar(self):
        return f"Evaluación {self._id_evaluacion} - {self._fecha} {self._hora} en {self._lugar} ({self._tipo})"

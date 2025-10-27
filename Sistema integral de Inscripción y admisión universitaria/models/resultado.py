class Resultado:
    def __init__(self, id_resultado, puntaje, estado, fecha_registro):
        self._id_resultado = id_resultado
        self._puntaje = puntaje
        self._estado = estado
        self._fecha_registro = fecha_registro
    
    def Generar_Resultado(self, nuevo_puntaje):
        self._puntaje = nuevo_puntaje
        print(f"Resultado {self._id_resultado} generado con puntaje {self._puntaje}.")
    
    def Mostrar_Resultado(self):
        return f"Resultado {self._id_resultado}: Puntaje {self._puntaje}, Estado {self._estado}, Fecha {self._fecha_registro}"

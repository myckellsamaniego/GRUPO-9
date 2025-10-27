class Resultado:
    def __init__(self, id_resultado=None, puntaje=None, estado=None, fecha=None):
        self._id_resultado = id_resultado
        self._puntaje = puntaje
        self._estado = estado
        self._fecha = fecha

    def Mostrar_Resultado(self):
        # Si no hay puntaje, asumimos que el objeto está vacío y damos un aviso.
        if self._puntaje is None:
            return "Aviso: No hay resultados calculados o registrados para esta consulta."
        
        # Si tiene datos, los muestra normalmente.
        return f"Resultado {self._id_resultado}: Puntaje {self._puntaje}, Estado {self._estado}, Fecha {self._fecha}"
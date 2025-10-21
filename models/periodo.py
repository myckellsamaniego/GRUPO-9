class Periodo:
    def __init__(self, id_periodo, nombre, estado, fecha_inicio, fecha_fin):
        self._id_periodo = id_periodo
        self._nombre = nombre
        self._estado = estado
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
    
    def Registrar_Tipo(self):
        print(f"Periodo '{self._nombre}' registrado con estado '{self._estado}'.")
    
    def Actualizar_Tipo(self, estado_nuevo):
        self._estado = estado_nuevo
        print(f"Periodo '{self._nombre}' actualizado a '{self._estado}'.")
    
    def __str__(self):
        return f"{self._nombre} ({self._estado}) [{self._fecha_inicio} - {self._fecha_fin}]"

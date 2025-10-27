class Periodo:
    def __init__(self, id_periodo=None, nombre=None, estado=None, fecha_inicio=None, fecha_fin=None):
        self._id_periodo = id_periodo
        self._nombre = nombre
        self._estado = estado
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
    
    def Registrar_Tipo(self):
        if self._nombre is None:
             print("Solicitando datos para registrar un nuevo período.")
             self._nombre = input("Ingrese nombre del nuevo período: ")
             self._estado = "Activo"
        print(f"Periodo '{self._nombre}' registrado con estado '{self._estado}'.")
    
    def Actualizar_Tipo(self, estado_nuevo):
        if self._nombre is None:
             print("Error: No se puede actualizar el estado sin un período existente.")
             return
        self._estado = estado_nuevo
        print(f"Periodo '{self._nombre}' actualizado a '{self._estado}'.")
    
    def __str__(self):
        return f"{self._nombre} ({self._estado}) [{self._fecha_inicio} - {self._fecha_fin}]"
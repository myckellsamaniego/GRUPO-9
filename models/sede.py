class Sede:
    def __init__(self, nombre, direccion, ciudad, capacidad):
        self._nombre = nombre
        self._direccion = direccion
        self._ciudad = ciudad
        self._capacidad = capacidad
    
    def Registrar_Sede(self):
        print(f"Sede '{self._nombre}' registrada en {self._ciudad}.")
    
    def Modificar(self, direccion=None, capacidad=None):
        if direccion:
            self._direccion = direccion
        if capacidad:
            self._capacidad = capacidad
        print(f"Sede '{self._nombre}' actualizada correctamente.")
    
    def Consultar_Sede(self):
        return f"{self._nombre} - {self._direccion}, Capacidad: {self._capacidad}"

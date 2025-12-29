class Sede:
    def __init__(self, id_sede=None, nombre=None, ciudad=None, direccion=None, estado=None):
        self._id_sede = id_sede
        self._nombre = nombre
        self._ciudad = ciudad
        self._direccion = direccion
        self._estado = estado

    def Registrar_Sede(self):
        print("--- REGISTRAR NUEVA SEDE ---")
        self._nombre = input("Ingrese nombre de la sede: ")
        self._ciudad = input("Ingrese ciudad: ")
        self._direccion = input("Ingrese dirección (opcional): ") or "N/A"
        self._estado = "Activa"
        print(f"Sede '{self._nombre}' registrada en {self._ciudad}.")

    def Modificar(self):
        # El objeto ya fue seleccionado de la lista, por lo que self._nombre ya NO es None
        print(f"--- MODIFICANDO SEDE ACTUAL: {self._nombre} en {self._ciudad} ---")

        nuevo_nombre = input(f"Nuevo nombre (actual: {self._nombre}, deje vacío para no cambiar): ")
        if nuevo_nombre:
            self._nombre = nuevo_nombre

        nueva_ciudad = input(f"Nueva ciudad (actual: {self._ciudad}, deje vacío para no cambiar): ")
        if nueva_ciudad:
            self._ciudad = nueva_ciudad
            
        nueva_direccion = input(f"Nueva dirección (actual: {self._direccion}, deje vacío para no cambiar): ")
        if nueva_direccion:
            self._direccion = nueva_direccion
            
        nuevo_estado = input(f"Nuevo estado (actual: {self._estado}, deje vacío para no cambiar): ")
        if nuevo_estado:
            self._estado = nuevo_estado

        print(f"Sede '{self._nombre}' actualizada correctamente.")
        
    def Consultar_Sede(self):
        return f"Sede: {self._nombre}, Ciudad: {self._ciudad}, Dirección: {self._direccion}, Estado: {self._estado}"
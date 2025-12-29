class Sede:
    def __init__(self, nombre: str, direccion: str, ciudad: str, capacidad: int):
        if not nombre or not ciudad:
            raise ValueError("El nombre y la ciudad de la sede son obligatorios")
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")

        self._nombre = nombre
        self._direccion = direccion
        self._ciudad = ciudad
        self._capacidad = capacidad

    @property
    def nombre(self):
        return self._nombre

    @property
    def direccion(self):
        return self._direccion

    @property
    def ciudad(self):
        return self._ciudad

    @property
    def capacidad(self):
        return self._capacidad

    def actualizar(self, direccion=None, capacidad=None):
        if direccion:
            self._direccion = direccion
        if capacidad:
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser mayor que cero")
            self._capacidad = capacidad
            
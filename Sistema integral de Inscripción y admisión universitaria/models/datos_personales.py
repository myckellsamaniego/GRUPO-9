class DatosPersonales:
    def __init__(self, nombre, apellidos, cedula, direccion, celular, correo, etnia, discapacidad):
        self._nombre = nombre
        self._apellidos = apellidos
        self._cedula = cedula
        self._direccion = direccion
        self._celular = celular
        self._correo = correo
        self._etnia = etnia
        self._discapacidad = discapacidad

    def Registrar(self):
        print(f"Registrando datos personales de {self._nombre} {self._apellidos}")

    def Actualizar(self):
        print(f"Actualizando datos de {self._nombre}")

    def Consultar(self):
        return (
            f"{self._nombre} {self._apellidos}, Cédula: {self._cedula}, "
            f"Dirección: {self._direccion}, Correo: {self._correo}, Etnia: {self._etnia}, "
            f"Discapacidad: {self._discapacidad}"
        )

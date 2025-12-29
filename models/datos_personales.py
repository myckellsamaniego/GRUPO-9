class DatosPersonales:
    def __init__(
        self,
        nombre: str,
        apellidos: str,
        cedula: str,
        direccion: str,
        celular: str,
        correo: str,
        etnia: str,
        discapacidad: bool
    ):
        if not nombre or not apellidos:
            raise ValueError("El nombre y apellidos son obligatorios")

        if not cedula:
            raise ValueError("La cédula es obligatoria")

        if not correo:
            raise ValueError("El correo es obligatorio")

        self._nombre = nombre
        self._apellidos = apellidos
        self._cedula = cedula
        self._direccion = direccion
        self._celular = celular
        self._correo = correo
        self._etnia = etnia
        self._discapacidad = discapacidad

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellidos(self):
        return self._apellidos

    @property
    def cedula(self):
        return self._cedula

    @property
    def direccion(self):
        return self._direccion

    @property
    def celular(self):
        return self._celular

    @property
    def correo(self):
        return self._correo

    @property
    def etnia(self):
        return self._etnia

    @property
    def discapacidad(self):
        return self._discapacidad

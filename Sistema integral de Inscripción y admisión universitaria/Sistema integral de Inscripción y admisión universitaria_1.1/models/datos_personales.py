class DatosPersonales:
    def __init__(self, nombre=None, apellidos=None, cedula=None, direccion=None, celular=None, correo=None, etnia=None, discapacidad=None):
        self._nombre = nombre
        self._apellidos = apellidos
        self._cedula = cedula
        self._direccion = direccion
        self._celular = celular
        self._correo = correo
        self._etnia = etnia
        self._discapacidad = discapacidad

    def Registrar(self):
        print("\n--- REGISTRO DE DATOS PERSONALES ---")
        self._nombre = input("Ingrese su(s) nombre(s): ")
        self._apellidos = input("Ingrese su(s) apellido(s): ")
        self._cedula = input("Ingrese su número de cédula: ")
        self._direccion = input("Ingrese su dirección: ")
        self._celular = input("Ingrese su número de celular: ")
        self._correo = input("Ingrese su correo electrónico: ")
        self._etnia = input("Ingrese su etnia: ")
        self._discapacidad = input("¿Tiene alguna discapacidad? (Sí/No): ")
        
        print(f"Datos personales registrados para: {self._nombre} {self._apellidos}.")

    def Actualizar(self):
        print(f"--- ACTUALIZANDO DATOS DE {self._nombre} {self._apellidos} ---")
        self._direccion = input(f"Nueva dirección (actual: {self._direccion}): ") or self._direccion
        self._celular = input(f"Nuevo celular (actual: {self._celular}): ") or self._celular
        print(f"Datos de {self._nombre} actualizados.")

    def Consultar(self):
        if self._nombre is None:
            return "Aviso: No se han registrado datos personales."
        
        return (
            f"DATOS PERSONALES REGISTRADOS:\n"
            f"  Nombre completo: {self._nombre} {self._apellidos}\n"
            f"  Cédula: {self._cedula}\n"
            f"  Contacto: {self._celular} ({self._correo})\n"
            f"  Ubicación: {self._direccion}\n"
            f"  Etnia: {self._etnia}\n"
            f"  Discapacidad: {self._discapacidad}"
        )
from models.usuario import Usuario

class Postulante(Usuario):
    def __init__(self, nombre, usuario, correo, clave):
        super().__init__(nombre, correo, clave)
        self._usuario = usuario
        
    @property 
    def usuario(self):
        return self._usuario
    
    @usuario.setter
    def usuario(self, nuevo):
        self._usuario = nuevo
        
    def Realizar_Inscripcion(self):
        print(f"{self._usuario} ha realizado una inscripción.")
        
    def Consultar_Inscripcion(self):
        print(f"{self._usuario} está consultando su inscripción.")
    
    def mostrar_informacion(self):
        return (
            f"Nombres: {self.nombres}, Usuario: {self._usuario}\n"
            f"Correo: {self.correo}, Contraseña: {self.clave}\n"
        )
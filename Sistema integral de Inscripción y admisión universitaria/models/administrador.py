from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, adminID, nombre, correo, clave):
        super().__init__(nombre, correo, clave)
        self._adminID = adminID
        
    @property    
    def adminID(self):
        return self._adminID
    
    @adminID.setter
    def adminID(self, nuevo):
        self._adminID = nuevo
        
    def Gestionar_Usuarios(self):
        print(f"Administrador {self._nombre} está gestionando usuarios.")
        
    def Gestionar_Evaluaciones(self):
        print(f"Administrador {self._nombre} está gestionando evaluaciones.")
        
    def Validar_Postulacion(self):
        print(f"Administrador {self._nombre} está validando postulaciones.")
    
    def mostrar_informacion(self):
        return (
            f"Nombres: {self.nombre}, ID: {self._adminID}\n"
            f"Correo: {self.correo}, Rol: {self.rol}\n"
        )

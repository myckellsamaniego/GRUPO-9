class UsuarioRepository:
    def __init__(self):
        
        self._usuarios = []

    def agregar(self, usuario):
        self._usuarios.append(usuario)

    def buscar_por_correo(self, correo):
        for u in self._usuarios:
            if u.correo == correo:
                return u
        return None

import json
import os
from factory.fabrica_usuarios import FabricaUsuarios


class UsuarioRepositoryJSON:
    """
    REPOSITORY CONCRETO (JSON)
    """

    def __init__(self, archivo="usuarios.json"):
        self._archivo = archivo
        self._fabrica = FabricaUsuarios()

        if not os.path.exists(self._archivo):
            self._crear_archivo_con_admin()


    def _leer(self):
        with open(self._archivo, "r") as f:
            return json.load(f)

    def _guardar(self, data):
        with open(self._archivo, "w") as f:
            json.dump(data, f, indent=4)

    def agregar(self, usuario):
        usuarios = self._leer()

        if any(u["correo"] == usuario.correo for u in usuarios):
            raise ValueError("El usuario ya existe")

        usuarios.append(self._usuario_a_dict(usuario))
        self._guardar(usuarios)

    def buscar_por_correo(self, correo):
        usuarios = self._leer()

        for u in usuarios:
            if u["correo"] == correo:
                return self._fabrica.crear_desde_dict(u)

        return None

    def listar(self):
        return [
            self._fabrica.crear_desde_dict(u)
            for u in self._leer()
        ]

    def _usuario_a_dict(self, usuario):
        if usuario.obtener_tipo() == "Administrador":
            return {
                "tipo": "ADMIN",
                "identificacion": usuario.identificacion,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "password": usuario.password,
                "admin_id": usuario.admin_id
            }

        if usuario.obtener_tipo() == "Postulante":
            return {
                "tipo": "POSTULANTE",
                "correo": usuario.correo,
                "password": usuario.password,
                "datos_personales": None
            }

        raise ValueError("Tipo de usuario no soportado")
    
    def _crear_archivo_con_admin(self):
        """
        Inicializa el sistema con un administrador por defecto.
        Esto simula un sistema real donde el admin ya existe.
        """

        admin_inicial = [
            {
                "tipo": "ADMIN",
                "identificacion": "ADM001",
                "nombre": "Administrador Principal",
                "correo": "admin@uleam.edu.ec",
                "password": "admin123",
                "admin_id": "ADMIN-001"
            }
        ]   

        with open(self._archivo, "w") as f:
            json.dump(admin_inicial, f, indent=4)


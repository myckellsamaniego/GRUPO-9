import json
import os
from repository.usuario_repository import UsuarioRepository
from factory.fabrica_usuarios import FabricaUsuarios


class UsuarioRepositoryJSON(UsuarioRepository):
    """
    REPOSITORY CONCRETO (JSON)
    Implementación del repositorio de usuarios con persistencia en JSON
    """

    def __init__(self, archivo="usuarios.json"):
        self._archivo = archivo
        self._fabrica = FabricaUsuarios()

        if not os.path.exists(self._archivo):
            self._crear_archivo_con_admin()

    def _leer(self):
        """Lee el archivo JSON"""
        with open(self._archivo, "r", encoding='utf-8') as f:
            return json.load(f)

    def _guardar(self, data):
        """Guarda datos en el archivo JSON"""
        with open(self._archivo, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def agregar(self, usuario):
        """
        Agrega un nuevo usuario al sistema
        
        Args:
            usuario: Instancia de Usuario (Postulante o Administrador)
            
        Raises:
            ValueError: Si el usuario ya existe
        """
        usuarios = self._leer()

        # Verificar si el correo ya existe
        if any(u["correo"] == usuario.correo for u in usuarios):
            raise ValueError("El usuario ya existe")

        usuarios.append(self._usuario_a_dict(usuario))
        self._guardar(usuarios)

    def buscar_por_correo(self, correo):
        """
        Busca un usuario por su correo electrónico
        
        Args:
            correo: Correo electrónico del usuario
            
        Returns:
            Instancia de Usuario o None si no existe
        """
        usuarios = self._leer()

        for u in usuarios:
            if u["correo"] == correo:
                return self._fabrica.crear_desde_dict(u)

        return None

    def listar(self):
        """
        Lista todos los usuarios del sistema
        
        Returns:
            Lista de instancias de Usuario
        """
        return [
            self._fabrica.crear_desde_dict(u)
            for u in self._leer()
        ]

    def _usuario_a_dict(self, usuario):
        """
        Convierte un usuario a diccionario para persistencia
        
        Args:
            usuario: Instancia de Usuario
            
        Returns:
            Diccionario con los datos del usuario
            
        Raises:
            ValueError: Si el tipo de usuario no es soportado
        """
        tipo = usuario.obtener_tipo()
        
        if tipo == "ADMIN":
            return {
                "tipo": "ADMIN",
                "identificacion": usuario.identificacion,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "password": usuario.password,
                "admin_id": usuario.admin_id
            }

        elif tipo == "Postulante":
            return {
                "tipo": "POSTULANTE",
                "correo": usuario.correo,
                "password": usuario.password,
                "datos_personales": usuario.datos_personales.to_dict()
            }

        else:
            raise ValueError(f"Tipo de usuario no soportado: {tipo}")
    
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

        with open(self._archivo, "w", encoding='utf-8') as f:
            json.dump(admin_inicial, f, indent=4, ensure_ascii=False)

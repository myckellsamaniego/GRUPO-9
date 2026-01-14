"""
Repositorio de Usuarios - Persistencia en JSON
"""
import json
import os
from typing import List, Optional
from factory.fabrica_usuarios import FabricaUsuarios


class UsuarioRepositoryJSON:
    """
    Repositorio para gestionar usuarios del sistema
    Almacena en archivo JSON
    """

    def __init__(self, archivo: str = "data/usuarios.json"):
        self.archivo = archivo
        self.fabrica = FabricaUsuarios()
        self._usuarios = []
        self._cargar_desde_archivo()

    def _cargar_desde_archivo(self):
        """Carga usuarios desde el archivo JSON"""
        if not os.path.exists(self.archivo):
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            self._usuarios = []
            return
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self._usuarios = [
                    self.fabrica.crear_desde_dict(d) 
                    for d in datos
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self._usuarios = []

    def _guardar_en_archivo(self):
        """Guarda usuarios en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        
        datos = []
        for usuario in self._usuarios:
            if hasattr(usuario, 'to_dict'):
                datos.append(usuario.to_dict())
            else:
                # Si no tiene to_dict, construir manualmente
                if usuario.obtener_tipo() == "ADMIN":
                    datos.append({
                        "tipo": "ADMIN",
                        "correo": usuario.correo,
                        "password": usuario.password,
                        "identificacion": usuario.identificacion,
                        "nombre": usuario.nombre,
                        "admin_id": usuario.admin_id
                    })
                else:  # Postulante
                    datos.append({
                        "tipo": "POSTULANTE",
                        "correo": usuario.correo,
                        "password": usuario.password,
                        "datos_personales": usuario.datos_personales.to_dict()
                    })
        
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def agregar(self, usuario) -> None:
        """
        Agrega un usuario al repositorio
        
        Args:
            usuario: Usuario a agregar (Postulante o Administrador)
        """
        # Verificar que no exista el correo
        if self.buscar_por_correo(usuario.correo):
            raise ValueError(f"Ya existe un usuario con el correo {usuario.correo}")
        
        self._usuarios.append(usuario)
        self._guardar_en_archivo()

    def buscar_por_correo(self, correo: str):
        """
        Busca un usuario por su correo electrónico
        
        Args:
            correo: Correo del usuario
            
        Returns:
            Usuario encontrado o None
        """
        for usuario in self._usuarios:
            if usuario.correo == correo:
                return usuario
        return None

    def buscar_por_cedula(self, cedula: str):
        """
        Busca un postulante por su cédula
        
        Args:
            cedula: Cédula del postulante
            
        Returns:
            Postulante encontrado o None
        """
        for usuario in self._usuarios:
            if usuario.obtener_tipo() == "POSTULANTE":
                if usuario.datos_personales.cedula == cedula:
                    return usuario
        return None

    def listar_todos(self) -> List:
        """
        Retorna todos los usuarios
        
        Returns:
            Lista de usuarios
        """
        return list(self._usuarios)

    def listar_postulantes(self) -> List:
        """
        Retorna solo los postulantes
        
        Returns:
            Lista de postulantes
        """
        return [
            u for u in self._usuarios 
            if u.obtener_tipo() == "POSTULANTE"
        ]

    def listar_administradores(self) -> List:
        """
        Retorna solo los administradores
        
        Returns:
            Lista de administradores
        """
        return [
            u for u in self._usuarios 
            if u.obtener_tipo() == "ADMIN"
        ]

    def actualizar(self, usuario) -> None:
        """
        Actualiza un usuario existente
        
        Args:
            usuario: Usuario con datos actualizados
        """
        for i, u in enumerate(self._usuarios):
            if u.correo == usuario.correo:
                self._usuarios[i] = usuario
                self._guardar_en_archivo()
                return
        
        raise ValueError(f"Usuario {usuario.correo} no encontrado")

    def eliminar(self, correo: str) -> bool:
        """
        Elimina un usuario por su correo
        
        Args:
            correo: Correo del usuario a eliminar
            
        Returns:
            True si se eliminó, False si no se encontró
        """
        for i, u in enumerate(self._usuarios):
            if u.correo == correo:
                self._usuarios.pop(i)
                self._guardar_en_archivo()
                return True
        return False

    def existe_cedula(self, cedula: str) -> bool:
        """
        Verifica si existe un postulante con esa cédula
        
        Args:
            cedula: Cédula a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.buscar_por_cedula(cedula) is not None
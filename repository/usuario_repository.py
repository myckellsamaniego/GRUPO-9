"""
Repositorio de Usuarios - Maneja la persistencia de usuarios en JSON
"""
import json
import os
from models.datos_personales import DatosPersonales
from models.datos_personales_completos import DatosPersonalesCompletos
from models.postulante import Postulante
from models.administrador import Administrador


class UsuarioRepositoryJSON:
    """Repositorio para gestionar usuarios en archivo JSON"""
    
    def __init__(self, archivo='data/usuarios.json'):
        self.archivo = archivo
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        # Cargar usuarios existentes
        self.usuarios = self._cargar()
    
    def agregar(self, usuario):
        """Agrega un nuevo usuario al repositorio"""
        # Verificar que no exista ya
        if self.buscar_por_correo(usuario.correo):
            raise ValueError(f"Ya existe un usuario con el correo {usuario.correo}")
        
        if hasattr(usuario, 'datos_personales') and self.existe_cedula(usuario.datos_personales.cedula):
            raise ValueError(f"Ya existe un usuario con la cédula {usuario.datos_personales.cedula}")
        
        self.usuarios.append(usuario)
        self._guardar()
    
    def actualizar(self, usuario):
        """Actualiza un usuario existente en el repositorio"""
        # Buscar el índice del usuario por cédula
        for i, u in enumerate(self.usuarios):
            if hasattr(u, 'datos_personales') and hasattr(usuario, 'datos_personales'):
                if u.datos_personales.cedula == usuario.datos_personales.cedula:
                    # Actualizar el usuario en la lista
                    self.usuarios[i] = usuario
                    # Guardar cambios
                    self._guardar()
                    return True
        
        # Si no se encuentra, lanzar excepción
        raise ValueError(f"Usuario con cédula {usuario.datos_personales.cedula} no encontrado")
    
    def buscar_por_correo(self, correo):
        """Busca un usuario por su correo electrónico"""
        for usuario in self.usuarios:
            if usuario.correo == correo:
                return usuario
        return None
    
    def buscar_por_cedula(self, cedula):
        """Busca un usuario por su cédula"""
        for usuario in self.usuarios:
            if hasattr(usuario, 'datos_personales'):
                if usuario.datos_personales.cedula == cedula:
                    return usuario
        return None
    
    def existe_cedula(self, cedula):
        """Verifica si existe un usuario con la cédula dada"""
        return self.buscar_por_cedula(cedula) is not None
    
    def listar(self):
        """Retorna todos los usuarios"""
        return self.usuarios
    
    def eliminar(self, correo):
        """Elimina un usuario por su correo"""
        for i, usuario in enumerate(self.usuarios):
            if usuario.correo == correo:
                del self.usuarios[i]
                self._guardar()
                return True
        return False
    
    def _cargar(self):
        """Carga los usuarios desde el archivo JSON"""
        if not os.path.exists(self.archivo):
            return []
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            usuarios = []
            for item in datos:
                tipo = item.get('tipo')
                
                if tipo == 'POSTULANTE':
                    # Determinar si son datos completos o básicos
                    datos_personales_dict = item['datos_personales']
                    
                    # Si tiene fecha_nacimiento, es DatosPersonalesCompletos
                    if 'fecha_nacimiento' in datos_personales_dict and datos_personales_dict['fecha_nacimiento']:
                        datos_personales = DatosPersonalesCompletos.from_dict(datos_personales_dict)
                    else:
                        # Es DatosPersonales básico
                        datos_personales = DatosPersonales.from_dict(datos_personales_dict)
                    
                    usuario = Postulante(
                        correo=item['correo'],
                        password=item['password'],
                        datos_personales=datos_personales
                    )
                    usuarios.append(usuario)
                
                elif tipo == 'ADMIN':
                    usuario = Administrador(
                        correo=item['correo'],
                        password=item['password'],
                        identificacion=item['identificacion'],
                        nombre=item['nombre'],
                        admin_id=item['admin_id']
                    )
                    usuarios.append(usuario)
            
            return usuarios
        
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _guardar(self):
        """Guarda los usuarios en el archivo JSON"""
        try:
            datos = []
            for usuario in self.usuarios:
                usuario_dict = {
                    'tipo': usuario.obtener_tipo(),
                    'correo': usuario.correo,
                    'password': usuario.password
                }
                
                # Si es postulante, agregar datos personales
                if hasattr(usuario, 'datos_personales'):
                    usuario_dict['datos_personales'] = usuario.datos_personales.to_dict()
                
                # Si es administrador, agregar campos específicos
                if hasattr(usuario, 'admin_id'):
                    usuario_dict['admin_id'] = usuario.admin_id
                    usuario_dict['identificacion'] = usuario.identificacion
                    usuario_dict['nombre'] = usuario.nombre
                
                datos.append(usuario_dict)
            
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
            import traceback
            traceback.print_exc()
            return False
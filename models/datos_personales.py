"""
Modelo extendido de Datos Personales con toda la información del formulario completo
"""
from datetime import date


class DatosPersonalesCompletos:
    """
    Clase que almacena toda la información personal del postulante
    según el formulario completo del sistema de admisión
    """
    
    def __init__(
        self,
        # PASO 1: Identificación
        nombre: str,
        apellidos: str,
        cedula: str,
        fecha_nacimiento: date,
        estado_civil: str,
        sexo: str,
        identidad_genero: str,
        
        # PASO 2: Referencia-Contactos
        correo: str,
        celular: str = "",
        provincia: str = "",
        canton: str = "",
        parroquia: str = "",
        barrio: str = "",
        calle_principal: str = "",
        calle_secundaria: str = "",
        numero_casa: str = "",
        
        # PASO 3: Autoidentificación étnica
        etnia: str = "",
        
        # PASO 4: Discapacidad
        discapacidad: bool = False,
        requiere_apoyo_evaluacion: bool = False,
        
        # PASO 5: Información Tecnológica
        internet_domicilio: bool = False,
        computadora_funcional: bool = False,
        sistema_operativo: str = "",
        camara_web: bool = False,
        
        # PASO 6: Educación
        orientacion_vocacional: bool = False,
        institucion_aspirar: str = "",
        nivel_maximo_estudios: str = "",
        razon_estudiar_carrera: str = ""
    ):
        # Validaciones básicas
        if not nombre or not apellidos:
            raise ValueError("El nombre y apellidos son obligatorios")
        if not cedula:
            raise ValueError("La cédula es obligatoria")
        if not correo:
            raise ValueError("El correo es obligatorio")
        
        # PASO 1: Identificación
        self._nombre = nombre
        self._apellidos = apellidos
        self._cedula = cedula
        self._fecha_nacimiento = fecha_nacimiento
        self._estado_civil = estado_civil
        self._sexo = sexo
        self._identidad_genero = identidad_genero
        
        # PASO 2: Referencia-Contactos
        self._correo = correo
        self._celular = celular
        self._provincia = provincia
        self._canton = canton
        self._parroquia = parroquia
        self._barrio = barrio
        self._calle_principal = calle_principal
        self._calle_secundaria = calle_secundaria
        self._numero_casa = numero_casa
        
        # PASO 3: Autoidentificación étnica
        self._etnia = etnia
        
        # PASO 4: Discapacidad
        self._discapacidad = discapacidad
        self._requiere_apoyo_evaluacion = requiere_apoyo_evaluacion
        
        # PASO 5: Información Tecnológica
        self._internet_domicilio = internet_domicilio
        self._computadora_funcional = computadora_funcional
        self._sistema_operativo = sistema_operativo
        self._camara_web = camara_web
        
        # PASO 6: Educación
        self._orientacion_vocacional = orientacion_vocacional
        self._institucion_aspirar = institucion_aspirar
        self._nivel_maximo_estudios = nivel_maximo_estudios
        self._razon_estudiar_carrera = razon_estudiar_carrera
    
    # ========== PROPIEDADES ==========
    
    # Paso 1
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
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    
    @property
    def estado_civil(self):
        return self._estado_civil
    
    @property
    def sexo(self):
        return self._sexo
    
    @property
    def identidad_genero(self):
        return self._identidad_genero
    
    # Paso 2
    @property
    def correo(self):
        return self._correo
    
    @property
    def celular(self):
        return self._celular
    
    @property
    def provincia(self):
        return self._provincia
    
    @property
    def canton(self):
        return self._canton
    
    @property
    def parroquia(self):
        return self._parroquia
    
    @property
    def barrio(self):
        return self._barrio
    
    @property
    def calle_principal(self):
        return self._calle_principal
    
    @property
    def calle_secundaria(self):
        return self._calle_secundaria
    
    @property
    def numero_casa(self):
        return self._numero_casa
    
    @property
    def direccion(self):
        """Genera la dirección completa"""
        partes = []
        if self._calle_principal:
            partes.append(self._calle_principal)
        if self._calle_secundaria:
            partes.append(f"y {self._calle_secundaria}")
        if self._numero_casa:
            partes.append(f"#{self._numero_casa}")
        if self._barrio:
            partes.append(f"- {self._barrio}")
        return " ".join(partes) if partes else ""
    
    # Paso 3
    @property
    def etnia(self):
        return self._etnia
    
    # Paso 4
    @property
    def discapacidad(self):
        return self._discapacidad
    
    @property
    def requiere_apoyo_evaluacion(self):
        return self._requiere_apoyo_evaluacion
    
    # Paso 5
    @property
    def internet_domicilio(self):
        return self._internet_domicilio
    
    @property
    def computadora_funcional(self):
        return self._computadora_funcional
    
    @property
    def sistema_operativo(self):
        return self._sistema_operativo
    
    @property
    def camara_web(self):
        return self._camara_web
    
    # Paso 6
    @property
    def orientacion_vocacional(self):
        return self._orientacion_vocacional
    
    @property
    def institucion_aspirar(self):
        return self._institucion_aspirar
    
    @property
    def nivel_maximo_estudios(self):
        return self._nivel_maximo_estudios
    
    @property
    def razon_estudiar_carrera(self):
        return self._razon_estudiar_carrera
    
    # ========== MÉTODOS ==========
    
    def datos_obligatorios_completos(self) -> bool:
        """Verifica que los datos obligatorios estén completos"""
        return all([
            self._nombre,
            self._apellidos,
            self._cedula,
            self._correo,
            self._fecha_nacimiento,
            self._estado_civil,
            self._sexo
        ])
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para persistencia"""
        return {
            # Paso 1
            "nombre": self._nombre,
            "apellidos": self._apellidos,
            "cedula": self._cedula,
            "fecha_nacimiento": self._fecha_nacimiento.isoformat() if isinstance(self._fecha_nacimiento, date) else str(self._fecha_nacimiento),
            "estado_civil": self._estado_civil,
            "sexo": self._sexo,
            "identidad_genero": self._identidad_genero,
            
            # Paso 2
            "correo": self._correo,
            "celular": self._celular,
            "provincia": self._provincia,
            "canton": self._canton,
            "parroquia": self._parroquia,
            "barrio": self._barrio,
            "calle_principal": self._calle_principal,
            "calle_secundaria": self._calle_secundaria,
            "numero_casa": self._numero_casa,
            "direccion": self.direccion,
            
            # Paso 3
            "etnia": self._etnia,
            
            # Paso 4
            "discapacidad": self._discapacidad,
            "requiere_apoyo_evaluacion": self._requiere_apoyo_evaluacion,
            
            # Paso 5
            "internet_domicilio": self._internet_domicilio,
            "computadora_funcional": self._computadora_funcional,
            "sistema_operativo": self._sistema_operativo,
            "camara_web": self._camara_web,
            
            # Paso 6
            "orientacion_vocacional": self._orientacion_vocacional,
            "institucion_aspirar": self._institucion_aspirar,
            "nivel_maximo_estudios": self._nivel_maximo_estudios,
            "razon_estudiar_carrera": self._razon_estudiar_carrera
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Reconstruye DatosPersonalesCompletos desde JSON"""
        from datetime import datetime
        
        # Convertir fecha si es string
        fecha_nac = data.get("fecha_nacimiento")
        if isinstance(fecha_nac, str):
            fecha_nac = datetime.fromisoformat(fecha_nac).date()
        
        return DatosPersonalesCompletos(
            # Paso 1
            nombre=data["nombre"],
            apellidos=data["apellidos"],
            cedula=data["cedula"],
            fecha_nacimiento=fecha_nac,
            estado_civil=data.get("estado_civil", ""),
            sexo=data.get("sexo", ""),
            identidad_genero=data.get("identidad_genero", ""),
            
            # Paso 2
            correo=data["correo"],
            celular=data.get("celular", ""),
            provincia=data.get("provincia", ""),
            canton=data.get("canton", ""),
            parroquia=data.get("parroquia", ""),
            barrio=data.get("barrio", ""),
            calle_principal=data.get("calle_principal", ""),
            calle_secundaria=data.get("calle_secundaria", ""),
            numero_casa=data.get("numero_casa", ""),
            
            # Paso 3
            etnia=data.get("etnia", ""),
            
            # Paso 4
            discapacidad=data.get("discapacidad", False),
            requiere_apoyo_evaluacion=data.get("requiere_apoyo_evaluacion", False),
            
            # Paso 5
            internet_domicilio=data.get("internet_domicilio", False),
            computadora_funcional=data.get("computadora_funcional", False),
            sistema_operativo=data.get("sistema_operativo", ""),
            camara_web=data.get("camara_web", False),
            
            # Paso 6
            orientacion_vocacional=data.get("orientacion_vocacional", False),
            institucion_aspirar=data.get("institucion_aspirar", ""),
            nivel_maximo_estudios=data.get("nivel_maximo_estudios", ""),
            razon_estudiar_carrera=data.get("razon_estudiar_carrera", "")
        )
    
    def __str__(self):
        return f"{self._nombre} {self._apellidos} ({self._cedula})"
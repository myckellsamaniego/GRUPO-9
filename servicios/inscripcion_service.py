from excepciones.errores_inscripcion import InscripcionDuplicadaError, CuposAgotadosError

class InscripcionService:
    """
    Servicio que maneja la lógica de negocio de las inscripciones
    """

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def registrar(self, inscripcion):
        """
        Registra una nueva inscripción después de validaciones
        """
        # 1. Verificar duplicados
        cedula = inscripcion.postulante.datos_personales.cedula
        existente = self._repositorio.buscar_por_cedula(cedula)

        if existente:
            raise InscripcionDuplicadaError(
                "El postulante ya tiene una inscripción registrada"
            )

        # 2. Verificar cupos disponibles
        if not inscripcion.oferta.hay_cupos():
            raise CuposAgotadosError(
                f"No hay cupos disponibles para {inscripcion.oferta.nombre}"
            )

        # 3. Ocupar un cupo
        inscripcion.oferta.ocupar_cupo()

        # 4. Guardar la inscripción
        self._repositorio.guardar(inscripcion)

        return inscripcion

    def listar(self):
        """Lista todas las inscripciones"""
        return self._repositorio.listar()

    def buscar_por_cedula(self, cedula: str):
        """Busca inscripción por cédula del postulante"""
        return self._repositorio.buscar_por_cedula(cedula)

    def aprobar_inscripcion(self, cedula: str):
        """
        Aprueba una inscripción pendiente
        
        Args:
            cedula: Cédula del postulante
            
        Returns:
            Inscripción aprobada
            
        Raises:
            ValueError: Si la inscripción no existe o no está pendiente
        """
        # Buscar inscripción (retorna dict del JSON)
        inscripcion_dict = self._repositorio.buscar_por_cedula(cedula)
        
        if not inscripcion_dict:
            raise ValueError("Inscripción no encontrada")
        
        if inscripcion_dict["estado_inscripcion"] != "PENDIENTE":
            raise ValueError("Solo se pueden aprobar inscripciones pendientes")
        
        # Actualizar estado en el diccionario
        inscripcion_dict["estado_inscripcion"] = "APROBADA"
        
        # Guardar cambios
        self._repositorio.actualizar_dict(cedula, inscripcion_dict)
        
        return inscripcion_dict

    def rechazar_inscripcion(self, cedula: str):
        """
        Rechaza una inscripción pendiente
        
        Args:
            cedula: Cédula del postulante
            
        Returns:
            Inscripción rechazada
            
        Raises:
            ValueError: Si la inscripción no existe o no está pendiente
        """
        # Buscar inscripción
        inscripcion_dict = self._repositorio.buscar_por_cedula(cedula)
        
        if not inscripcion_dict:
            raise ValueError("Inscripción no encontrada")
        
        if inscripcion_dict["estado_inscripcion"] != "PENDIENTE":
            raise ValueError("Solo se pueden rechazar inscripciones pendientes")
        
        # Actualizar estado
        inscripcion_dict["estado_inscripcion"] = "RECHAZADA"
        
        # Guardar cambios
        self._repositorio.actualizar_dict(cedula, inscripcion_dict)
        
        return inscripcion_dict

    def listar_por_estado(self, estado: str):
        """Lista inscripciones por estado específico"""
        todas = self.listar()
        return [i for i in todas if i["estado_inscripcion"] == estado]
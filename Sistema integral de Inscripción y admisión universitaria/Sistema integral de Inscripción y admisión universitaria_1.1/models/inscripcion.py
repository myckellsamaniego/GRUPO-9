class Inscripcion:
    # FIX: Se añaden valores por defecto.
    def __init__(self, id_inscripcion=None, fecha=None, modalidad=None, periodo=None):
        self._id_inscripcion = id_inscripcion
        self._fecha = fecha
        self._modalidad = modalidad 
        self._periodo = periodo
    
    def Crear_Inscripcion(self):
        if self._id_inscripcion is None:
             self._id_inscripcion = "INS001"
             self._modalidad = "Matutino"
        print(f"Inscripción {self._id_inscripcion} creada en modalidad {self._modalidad}.")
    
    def Modificar(self, modalidad=None):
        if modalidad:
            self._modalidad = modalidad
        print(f"Inscripción {self._id_inscripcion} modificada correctamente.")
    
    def Cancelar(self):
        print(f"Inscripción {self._id_inscripcion} ha sido cancelada.")
    
    def Consultar(self):
        return f"Inscripción {self._id_inscripcion} - {self._modalidad} ({'Periodo Actual' if self._periodo is None else self._periodo.nombre})"
    
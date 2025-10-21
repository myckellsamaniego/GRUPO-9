class Inscripcion:
    def __init__(self, id_inscripcion, fecha, modalidad, periodo):
        self._id_inscripcion = id_inscripcion
        self._fecha = fecha
        self._modalidad = modalidad  # Matutino/Vespertino
        self._periodo = periodo
    
    def Crear_Inscripcion(self):
        print(f"Inscripción {self._id_inscripcion} creada en modalidad {self._modalidad}.")
    
    def Modificar(self, modalidad=None):
        if modalidad:
            self._modalidad = modalidad
        print(f"Inscripción {self._id_inscripcion} modificada correctamente.")
    
    def Cancelar(self):
        print(f"Inscripción {self._id_inscripcion} ha sido cancelada.")
    
    def Consultar(self):
        return f"Inscripción {self._id_inscripcion} - {self._modalidad} ({self._periodo.nombre})"

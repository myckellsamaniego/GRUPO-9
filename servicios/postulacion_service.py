from factory.validador_factory import ValidadorFactory
from models.postulacion import Postulacion


class PostulacionService:
    """
    Orquesta el proceso completo de postulación al examen.
    """

    def __init__(self, repositorio_postulaciones):
        self._repositorio_postulaciones = repositorio_postulaciones

    def postular(self, inscripcion, periodo):
        #  Construir contexto
        contexto = {
            "inscripcion": inscripcion,
            "periodo": periodo,
            "repositorio_postulaciones": self._repositorio_postulaciones
        }

        #  Validar reglas del proceso
        validador = ValidadorFactory.crear_validador_postulacion()
        validador.validar(contexto)

        #  Crear la postulación
        postulacion = Postulacion(inscripcion, periodo)

        #  Persistir
        self._repositorio_postulaciones.guardar(postulacion)

        return postulacion

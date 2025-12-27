from models.postulante import Postulante
from models.oferta_academica import OfertaAcademica
from models.inscripcion import Inscripcion

from factory.validador_factory import ValidadorFactory
from repository.inscripcion_repository_memoria import InscripcionRepositoryMemoria
from servicios.inscripcion_service import InscripcionService


def main():
    postulante = Postulante("0102030405", "Juan Pérez", 8.5)
    oferta = OfertaAcademica("TI-01", "Tecnologías de la Información", 2)

    validador = ValidadorFactory.crear_validador("regular")

    inscripcion = Inscripcion(postulante, oferta, validador)

    repositorio = InscripcionRepositoryMemoria()
    servicio = InscripcionService(repositorio)

    servicio.registrar(inscripcion)

    print("Inscripción aprobada:", inscripcion.aprobada)
    print("Cupos restantes:", oferta.cupos)


if __name__ == "__main__":
    main()

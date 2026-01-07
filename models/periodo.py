from datetime import date

class Periodo:

    ESTADOS_VALIDOS = ("PLANIFICADO", "ACTIVO", "CERRADO")

    def __init__(
        self,
        id_periodo: str,
        nombre: str,
        estado: str,
        fecha_inicio: date,
        fecha_fin: date
    ):
        if not id_periodo:
            raise ValueError("El id del periodo es obligatorio")

        if not nombre:
            raise ValueError("El nombre del periodo es obligatorio")

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de periodo no válido")

        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")

        self._id_periodo = id_periodo
        self._nombre = nombre
        self._estado = estado
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin

    @property
    def id_periodo(self) -> str:
        return self._id_periodo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def fecha_inicio(self) -> date:
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> date:
        return self._fecha_fin

    def cambiar_estado(self, nuevo_estado: str):
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado no permitido")

        self._estado = nuevo_estado

    def __str__(self):
        return f"{self._nombre} ({self._estado}) [{self._fecha_inicio} - {self._fecha_fin}]"

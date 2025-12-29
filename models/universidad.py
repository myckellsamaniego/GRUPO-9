class Universidad:
    def __init__(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre de la universidad es obligatorio")

        self._nombre = nombre
        self._ofertas_academicas = []
        self._periodos = []

    @property
    def nombre(self):
        return self._nombre

    def agregar_periodo(self, periodo):
        self._periodos.append(periodo)

    def agregar_oferta(self, oferta):
        self._ofertas_academicas.append(oferta)

    def consultar_ofertas(self):
        return self._ofertas_academicas

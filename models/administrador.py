from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, identificacion: str, nombre: str, admin_id: str):
        super().__init__(identificacion, nombre)

        if not admin_id:
            raise ValueError("El ID del administrador es obligatorio")

        self._admin_id = admin_id

    @property
    def admin_id(self):
        return self._admin_id

    def autorizar_periodo(self, periodo) -> bool:
        """
        Autoriza la activación de un periodo de admisión.
        """
        return True

    def obtener_tipo(self) -> str:
        return "Administrador"

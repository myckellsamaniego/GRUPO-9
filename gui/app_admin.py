"""
GUI del Administrador - Sistema de Admisión
"""
import tkinter as tk
from tkinter import ttk, messagebox

from repository.inscripcion_repository import InscripcionRepositoryJSON
from servicios.inscripcion_service import InscripcionService


class AdminApp:
    """
    Interfaz gráfica del administrador del sistema de admisión.
    Permite gestionar inscripciones: aprobar, rechazar y visualizar.
    """

    def __init__(self, root, administrador):
        self.root = root
        self.administrador = administrador

        self.root.title("Panel Administrador - Sistema de Admisión ULEAM")
        self.root.geometry("1000x600")

        # Servicio de inscripciones
        self.inscripcion_service = InscripcionService(
            InscripcionRepositoryJSON()
        )

        self.crear_interfaz()
        self.cargar_inscripciones()

    def crear_interfaz(self):
        # ========== HEADER ==========
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)

        ttk.Label(
            header_frame,
            text=f" Administrador: {self.administrador.nombre}",
            font=("Arial", 16, "bold")
        ).pack()

        ttk.Label(
            header_frame,
            text=f"ID: {self.administrador.admin_id}",
            font=("Arial", 9),
            foreground="gray"
        ).pack()

        # ========== BARRA DE BOTONES ==========
        botones_frame = ttk.Frame(self.root, padding="10")
        botones_frame.pack(fill=tk.X)

        ttk.Button(
            botones_frame,
            text=" Actualizar Lista",
            command=self.cargar_inscripciones,
            width=20
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            botones_frame,
            text=" Aprobar Seleccionada",
            command=self.aprobar_seleccionada,
            width=20
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            botones_frame,
            text=" Rechazar Seleccionada",
            command=self.rechazar_seleccionada,
            width=20
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            botones_frame,
            text=" Estadísticas",
            command=self.mostrar_estadisticas,
            width=20
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            botones_frame,
            text=" Cerrar Sesión",
            command=self.cerrar_sesion,
            width=20
        ).grid(row=0, column=4, padx=5)

        # ========== FILTROS ==========
        filtros_frame = ttk.LabelFrame(self.root, text="Filtros", padding="5")
        filtros_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filtros_frame, text="Filtrar por estado:").grid(row=0, column=0, padx=5)
        
        self.filtro_estado = ttk.Combobox(
            filtros_frame,
            values=["TODOS", "PENDIENTE", "APROBADA", "RECHAZADA"],
            state="readonly",
            width=15
        )
        self.filtro_estado.set("TODOS")
        self.filtro_estado.grid(row=0, column=1, padx=5)
        self.filtro_estado.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros())

        # ========== TABLA DE INSCRIPCIONES ==========
        tabla_frame = ttk.Frame(self.root)
        tabla_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Columnas
        columnas = ("cedula", "postulante", "correo", "carrera", "estado")

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=15
        )

        # Configurar encabezados
        self.tabla.heading("cedula", text="Cédula")
        self.tabla.heading("postulante", text="Postulante")
        self.tabla.heading("correo", text="Correo")
        self.tabla.heading("carrera", text="Carrera")
        self.tabla.heading("estado", text="Estado")

        # Configurar anchos
        self.tabla.column("cedula", width=100)
        self.tabla.column("postulante", width=200)
        self.tabla.column("correo", width=200)
        self.tabla.column("carrera", width=250)
        self.tabla.column("estado", width=120)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL, command=self.tabla.xview)
        self.tabla.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Posicionar elementos
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configurar expansión
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        # ========== BARRA DE ESTADO ==========
        self.status_bar = ttk.Label(
            self.root,
            text="Listo",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def cargar_inscripciones(self):
        """Carga todas las inscripciones en la tabla"""
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Obtener registros
        registros = self.inscripcion_service.listar()

        if not registros:
            self.status_bar.config(text="No hay inscripciones registradas")
            return

        # Insertar en tabla
        for ins in registros:
            # Determinar tag según estado
            tag = self._obtener_tag_estado(ins["estado_inscripcion"])

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ins["cedula_postulante"],
                    ins["nombre_postulante"],
                    ins.get("correo_postulante", "N/A"),
                    ins["carrera_seleccionada"],
                    ins["estado_inscripcion"]
                ),
                tags=(tag,)
            )

        # Configurar colores por estado
        self.tabla.tag_configure("aprobada", background="#d4edda", foreground="#155724")
        self.tabla.tag_configure("rechazada", background="#f8d7da", foreground="#721c24")
        self.tabla.tag_configure("pendiente", background="#fff3cd", foreground="#856404")

        # Actualizar barra de estado
        total = len(registros)
        pendientes = len([r for r in registros if r["estado_inscripcion"] == "PENDIENTE"])
        aprobadas = len([r for r in registros if r["estado_inscripcion"] == "APROBADA"])
        
        self.status_bar.config(
            text=f"Total: {total} | Pendientes: {pendientes} | Aprobadas: {aprobadas}"
        )

    def aplicar_filtros(self):
        """Aplica filtros a la tabla"""
        filtro = self.filtro_estado.get()
        
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Obtener registros
        registros = self.inscripcion_service.listar()

        # Filtrar si es necesario
        if filtro != "TODOS":
            registros = [r for r in registros if r["estado_inscripcion"] == filtro]

        # Insertar en tabla
        for ins in registros:
            tag = self._obtener_tag_estado(ins["estado_inscripcion"])
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ins["cedula_postulante"],
                    ins["nombre_postulante"],
                    ins.get("correo_postulante", "N/A"),
                    ins["carrera_seleccionada"],
                    ins["estado_inscripcion"]
                ),
                tags=(tag,)
            )

        self.status_bar.config(text=f"Mostrando: {len(registros)} inscripción(es)")

    def _obtener_tag_estado(self, estado):
        """Retorna el tag según el estado"""
        if estado == "APROBADA":
            return "aprobada"
        elif estado == "RECHAZADA":
            return "rechazada"
        else:
            return "pendiente"

    def aprobar_seleccionada(self):
        """Aprueba la inscripción seleccionada"""
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, seleccione una inscripción de la tabla"
            )
            return

        item = self.tabla.item(seleccion[0])
        cedula = item["values"][0]
        nombre = item["values"][1]
        estado_actual = item["values"][4]

        if estado_actual != "PENDIENTE":
            messagebox.showwarning(
                "Acción No Permitida",
                f"Solo se pueden aprobar inscripciones PENDIENTES.\n"
                f"Estado actual: {estado_actual}"
            )
            return

        # Confirmar acción
        respuesta = messagebox.askyesno(
            "Confirmar Aprobación",
            f"¿Está seguro de aprobar la inscripción de:\n\n"
            f"{nombre}\n"
            f"Cédula: {cedula}"
        )

        if not respuesta:
            return

        try:
            self.inscripcion_service.aprobar_inscripcion(cedula)
            messagebox.showinfo(
                " Éxito",
                f"Inscripción de {nombre} aprobada correctamente"
            )
            self.cargar_inscripciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aprobar la inscripción:\n{e}")

    def rechazar_seleccionada(self):
        """Rechaza la inscripción seleccionada"""
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, seleccione una inscripción de la tabla"
            )
            return

        item = self.tabla.item(seleccion[0])
        cedula = item["values"][0]
        nombre = item["values"][1]
        estado_actual = item["values"][4]

        if estado_actual != "PENDIENTE":
            messagebox.showwarning(
                "Acción No Permitida",
                f"Solo se pueden rechazar inscripciones PENDIENTES.\n"
                f"Estado actual: {estado_actual}"
            )
            return

        # Confirmar acción
        respuesta = messagebox.askyesno(
            "Confirmar Rechazo",
            f"¿Está seguro de RECHAZAR la inscripción de:\n\n"
            f"{nombre}\n"
            f"Cédula: {cedula}",
            icon="warning"
        )

        if not respuesta:
            return

        try:
            self.inscripcion_service.rechazar_inscripcion(cedula)
            messagebox.showinfo(
                " Operación Completada",
                f"Inscripción de {nombre} rechazada"
            )
            self.cargar_inscripciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo rechazar la inscripción:\n{e}")

    def mostrar_estadisticas(self):
        """Muestra estadísticas del sistema"""
        registros = self.inscripcion_service.listar()
        
        total = len(registros)
        pendientes = len([r for r in registros if r["estado_inscripcion"] == "PENDIENTE"])
        aprobadas = len([r for r in registros if r["estado_inscripcion"] == "APROBADA"])
        rechazadas = len([r for r in registros if r["estado_inscripcion"] == "RECHAZADA"])

        # Contar por carrera
        carreras = {}
        for r in registros:
            carrera = r["carrera_seleccionada"]
            carreras[carrera] = carreras.get(carrera, 0) + 1

        # Construir mensaje
        mensaje = f" ESTADÍSTICAS DEL SISTEMA\n\n"
        mensaje += f"Total de inscripciones: {total}\n"
        mensaje += f"• Pendientes: {pendientes}\n"
        mensaje += f"• Aprobadas: {aprobadas}\n"
        mensaje += f"• Rechazadas: {rechazadas}\n\n"
        mensaje += "Inscripciones por carrera:\n"
        
        for carrera, cantidad in sorted(carreras.items()):
            mensaje += f"• {carrera}: {cantidad}\n"

        messagebox.showinfo("Estadísticas", mensaje)

    def cerrar_sesion(self):
        """Cierra la sesión del administrador"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar sesión?"
        )
        if respuesta:
            self.root.destroy()
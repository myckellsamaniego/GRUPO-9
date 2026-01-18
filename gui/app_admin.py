"""
GUI del Administrador - Sistema de Admisión
ACTUALIZADO: Compatible con DatosPersonalesCompletos del formulario de 6 pasos
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

from repository.inscripcion_repository import InscripcionRepositoryJSON
from servicios.inscripcion_service import InscripcionService


class AdminApp:
    """
    Interfaz gráfica del administrador del sistema de admisión.
    Permite gestionar inscripciones: aprobar, rechazar, visualizar y ver detalles completos.
    """

    def __init__(self, root, administrador):
        self.root = root
        self.administrador = administrador

        self.root.title("Panel Administrador - Sistema de Admisión ULEAM")
        self.root.geometry("1200x700")

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
            text=f"👤 Administrador: {self.administrador.nombre}",
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
            text="🔄 Actualizar Lista",
            command=self.cargar_inscripciones,
            width=20
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            botones_frame,
            text="👁️ Ver Detalles",
            command=self.ver_detalles_completos,
            width=20
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            botones_frame,
            text="✅ Aprobar",
            command=self.aprobar_seleccionada,
            width=20
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            botones_frame,
            text="❌ Rechazar",
            command=self.rechazar_seleccionada,
            width=20
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            botones_frame,
            text="📊 Estadísticas",
            command=self.mostrar_estadisticas,
            width=20
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            botones_frame,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            width=20
        ).grid(row=0, column=5, padx=5)

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

        ttk.Label(filtros_frame, text="Buscar por cédula:").grid(row=0, column=2, padx=(20, 5))
        
        self.buscar_cedula_var = tk.StringVar()
        self.buscar_cedula_var.trace('w', lambda *args: self.aplicar_filtros())
        ttk.Entry(
            filtros_frame,
            textvariable=self.buscar_cedula_var,
            width=15
        ).grid(row=0, column=3, padx=5)

        # ========== TABLA DE INSCRIPCIONES ==========
        tabla_frame = ttk.Frame(self.root)
        tabla_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Columnas actualizadas
        columnas = ("cedula", "postulante", "correo", "carrera", "fecha_nac", "celular", "estado")

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
        self.tabla.heading("fecha_nac", text="F. Nacimiento")
        self.tabla.heading("celular", text="Celular")
        self.tabla.heading("estado", text="Estado")

        # Configurar anchos
        self.tabla.column("cedula", width=90)
        self.tabla.column("postulante", width=180)
        self.tabla.column("correo", width=180)
        self.tabla.column("carrera", width=200)
        self.tabla.column("fecha_nac", width=100)
        self.tabla.column("celular", width=100)
        self.tabla.column("estado", width=100)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(tabla_frame, orient=tk.HORIZONTAL, command=self.tabla.xview)
        self.tabla.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Doble click para ver detalles
        self.tabla.bind("<Double-Button-1>", lambda e: self.ver_detalles_completos())

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
            # Extraer datos personales
            datos = ins.get("datos_personales", {})
            
            # Obtener fecha de nacimiento si existe
            fecha_nac = datos.get("fecha_nacimiento", "N/A")
            if fecha_nac and fecha_nac != "N/A":
                try:
                    # Si es un string ISO, convertir a formato legible
                    if isinstance(fecha_nac, str):
                        fecha_obj = datetime.fromisoformat(fecha_nac)
                        fecha_nac = fecha_obj.strftime("%d/%m/%Y")
                except:
                    fecha_nac = str(fecha_nac)
            
            # Determinar tag según estado
            tag = self._obtener_tag_estado(ins["estado_inscripcion"])

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ins["cedula_postulante"],
                    ins["nombre_postulante"],
                    ins.get("correo_postulante", datos.get("correo", "N/A")),
                    ins["carrera_seleccionada"],
                    fecha_nac,
                    datos.get("celular", "N/A"),
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
        filtro_estado = self.filtro_estado.get()
        buscar_cedula = self.buscar_cedula_var.get().strip()
        
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Obtener registros
        registros = self.inscripcion_service.listar()

        # Filtrar por estado
        if filtro_estado != "TODOS":
            registros = [r for r in registros if r["estado_inscripcion"] == filtro_estado]
        
        # Filtrar por cédula
        if buscar_cedula:
            registros = [r for r in registros if buscar_cedula in r["cedula_postulante"]]

        # Insertar en tabla
        for ins in registros:
            datos = ins.get("datos_personales", {})
            
            fecha_nac = datos.get("fecha_nacimiento", "N/A")
            if fecha_nac and fecha_nac != "N/A":
                try:
                    if isinstance(fecha_nac, str):
                        fecha_obj = datetime.fromisoformat(fecha_nac)
                        fecha_nac = fecha_obj.strftime("%d/%m/%Y")
                except:
                    fecha_nac = str(fecha_nac)
            
            tag = self._obtener_tag_estado(ins["estado_inscripcion"])
            
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    ins["cedula_postulante"],
                    ins["nombre_postulante"],
                    ins.get("correo_postulante", datos.get("correo", "N/A")),
                    ins["carrera_seleccionada"],
                    fecha_nac,
                    datos.get("celular", "N/A"),
                    ins["estado_inscripcion"]
                ),
                tags=(tag,)
            )

        self.status_bar.config(text=f"Mostrando: {len(registros)} inscripción(es)")

    def ver_detalles_completos(self):
        """Muestra una ventana con todos los detalles del postulante"""
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, seleccione una inscripción de la tabla"
            )
            return

        item = self.tabla.item(seleccion[0])
        cedula = item["values"][0]

        # Buscar inscripción completa
        inscripcion = self.inscripcion_service.buscar_por_cedula(cedula)
        
        if not inscripcion:
            messagebox.showerror("Error", "No se encontró la inscripción")
            return

        # Crear ventana de detalles
        detalles_window = tk.Toplevel(self.root)
        detalles_window.title(f"Detalles Completos - {inscripcion['nombre_postulante']}")
        detalles_window.geometry("900x700")
        detalles_window.resizable(True, True)

        # Header
        header = tk.Frame(detalles_window, bg="#1e3a8a", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"📋 Perfil Completo del Postulante",
            font=("Arial", 16, "bold"),
            bg="#1e3a8a",
            fg="white"
        ).pack(pady=10)

        estado_texto = inscripcion["estado_inscripcion"]
        color_estado = {"PENDIENTE": "#f59e0b", "APROBADA": "#10b981", "RECHAZADA": "#ef4444"}.get(estado_texto, "gray")
        
        tk.Label(
            header,
            text=f"Estado: {estado_texto}",
            font=("Arial", 11, "bold"),
            bg="#1e3a8a",
            fg=color_estado
        ).pack()

        # Contenedor con scroll
        canvas = tk.Canvas(detalles_window, bg="white")
        scrollbar = ttk.Scrollbar(detalles_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Extraer datos personales
        datos = inscripcion.get("datos_personales", {})

        # PASO 1: IDENTIFICACIÓN
        self._crear_seccion(scrollable_frame, "📝 PASO 1: IDENTIFICACIÓN", [
            ("Cédula", datos.get("cedula", "N/A")),
            ("Nombres", datos.get("nombre", "N/A")),
            ("Apellidos", datos.get("apellidos", "N/A")),
            ("Fecha de Nacimiento", self._formatear_fecha(datos.get("fecha_nacimiento"))),
            ("Estado Civil", datos.get("estado_civil", "N/A")),
            ("Sexo", datos.get("sexo", "N/A")),
            ("Identidad de Género", datos.get("identidad_genero", "N/A"))
        ])

        # PASO 2: CONTACTOS
        direccion_completa = datos.get("direccion", "N/A")
        self._crear_seccion(scrollable_frame, "📍 PASO 2: REFERENCIA Y CONTACTOS", [
            ("Correo Electrónico", datos.get("correo", "N/A")),
            ("Celular", datos.get("celular", "N/A")),
            ("Provincia", datos.get("provincia", "N/A")),
            ("Cantón", datos.get("canton", "N/A")),
            ("Parroquia", datos.get("parroquia", "N/A")),
            ("Barrio", datos.get("barrio", "N/A")),
            ("Calle Principal", datos.get("calle_principal", "N/A")),
            ("Calle Secundaria", datos.get("calle_secundaria", "N/A")),
            ("Número de Casa", datos.get("numero_casa", "N/A")),
            ("Dirección Completa", direccion_completa)
        ])

        # PASO 3: ETNIA
        self._crear_seccion(scrollable_frame, "🌍 PASO 3: AUTOIDENTIFICACIÓN ÉTNICA", [
            ("Etnia", datos.get("etnia", "N/A"))
        ])

        # PASO 4: DISCAPACIDAD
        self._crear_seccion(scrollable_frame, "♿ PASO 4: DISCAPACIDAD", [
            ("Tiene Discapacidad", "Sí" if datos.get("discapacidad") else "No"),
            ("Requiere Apoyo en Evaluación", "Sí" if datos.get("requiere_apoyo_evaluacion") else "No")
        ])

        # PASO 5: TECNOLOGÍA
        self._crear_seccion(scrollable_frame, "💻 PASO 5: INFORMACIÓN TECNOLÓGICA", [
            ("Internet en Domicilio", "Sí" if datos.get("internet_domicilio") else "No"),
            ("Computadora Funcional", "Sí" if datos.get("computadora_funcional") else "No"),
            ("Sistema Operativo", datos.get("sistema_operativo", "N/A")),
            ("Cámara Web", "Sí" if datos.get("camara_web") else "No")
        ])

        # PASO 6: EDUCACIÓN
        self._crear_seccion(scrollable_frame, "🎓 PASO 6: EDUCACIÓN", [
            ("Orientación Vocacional", "Sí" if datos.get("orientacion_vocacional") else "No"),
            ("Institución a la que Aspira", datos.get("institucion_aspirar", "N/A")),
            ("Nivel Máximo de Estudios", datos.get("nivel_maximo_estudios", "N/A")),
            ("Razón para Estudiar", datos.get("razon_estudiar_carrera", "N/A"))
        ])

        # INFORMACIÓN DE INSCRIPCIÓN
        self._crear_seccion(scrollable_frame, "🎯 INFORMACIÓN DE INSCRIPCIÓN", [
            ("Carrera Seleccionada", inscripcion.get("carrera_seleccionada", "N/A")),
            ("Cupos Disponibles", str(inscripcion.get("cupos_oferta", "N/A"))),
            ("Código de Oferta", inscripcion.get("codigo_oferta", "N/A")),
            ("Estado de Inscripción", inscripcion["estado_inscripcion"])
        ])

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Botón cerrar
        btn_frame = tk.Frame(detalles_window, bg="#f3f4f6", height=60)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        btn_frame.pack_propagate(False)

        tk.Button(
            btn_frame,
            text="✖ Cerrar",
            command=detalles_window.destroy,
            bg="#6b7280",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(pady=10)

    def _crear_seccion(self, parent, titulo, campos):
        """Crea una sección de información en el detalle"""
        frame = tk.LabelFrame(
            parent,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#1e40af",
            padx=15,
            pady=10
        )
        frame.pack(fill=tk.X, padx=20, pady=10)

        for i, (etiqueta, valor) in enumerate(campos):
            row_frame = tk.Frame(frame, bg="white")
            row_frame.pack(fill=tk.X, pady=3)

            tk.Label(
                row_frame,
                text=f"{etiqueta}:",
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#374151",
                width=25,
                anchor="w"
            ).pack(side=tk.LEFT)

            # Si el valor es muy largo, usar Text widget
            if isinstance(valor, str) and len(valor) > 60:
                text_widget = tk.Text(
                    row_frame,
                    height=3,
                    width=50,
                    font=("Arial", 9),
                    wrap=tk.WORD,
                    bg="#f9fafb",
                    relief=tk.FLAT
                )
                text_widget.insert("1.0", valor)
                text_widget.config(state="disabled")
                text_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            else:
                tk.Label(
                    row_frame,
                    text=str(valor),
                    font=("Arial", 10),
                    bg="white",
                    fg="#111827",
                    anchor="w"
                ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _formatear_fecha(self, fecha):
        """Formatea una fecha para mostrar"""
        if not fecha or fecha == "N/A":
            return "N/A"
        try:
            if isinstance(fecha, str):
                fecha_obj = datetime.fromisoformat(fecha)
                return fecha_obj.strftime("%d/%m/%Y")
            return str(fecha)
        except:
            return str(fecha)

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
        estado_actual = item["values"][6]

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
                "✅ Éxito",
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
        estado_actual = item["values"][6]

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
                "✅ Operación Completada",
                f"Inscripción de {nombre} rechazada"
            )
            self.cargar_inscripciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo rechazar la inscripción:\n{e}")

    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas del sistema"""
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

        # Estadísticas adicionales de datos completos
        con_perfil_completo = 0
        con_discapacidad = 0
        con_internet = 0
        
        for r in registros:
            datos = r.get("datos_personales", {})
            if datos.get("fecha_nacimiento"):
                con_perfil_completo += 1
            if datos.get("discapacidad"):
                con_discapacidad += 1
            if datos.get("internet_domicilio"):
                con_internet += 1

        # Construir mensaje
        mensaje = f"📊 ESTADÍSTICAS DEL SISTEMA\n\n"
        mensaje += f"{'='*40}\n"
        mensaje += f"INSCRIPCIONES\n"
        mensaje += f"{'='*40}\n"
        mensaje += f"Total de inscripciones: {total}\n"
        mensaje += f"• Pendientes: {pendientes}\n"
        mensaje += f"• Aprobadas: {aprobadas}\n"
        mensaje += f"• Rechazadas: {rechazadas}\n\n"
        
        mensaje += f"{'='*40}\n"
        mensaje += f"PERFILES COMPLETADOS\n"
        mensaje += f"{'='*40}\n"
        mensaje += f"• Con perfil completo: {con_perfil_completo} ({round(con_perfil_completo/total*100 if total > 0 else 0, 1)}%)\n"
        mensaje += f"• Con discapacidad: {con_discapacidad}\n"
        mensaje += f"• Con acceso a internet: {con_internet}\n\n"
        
        mensaje += f"{'='*40}\n"
        mensaje += "INSCRIPCIONES POR CARRERA\n"
        mensaje += f"{'='*40}\n"
        
        for carrera, cantidad in sorted(carreras.items()):
            mensaje += f"• {carrera}: {cantidad}\n"

        messagebox.showinfo("Estadísticas Detalladas", mensaje)

    def cerrar_sesion(self):
        """Cierra la sesión del administrador"""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea cerrar sesión?"
        )
        if respuesta:
            self.root.destroy()
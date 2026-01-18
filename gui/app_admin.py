"""
Panel de Administrador Mejorado - Sistema de Admisión ULEAM
Gestión completa de usuarios, inscripciones y sedes
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

from repository.inscripcion_repository import InscripcionRepositoryJSON
from repository.usuario_repository_json import UsuarioRepositoryJSON
from repository.sede_repository import SedeRepositoryJSON
from servicios.inscripcion_service import InscripcionService
from models.sede import Sede
from models.datos_personales import DatosPersonales
from models.datos_personales_completos import DatosPersonalesCompletos
from factory.fabrica_usuarios import FabricaUsuarios


class AdminAppMejorado:
    """Panel de administrador con gestión completa"""

    # Paleta de colores moderna
    COLOR_PRIMARY = "#1e40af"      # Azul oscuro
    COLOR_SECONDARY = "#3b82f6"    # Azul medio
    COLOR_ACCENT = "#60a5fa"       # Azul claro
    COLOR_SUCCESS = "#10b981"      # Verde
    COLOR_WARNING = "#f59e0b"      # Naranja
    COLOR_DANGER = "#ef4444"       # Rojo
    COLOR_BG = "#f8fafc"           # Fondo claro
    COLOR_WHITE = "#ffffff"
    COLOR_TEXT = "#1e293b"
    COLOR_TEXT_LIGHT = "#64748b"

    def __init__(self, root, administrador):
        self.root = root
        self.administrador = administrador
        
        self.root.title("Panel de Administrador - ULEAM")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.COLOR_BG)
        
        # Repositorios y servicios
        self.inscripcion_service = InscripcionService(InscripcionRepositoryJSON())
        self.usuario_repo = UsuarioRepositoryJSON()
        self.sede_repo = SedeRepositoryJSON()
        self.fabrica = FabricaUsuarios()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Mostrar panel de inicio
        self.mostrar_panel_inicio()

    def crear_interfaz(self):
        """Crea la estructura principal de la interfaz"""
        
        # ========== BARRA SUPERIOR ==========
        self.crear_barra_superior()
        
        # ========== CONTENEDOR PRINCIPAL ==========
        main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ========== MENÚ LATERAL ==========
        self.crear_menu_lateral(main_container)
        
        # ========== ÁREA DE CONTENIDO ==========
        self.content_frame = tk.Frame(main_container, bg=self.COLOR_WHITE)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_barra_superior(self):
        """Crea la barra superior con info del admin"""
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo y título
        tk.Label(
            header,
            text="🎓 ULEAM - SISTEMA DE ADMISIÓN",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_WHITE
        ).pack(side=tk.LEFT, padx=20)
        
        # Info del admin
        info_frame = tk.Frame(header, bg=self.COLOR_PRIMARY)
        info_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(
            info_frame,
            text=f"Administrador: {self.administrador.nombre}",
            font=("Arial", 10),
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_WHITE
        ).pack(anchor=tk.E)
        
        tk.Label(
            info_frame,
            text=f"ID: {self.administrador.admin_id}",
            font=("Arial", 9),
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_ACCENT
        ).pack(anchor=tk.E)

    def crear_menu_lateral(self, parent):
        """Crea el menú de navegación lateral"""
        menu = tk.Frame(parent, bg=self.COLOR_WHITE, width=250, relief=tk.RAISED, bd=1)
        menu.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
        menu.pack_propagate(False)
        
        tk.Label(
            menu,
            text="MENÚ PRINCIPAL",
            font=("Arial", 12, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_TEXT
        ).pack(pady=(20, 10), padx=10)
        
        # Separador
        tk.Frame(menu, height=2, bg=self.COLOR_ACCENT).pack(fill=tk.X, padx=10, pady=5)
        
        # Opciones del menú
        opciones = [
            ("🏠 Inicio", self.mostrar_panel_inicio),
            ("📋 Inscripciones", self.mostrar_panel_inscripciones),
            ("👥 Usuarios", self.mostrar_panel_usuarios),
            ("🏢 Sedes", self.mostrar_panel_sedes),
            ("📊 Estadísticas", self.mostrar_estadisticas),
            ("🚪 Cerrar Sesión", self.cerrar_sesion)
        ]
        
        for texto, comando in opciones:
            self.crear_boton_menu(menu, texto, comando)

    def crear_boton_menu(self, parent, texto, comando):
        """Crea un botón del menú lateral"""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Arial", 11),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_TEXT,
            activebackground=self.COLOR_ACCENT,
            activeforeground=self.COLOR_WHITE,
            relief=tk.FLAT,
            cursor="hand2",
            anchor=tk.W,
            padx=20,
            pady=12,
            command=comando
        )
        btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Efecto hover
        btn.bind("<Enter>", lambda e: btn.config(bg=self.COLOR_ACCENT, fg=self.COLOR_WHITE))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.COLOR_WHITE, fg=self.COLOR_TEXT))

    def limpiar_contenido(self):
        """Limpia el área de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_panel_inicio(self):
        """Muestra el panel de inicio con resumen"""
        self.limpiar_contenido()
        
        # Título
        tk.Label(
            self.content_frame,
            text="📊 Panel de Control",
            font=("Arial", 24, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_PRIMARY
        ).pack(pady=30)
        
        # Tarjetas de resumen
        cards_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        cards_frame.pack(pady=20)
        
        # Obtener estadísticas
        inscripciones = self.inscripcion_service.listar()
        usuarios = self.usuario_repo.listar_postulantes()
        sedes = self.sede_repo.listar_todas()
        
        pendientes = len([i for i in inscripciones if i['estado_inscripcion'] == 'PENDIENTE'])
        aprobadas = len([i for i in inscripciones if i['estado_inscripcion'] == 'APROBADA'])
        
        # Crear tarjetas
        self.crear_tarjeta_estadistica(cards_frame, "👥 Total Usuarios", len(usuarios), self.COLOR_SECONDARY, 0, 0)
        self.crear_tarjeta_estadistica(cards_frame, "📝 Total Inscripciones", len(inscripciones), self.COLOR_SUCCESS, 0, 1)
        self.crear_tarjeta_estadistica(cards_frame, "⏳ Pendientes", pendientes, self.COLOR_WARNING, 1, 0)
        self.crear_tarjeta_estadistica(cards_frame, "✅ Aprobadas", aprobadas, self.COLOR_SUCCESS, 1, 1)
        self.crear_tarjeta_estadistica(cards_frame, "🏢 Sedes", len(sedes), self.COLOR_PRIMARY, 2, 0)
        
        # Botones de acción rápida
        tk.Label(
            self.content_frame,
            text="Acciones Rápidas",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_TEXT
        ).pack(pady=(40, 20))
        
        btn_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        btn_frame.pack()
        
        self.crear_boton_accion(btn_frame, "📋 Ver Inscripciones", self.mostrar_panel_inscripciones).grid(row=0, column=0, padx=10)
        self.crear_boton_accion(btn_frame, "👥 Gestionar Usuarios", self.mostrar_panel_usuarios).grid(row=0, column=1, padx=10)
        self.crear_boton_accion(btn_frame, "🏢 Gestionar Sedes", self.mostrar_panel_sedes).grid(row=0, column=2, padx=10)

    def crear_tarjeta_estadistica(self, parent, titulo, valor, color, row, col):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=0)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        tk.Label(
            card,
            text=titulo,
            font=("Arial", 12),
            bg=color,
            fg=self.COLOR_WHITE
        ).pack(pady=(20, 5), padx=30)
        
        tk.Label(
            card,
            text=str(valor),
            font=("Arial", 32, "bold"),
            bg=color,
            fg=self.COLOR_WHITE
        ).pack(pady=(0, 20), padx=30)

    def crear_boton_accion(self, parent, texto, comando):
        """Crea un botón de acción"""
        return tk.Button(
            parent,
            text=texto,
            font=("Arial", 12, "bold"),
            bg=self.COLOR_SECONDARY,
            fg=self.COLOR_WHITE,
            activebackground=self.COLOR_PRIMARY,
            activeforeground=self.COLOR_WHITE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=15,
            command=comando
        )

    def mostrar_panel_inscripciones(self):
        """Muestra el panel de gestión de inscripciones"""
        self.limpiar_contenido()
        
        # Título
        header_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        header_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
        
        tk.Label(
            header_frame,
            text="📋 Gestión de Inscripciones",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_PRIMARY
        ).pack(side=tk.LEFT)
        
        # Botones de acción
        btn_actualizar = tk.Button(
            header_frame,
            text="🔄 Actualizar",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_SECONDARY,
            fg=self.COLOR_WHITE,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.mostrar_panel_inscripciones
        )
        btn_actualizar.pack(side=tk.RIGHT, padx=5)
        
        # Filtros
        filtros_frame = tk.LabelFrame(
            self.content_frame,
            text="Filtros",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_TEXT
        )
        filtros_frame.pack(fill=tk.X, padx=20, pady=10)
        
        filter_container = tk.Frame(filtros_frame, bg=self.COLOR_WHITE)
        filter_container.pack(pady=10, padx=10)
        
        tk.Label(filter_container, text="Estado:", bg=self.COLOR_WHITE).grid(row=0, column=0, padx=5)
        self.filtro_estado_insc = ttk.Combobox(
            filter_container,
            values=["TODOS", "PENDIENTE", "APROBADA", "RECHAZADA"],
            state="readonly",
            width=15
        )
        self.filtro_estado_insc.set("TODOS")
        self.filtro_estado_insc.grid(row=0, column=1, padx=5)
        self.filtro_estado_insc.bind("<<ComboboxSelected>>", lambda e: self.aplicar_filtros_inscripciones())
        
        tk.Label(filter_container, text="Buscar por cédula:", bg=self.COLOR_WHITE).grid(row=0, column=2, padx=(20, 5))
        self.buscar_cedula_insc_var = tk.StringVar()
        self.buscar_cedula_insc_var.trace('w', lambda *args: self.aplicar_filtros_inscripciones())
        ttk.Entry(filter_container, textvariable=self.buscar_cedula_insc_var, width=15).grid(row=0, column=3, padx=5)
        
        # Tabla
        tabla_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columnas = ("cedula", "nombre", "correo", "carrera", "estado")
        self.tabla_inscripciones = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)
        
        self.tabla_inscripciones.heading("cedula", text="Cédula")
        self.tabla_inscripciones.heading("nombre", text="Nombre Completo")
        self.tabla_inscripciones.heading("correo", text="Correo")
        self.tabla_inscripciones.heading("carrera", text="Carrera")
        self.tabla_inscripciones.heading("estado", text="Estado")
        
        self.tabla_inscripciones.column("cedula", width=100)
        self.tabla_inscripciones.column("nombre", width=200)
        self.tabla_inscripciones.column("correo", width=200)
        self.tabla_inscripciones.column("carrera", width=200)
        self.tabla_inscripciones.column("estado", width=100)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla_inscripciones.yview)
        self.tabla_inscripciones.configure(yscroll=scrollbar.set)
        
        self.tabla_inscripciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Colores por estado
        self.tabla_inscripciones.tag_configure("aprobada", background="#d1fae5")
        self.tabla_inscripciones.tag_configure("rechazada", background="#fee2e2")
        self.tabla_inscripciones.tag_configure("pendiente", background="#fef3c7")
        
        # Botones de acción
        acciones_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        acciones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            acciones_frame, text="✅ Aprobar", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.aprobar_inscripcion
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            acciones_frame, text="❌ Rechazar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.rechazar_inscripcion
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            acciones_frame, text="👁️ Ver Detalles", bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.ver_detalles_inscripcion
        ).pack(side=tk.LEFT, padx=5)
        
        # Cargar datos
        self.cargar_inscripciones()

    def cargar_inscripciones(self):
        """Carga las inscripciones en la tabla"""
        for item in self.tabla_inscripciones.get_children():
            self.tabla_inscripciones.delete(item)
        
        inscripciones = self.inscripcion_service.listar()
        for insc in inscripciones:
            tag = "aprobada" if insc['estado_inscripcion'] == "APROBADA" else \
                  "rechazada" if insc['estado_inscripcion'] == "RECHAZADA" else "pendiente"
            
            self.tabla_inscripciones.insert("", tk.END, values=(
                insc['cedula_postulante'],
                insc['nombre_postulante'],
                insc.get('correo_postulante', ''),
                insc['carrera_seleccionada'],
                insc['estado_inscripcion']
            ), tags=(tag,))

    def aplicar_filtros_inscripciones(self):
        """Aplica filtros a inscripciones"""
        for item in self.tabla_inscripciones.get_children():
            self.tabla_inscripciones.delete(item)
        
        estado = self.filtro_estado_insc.get()
        cedula = self.buscar_cedula_insc_var.get().strip()
        
        inscripciones = self.inscripcion_service.listar()
        
        if estado != "TODOS":
            inscripciones = [i for i in inscripciones if i['estado_inscripcion'] == estado]
        if cedula:
            inscripciones = [i for i in inscripciones if cedula in i['cedula_postulante']]
        
        for insc in inscripciones:
            tag = "aprobada" if insc['estado_inscripcion'] == "APROBADA" else \
                  "rechazada" if insc['estado_inscripcion'] == "RECHAZADA" else "pendiente"
            
            self.tabla_inscripciones.insert("", tk.END, values=(
                insc['cedula_postulante'],
                insc['nombre_postulante'],
                insc.get('correo_postulante', ''),
                insc['carrera_seleccionada'],
                insc['estado_inscripcion']
            ), tags=(tag,))

    def aprobar_inscripcion(self):
        """Aprueba una inscripción seleccionada"""
        seleccion = self.tabla_inscripciones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una inscripción")
            return
        
        item = self.tabla_inscripciones.item(seleccion[0])
        cedula = item['values'][0]
        nombre = item['values'][1]
        estado = item['values'][4]
        
        if estado != "PENDIENTE":
            messagebox.showwarning("Advertencia", f"Solo se pueden aprobar inscripciones PENDIENTES.\nEstado actual: {estado}")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Aprobar inscripción de {nombre}?"):
            try:
                self.inscripcion_service.aprobar_inscripcion(cedula)
                messagebox.showinfo("Éxito", "Inscripción aprobada")
                self.cargar_inscripciones()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def rechazar_inscripcion(self):
        """Rechaza una inscripción seleccionada"""
        seleccion = self.tabla_inscripciones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una inscripción")
            return
        
        item = self.tabla_inscripciones.item(seleccion[0])
        cedula = item['values'][0]
        nombre = item['values'][1]
        estado = item['values'][4]
        
        if estado != "PENDIENTE":
            messagebox.showwarning("Advertencia", f"Solo se pueden rechazar inscripciones PENDIENTES.\nEstado actual: {estado}")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Rechazar inscripción de {nombre}?", icon="warning"):
            try:
                self.inscripcion_service.rechazar_inscripcion(cedula)
                messagebox.showinfo("Éxito", "Inscripción rechazada")
                self.cargar_inscripciones()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def ver_detalles_inscripcion(self):
        """Muestra detalles completos de una inscripción"""
        seleccion = self.tabla_inscripciones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una inscripción")
            return
        
        item = self.tabla_inscripciones.item(seleccion[0])
        cedula = item['values'][0]
        
        inscripcion = self.inscripcion_service.buscar_por_cedula(cedula)
        if not inscripcion:
            messagebox.showerror("Error", "Inscripción no encontrada")
            return
        
        # Ventana de detalles
        detalles = tk.Toplevel(self.root)
        detalles.title(f"Detalles - {inscripcion['nombre_postulante']}")
        detalles.geometry("700x600")
        
        text = scrolledtext.ScrolledText(detalles, wrap=tk.WORD, font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        datos = inscripcion.get('datos_personales', {})
        
        info = f"""
╔══════════════════════════════════════════════════════════════╗
║           DETALLES COMPLETOS DEL POSTULANTE                 ║
╚══════════════════════════════════════════════════════════════╝

📋 INFORMACIÓN PERSONAL
  • Cédula: {datos.get('cedula', 'N/A')}
  • Nombres: {datos.get('nombre', 'N/A')}
  • Apellidos: {datos.get('apellidos', 'N/A')}
  • Fecha Nacimiento: {datos.get('fecha_nacimiento', 'N/A')}
  • Estado Civil: {datos.get('estado_civil', 'N/A')}
  • Sexo: {datos.get('sexo', 'N/A')}

📞 CONTACTO
  • Correo: {datos.get('correo', 'N/A')}
  • Celular: {datos.get('celular', 'N/A')}
  • Provincia: {datos.get('provincia', 'N/A')}
  • Cantón: {datos.get('canton', 'N/A')}
  • Dirección: {datos.get('direccion', 'N/A')}

🎯 INSCRIPCIÓN
  • Carrera: {inscripcion['carrera_seleccionada']}
  • Estado: {inscripcion['estado_inscripcion']}
  • Código Oferta: {inscripcion.get('codigo_oferta', 'N/A')}

🌍 OTROS DATOS
  • Etnia: {datos.get('etnia', 'N/A')}
  • Discapacidad: {'Sí' if datos.get('discapacidad') else 'No'}
  • Internet: {'Sí' if datos.get('internet_domicilio') else 'No'}
  • Computadora: {'Sí' if datos.get('computadora_funcional') else 'No'}
        """
        
        text.insert("1.0", info)
        text.config(state=tk.DISABLED)

    def mostrar_panel_usuarios(self):
        """Muestra el panel de gestión de usuarios"""
        self.limpiar_contenido()
        
        # Título
        header_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        header_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
        
        tk.Label(
            header_frame,
            text="👥 Gestión de Usuarios",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_PRIMARY
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            header_frame, text="➕ Nuevo Usuario", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=15, pady=8,
            command=self.crear_usuario
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            header_frame, text="🔄 Actualizar", bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=15, pady=8,
            command=self.mostrar_panel_usuarios
        ).pack(side=tk.RIGHT, padx=5)
        
        # Filtros
        filtros_frame = tk.LabelFrame(self.content_frame, text="Filtros", font=("Arial", 10, "bold"), bg=self.COLOR_WHITE)
        filtros_frame.pack(fill=tk.X, padx=20, pady=10)
        
        filter_container = tk.Frame(filtros_frame, bg=self.COLOR_WHITE)
        filter_container.pack(pady=10, padx=10)
        
        tk.Label(filter_container, text="Buscar por cédula:", bg=self.COLOR_WHITE).grid(row=0, column=0, padx=5)
        self.buscar_usuario_cedula_var = tk.StringVar()
        self.buscar_usuario_cedula_var.trace('w', lambda *args: self.aplicar_filtros_usuarios())
        ttk.Entry(filter_container, textvariable=self.buscar_usuario_cedula_var, width=15).grid(row=0, column=1, padx=5)
        
        tk.Label(filter_container, text="Buscar por nombre:", bg=self.COLOR_WHITE).grid(row=0, column=2, padx=(20, 5))
        self.buscar_usuario_nombre_var = tk.StringVar()
        self.buscar_usuario_nombre_var.trace('w', lambda *args: self.aplicar_filtros_usuarios())
        ttk.Entry(filter_container, textvariable=self.buscar_usuario_nombre_var, width=20).grid(row=0, column=3, padx=5)
        
        # Tabla
        tabla_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columnas = ("cedula", "nombre", "apellidos", "correo", "celular")
        self.tabla_usuarios = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)
        
        self.tabla_usuarios.heading("cedula", text="Cédula")
        self.tabla_usuarios.heading("nombre", text="Nombres")
        self.tabla_usuarios.heading("apellidos", text="Apellidos")
        self.tabla_usuarios.heading("correo", text="Correo")
        self.tabla_usuarios.heading("celular", text="Celular")
        
        self.tabla_usuarios.column("cedula", width=100)
        self.tabla_usuarios.column("nombre", width=150)
        self.tabla_usuarios.column("apellidos", width=150)
        self.tabla_usuarios.column("correo", width=200)
        self.tabla_usuarios.column("celular", width=100)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscroll=scrollbar.set)
        
        self.tabla_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        acciones_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        acciones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            acciones_frame, text="✏️ Editar", bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.editar_usuario
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            acciones_frame, text="🗑️ Eliminar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.eliminar_usuario
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            acciones_frame, text="👁️ Ver Detalles", bg=self.COLOR_PRIMARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.ver_detalles_usuario
        ).pack(side=tk.LEFT, padx=5)
        
        # Cargar datos
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """Carga los usuarios en la tabla"""
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        usuarios = self.usuario_repo.listar_postulantes()
        for user in usuarios:
            datos = user.datos_personales
            self.tabla_usuarios.insert("", tk.END, values=(
                datos.cedula,
                datos.nombre,
                datos.apellidos,
                datos.correo,
                datos.celular if hasattr(datos, 'celular') else 'N/A'
            ))

    def aplicar_filtros_usuarios(self):
        """Aplica filtros a usuarios"""
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        cedula = self.buscar_usuario_cedula_var.get().strip().lower()
        nombre = self.buscar_usuario_nombre_var.get().strip().lower()
        
        usuarios = self.usuario_repo.listar_postulantes()
        
        for user in usuarios:
            datos = user.datos_personales
            if cedula and cedula not in datos.cedula.lower():
                continue
            if nombre and nombre not in datos.nombre.lower() and nombre not in datos.apellidos.lower():
                continue
            
            self.tabla_usuarios.insert("", tk.END, values=(
                datos.cedula,
                datos.nombre,
                datos.apellidos,
                datos.correo,
                datos.celular if hasattr(datos, 'celular') else 'N/A'
            ))

    def crear_usuario(self):
        """Abre ventana para crear nuevo usuario"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Nuevo Usuario")
        ventana.geometry("500x600")
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Header
        header = tk.Frame(ventana, bg=self.COLOR_PRIMARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="➕ Nuevo Postulante", font=("Arial", 16, "bold"),
                bg=self.COLOR_PRIMARY, fg=self.COLOR_WHITE).pack(pady=15)
        
        # Formulario
        form = tk.Frame(ventana, bg=self.COLOR_WHITE, padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True)
        
        entries = {}
        campos = [
            ("Cédula *", "cedula"),
            ("Nombres *", "nombres"),
            ("Apellidos *", "apellidos"),
            ("Correo *", "correo"),
            ("Celular", "celular"),
            ("Contraseña *", "password")
        ]
        
        for i, (label, key) in enumerate(campos):
            tk.Label(form, text=label, bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
                row=i*2, column=0, sticky=tk.W, pady=(5, 2))
            entry = ttk.Entry(form, width=40, show="*" if key == "password" else None)
            entry.grid(row=i*2+1, column=0, sticky=tk.EW, pady=(0, 10))
            entries[key] = entry
        
        def guardar():
            try:
                cedula = entries['cedula'].get().strip()
                nombres = entries['nombres'].get().strip()
                apellidos = entries['apellidos'].get().strip()
                correo = entries['correo'].get().strip()
                celular = entries['celular'].get().strip()
                password = entries['password'].get()
                
                if not all([cedula, nombres, apellidos, correo, password]):
                    raise ValueError("Complete los campos obligatorios")
                
                if self.usuario_repo.existe_cedula(cedula):
                    raise ValueError("Ya existe un usuario con esa cédula")
                
                if self.usuario_repo.buscar_por_correo(correo):
                    raise ValueError("Ya existe un usuario con ese correo")
                
                datos = DatosPersonales(
                    nombre=nombres,
                    apellidos=apellidos,
                    cedula=cedula,
                    correo=correo,
                    celular=celular,
                    direccion="",
                    etnia="",
                    discapacidad=False
                )
                
                postulante = self.fabrica.crear_usuario("Postulante", correo=correo,
                                                       password=password, datos_personales=datos)
                self.usuario_repo.agregar(postulante)
                
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                ventana.destroy()
                self.cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Botones
        btn_frame = tk.Frame(form, bg=self.COLOR_WHITE)
        btn_frame.grid(row=len(campos)*2, column=0, pady=20)
        
        tk.Button(btn_frame, text="✔ Guardar", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✖ Cancelar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=5)

    def editar_usuario(self):
        """Edita un usuario seleccionado"""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return
        
        item = self.tabla_usuarios.item(seleccion[0])
        cedula = item['values'][0]
        
        usuario = self.usuario_repo.buscar_por_cedula(cedula)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        # Ventana de edición
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Usuario")
        ventana.geometry("500x600")
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Header
        header = tk.Frame(ventana, bg=self.COLOR_SECONDARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="✏️ Editar Postulante", font=("Arial", 16, "bold"),
                bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE).pack(pady=15)
        
        # Formulario
        form = tk.Frame(ventana, bg=self.COLOR_WHITE, padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True)
        
        datos = usuario.datos_personales
        
        entries = {}
        campos = [
            ("Cédula", "cedula", datos.cedula, True),
            ("Nombres", "nombres", datos.nombre, False),
            ("Apellidos", "apellidos", datos.apellidos, False),
            ("Correo", "correo", datos.correo, False),
            ("Celular", "celular", datos.celular if hasattr(datos, 'celular') else '', False)
        ]
        
        for i, (label, key, valor, readonly) in enumerate(campos):
            tk.Label(form, text=label + ":", bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
                row=i*2, column=0, sticky=tk.W, pady=(5, 2))
            entry = ttk.Entry(form, width=40)
            entry.insert(0, valor)
            if readonly:
                entry.config(state='readonly')
            entry.grid(row=i*2+1, column=0, sticky=tk.EW, pady=(0, 10))
            entries[key] = entry
        
        def guardar():
            try:
                # Actualizar datos
                datos.nombre = entries['nombres'].get().strip()
                datos.apellidos = entries['apellidos'].get().strip()
                datos.correo = entries['correo'].get().strip()
                if hasattr(datos, 'celular'):
                    datos.celular = entries['celular'].get().strip()
                
                self.usuario_repo.actualizar(usuario)
                messagebox.showinfo("Éxito", "Usuario actualizado")
                ventana.destroy()
                self.cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Botones
        btn_frame = tk.Frame(form, bg=self.COLOR_WHITE)
        btn_frame.grid(row=len(campos)*2, column=0, pady=20)
        
        tk.Button(btn_frame, text="✔ Guardar", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✖ Cancelar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=5)

    def eliminar_usuario(self):
        """Elimina un usuario"""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return
        
        item = self.tabla_usuarios.item(seleccion[0])
        cedula = item['values'][0]
        nombre = f"{item['values'][1]} {item['values'][2]}"
        
        if messagebox.askyesno("Confirmar Eliminación",
                              f"¿Está seguro de eliminar a {nombre}?\n\nEsta acción no se puede deshacer.",
                              icon="warning"):
            try:
                usuario = self.usuario_repo.buscar_por_cedula(cedula)
                self.usuario_repo.eliminar(usuario.correo)
                messagebox.showinfo("Éxito", "Usuario eliminado")
                self.cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def ver_detalles_usuario(self):
        """Muestra detalles del usuario"""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return
        
        item = self.tabla_usuarios.item(seleccion[0])
        cedula = item['values'][0]
        
        usuario = self.usuario_repo.buscar_por_cedula(cedula)
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        datos = usuario.datos_personales
        
        info = f"""
DATOS DEL USUARIO

Cédula: {datos.cedula}
Nombres: {datos.nombre}
Apellidos: {datos.apellidos}
Correo: {datos.correo}
Celular: {datos.celular if hasattr(datos, 'celular') else 'N/A'}
Dirección: {datos.direccion if hasattr(datos, 'direccion') else 'N/A'}
Etnia: {datos.etnia if hasattr(datos, 'etnia') else 'N/A'}
Discapacidad: {'Sí' if datos.discapacidad else 'No'}
        """
        
        messagebox.showinfo("Detalles del Usuario", info)

    def mostrar_panel_sedes(self):
        """Muestra el panel de gestión de sedes"""
        self.limpiar_contenido()
        
        # Título
        header_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        header_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
        
        tk.Label(
            header_frame,
            text="🏢 Gestión de Sedes",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_PRIMARY
        ).pack(side=tk.LEFT)
        
        # Botones
        tk.Button(
            header_frame, text="➕ Nueva Sede", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=15, pady=8,
            command=self.crear_sede
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            header_frame, text="🔄 Actualizar", bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=15, pady=8,
            command=self.mostrar_panel_sedes
        ).pack(side=tk.RIGHT, padx=5)
        
        # Tabla
        tabla_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columnas = ("nombre", "direccion", "ciudad", "capacidad")
        self.tabla_sedes = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)
        
        self.tabla_sedes.heading("nombre", text="Nombre Sede")
        self.tabla_sedes.heading("direccion", text="Dirección")
        self.tabla_sedes.heading("ciudad", text="Ciudad")
        self.tabla_sedes.heading("capacidad", text="Capacidad")
        
        self.tabla_sedes.column("nombre", width=200)
        self.tabla_sedes.column("direccion", width=300)
        self.tabla_sedes.column("ciudad", width=150)
        self.tabla_sedes.column("capacidad", width=100)
        
        scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla_sedes.yview)
        self.tabla_sedes.configure(yscroll=scrollbar.set)
        
        self.tabla_sedes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        acciones_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        acciones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            acciones_frame, text="✏️ Editar", bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.editar_sede
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            acciones_frame, text="🗑️ Eliminar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
            font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=10,
            command=self.eliminar_sede
        ).pack(side=tk.LEFT, padx=5)
        
        # Cargar datos
        self.cargar_sedes()

    def cargar_sedes(self):
        """Carga las sedes en la tabla"""
        for item in self.tabla_sedes.get_children():
            self.tabla_sedes.delete(item)
        
        sedes = self.sede_repo.listar_todas()
        for sede in sedes:
            self.tabla_sedes.insert("", tk.END, values=(
                sede.nombre,
                sede.direccion,
                sede.ciudad,
                sede.capacidad
            ))

    def crear_sede(self):
        """Crea una nueva sede"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nueva Sede")
        ventana.geometry("500x400")
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Header
        header = tk.Frame(ventana, bg=self.COLOR_PRIMARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="🏢 Nueva Sede", font=("Arial", 16, "bold"),
                bg=self.COLOR_PRIMARY, fg=self.COLOR_WHITE).pack(pady=15)
        
        # Formulario
        form = tk.Frame(ventana, bg=self.COLOR_WHITE, padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True)
        
        entries = {}
        campos = [
            ("Nombre Sede *", "nombre"),
            ("Dirección *", "direccion"),
            ("Ciudad *", "ciudad"),
            ("Capacidad *", "capacidad")
        ]
        
        for i, (label, key) in enumerate(campos):
            tk.Label(form, text=label, bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
                row=i*2, column=0, sticky=tk.W, pady=(5, 2))
            entry = ttk.Entry(form, width=40)
            entry.grid(row=i*2+1, column=0, sticky=tk.EW, pady=(0, 10))
            entries[key] = entry
        
        def guardar():
            try:
                nombre = entries['nombre'].get().strip()
                direccion = entries['direccion'].get().strip()
                ciudad = entries['ciudad'].get().strip()
                capacidad = entries['capacidad'].get().strip()
                
                if not all([nombre, direccion, ciudad, capacidad]):
                    raise ValueError("Complete todos los campos")
                
                try:
                    capacidad = int(capacidad)
                except:
                    raise ValueError("La capacidad debe ser un número")
                
                sede = Sede(nombre, direccion, ciudad, capacidad)
                self.sede_repo.agregar(sede)
                
                messagebox.showinfo("Éxito", "Sede creada correctamente")
                ventana.destroy()
                self.cargar_sedes()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Botones
        btn_frame = tk.Frame(form, bg=self.COLOR_WHITE)
        btn_frame.grid(row=len(campos)*2, column=0, pady=20)
        
        tk.Button(btn_frame, text="✔ Guardar", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✖ Cancelar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=5)

    def editar_sede(self):
        """Edita una sede"""
        seleccion = self.tabla_sedes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una sede")
            return
        
        item = self.tabla_sedes.item(seleccion[0])
        nombre_actual = item['values'][0]
        
        sede = self.sede_repo.buscar_por_nombre(nombre_actual)
        if not sede:
            messagebox.showerror("Error", "Sede no encontrada")
            return
        
        # Ventana edición
        ventana = tk.Toplevel(self.root)
        ventana.title("Editar Sede")
        ventana.geometry("500x300")
        ventana.transient(self.root)
        ventana.grab_set()
        
        # Header
        header = tk.Frame(ventana, bg=self.COLOR_SECONDARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="✏️ Editar Sede", font=("Arial", 16, "bold"),
                bg=self.COLOR_SECONDARY, fg=self.COLOR_WHITE).pack(pady=15)
        
        # Formulario
        form = tk.Frame(ventana, bg=self.COLOR_WHITE, padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True)
        
        # Solo se pueden editar dirección y capacidad
        tk.Label(form, text="Nombre:", bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(5, 2))
        tk.Label(form, text=sede.nombre, bg=self.COLOR_WHITE, fg=self.COLOR_TEXT_LIGHT).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        tk.Label(form, text="Nueva Dirección:", bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(5, 2))
        direccion_entry = ttk.Entry(form, width=40)
        direccion_entry.insert(0, sede.direccion)
        direccion_entry.grid(row=3, column=0, sticky=tk.EW, pady=(0, 10))
        
        tk.Label(form, text="Nueva Capacidad:", bg=self.COLOR_WHITE, font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky=tk.W, pady=(5, 2))
        capacidad_entry = ttk.Entry(form, width=40)
        capacidad_entry.insert(0, str(sede.capacidad))
        capacidad_entry.grid(row=5, column=0, sticky=tk.EW, pady=(0, 10))
        
        def guardar():
            try:
                direccion = direccion_entry.get().strip()
                capacidad = int(capacidad_entry.get().strip())
                
                self.sede_repo.actualizar(nombre_actual, direccion, capacidad)
                messagebox.showinfo("Éxito", "Sede actualizada")
                ventana.destroy()
                self.cargar_sedes()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Botones
        btn_frame = tk.Frame(form, bg=self.COLOR_WHITE)
        btn_frame.grid(row=6, column=0, pady=20)
        
        tk.Button(btn_frame, text="✔ Guardar", bg=self.COLOR_SUCCESS, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✖ Cancelar", bg=self.COLOR_DANGER, fg=self.COLOR_WHITE,
                 font=("Arial", 11, "bold"), relief=tk.FLAT, padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=5)

    def eliminar_sede(self):
        """Elimina una sede"""
        seleccion = self.tabla_sedes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una sede")
            return
        
        item = self.tabla_sedes.item(seleccion[0])
        nombre = item['values'][0]
        
        if messagebox.askyesno("Confirmar Eliminación",
                              f"¿Está seguro de eliminar la sede '{nombre}'?\n\nEsta acción no se puede deshacer.",
                              icon="warning"):
            try:
                self.sede_repo.eliminar(nombre)
                messagebox.showinfo("Éxito", "Sede eliminada")
                self.cargar_sedes()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def mostrar_estadisticas(self):
        """Muestra estadísticas del sistema"""
        self.limpiar_contenido()
        
        tk.Label(
            self.content_frame,
            text="📊 Estadísticas del Sistema",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_WHITE,
            fg=self.COLOR_PRIMARY
        ).pack(pady=30)
        
        # Obtener datos
        inscripciones = self.inscripcion_service.listar()
        usuarios = self.usuario_repo.listar_postulantes()
        sedes = self.sede_repo.listar_todas()
        
        pendientes = len([i for i in inscripciones if i['estado_inscripcion'] == 'PENDIENTE'])
        aprobadas = len([i for i in inscripciones if i['estado_inscripcion'] == 'APROBADA'])
        rechazadas = len([i for i in inscripciones if i['estado_inscripcion'] == 'RECHAZADA'])
        
        # Área de texto
        text_frame = tk.Frame(self.content_frame, bg=self.COLOR_WHITE)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Courier", 11))
        text.pack(fill=tk.BOTH, expand=True)
        
        stats = f"""
╔═══════════════════════════════════════════════════════╗
║        ESTADÍSTICAS GENERALES DEL SISTEMA            ║
╚═══════════════════════════════════════════════════════╝

👥 USUARIOS
   • Total de postulantes: {len(usuarios)}
   
📋 INSCRIPCIONES
   • Total: {len(inscripciones)}
   • Pendientes: {pendientes}
   • Aprobadas: {aprobadas}
   • Rechazadas: {rechazadas}

🏢 SEDES
   • Total de sedes: {len(sedes)}
   • Capacidad total: {sum(s.capacidad for s in sedes)}

📊 PORCENTAJES
   • Tasa de aprobación: {round(aprobadas/len(inscripciones)*100 if inscripciones else 0, 1)}%
   • Tasa de rechazo: {round(rechazadas/len(inscripciones)*100 if inscripciones else 0, 1)}%
   • Pendientes: {round(pendientes/len(inscripciones)*100 if inscripciones else 0, 1)}%

═══════════════════════════════════════════════════════
        """
        
        text.insert("1.0", stats)
        text.config(state=tk.DISABLED)

    def cerrar_sesion(self):
        """Cierra la sesión del administrador"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.root.destroy()
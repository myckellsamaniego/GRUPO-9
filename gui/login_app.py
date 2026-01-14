"""
Pantalla de Acceso/Bienvenida - Sistema Simplificado
Sistema de Admisión ULEAM 2026
"""
import tkinter as tk
from tkinter import messagebox, ttk

from gui.app_admin import AdminApp
from gui.app_postulante import PostulanteApp
from gui.registro import RegistroApp


class LoginMejoradoApp:
    """
    Pantalla de bienvenida con opciones de:
    1. Iniciar Sesión (usuarios registrados)
    2. Registrarse (formulario básico - solo cuenta)
    """

    def __init__(self, root, auth_service, usuario_repo):
        self.root = root
        self.auth_service = auth_service
        self.usuario_repo = usuario_repo

        self.root.title("Sistema de Admisión ULEAM 2026")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Colores institucionales
        self.color_principal = "#1e3a8a"
        self.color_secundario = "#3b82f6"
        self.color_acento = "#10b981"
        
        self.centrar_ventana()
        self.mostrar_alerta_fechas()
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 900
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def mostrar_alerta_fechas(self):
        """Muestra modal con fechas importantes del proceso"""
        modal = tk.Toplevel(self.root)
        modal.title("Fechas Importantes")
        modal.geometry("500x350")
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()
        
        # Centrar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (250)
        y = (modal.winfo_screenheight() // 2) - (175)
        modal.geometry(f'500x350+{x}+{y}')
        
        # Contenido
        header = tk.Frame(modal, bg="#dc2626", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="⚠️ FECHAS IMPORTANTES",
            font=("Arial", 16, "bold"),
            bg="#dc2626",
            fg="white"
        ).pack(pady=15)
        
        content = tk.Frame(modal, bg="white", padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        info_text = """
📅 PROCESO DE ADMISIÓN 2026

• Inscripciones Abiertas: Hasta el 31 de Marzo 2026
• Publicación de Resultados: 15 de Abril 2026
• Inicio de evaluaciones: Mayo 2026

⚡ IMPORTANTE:
✓ Complete todos los pasos del registro
✓ Revise su correo electrónico frecuentemente
✓ Los cupos son limitados
✓ La inscripción NO garantiza un cupo

📧 Para consultas: admisiones@uleam.edu.ec
        """
        
        tk.Label(
            content,
            text=info_text,
            font=("Arial", 11),
            justify=tk.LEFT,
            bg="white"
        ).pack(pady=10)
        
        tk.Button(
            modal,
            text="✓ Entendido",
            command=modal.destroy,
            bg=self.color_acento,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(pady=15)

    def crear_interfaz(self):
        """Crea la interfaz principal de bienvenida"""
        
        # ========== HEADER CON LOGO ==========
        header = tk.Frame(self.root, bg=self.color_principal, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=self.color_principal)
        title_frame.pack(expand=True)
        
        tk.Label(
            title_frame,
            text="UNIVERSIDAD LAICA ELOY ALFARO DE MANABÍ",
            font=("Arial", 14, "bold"),
            bg=self.color_principal,
            fg="white"
        ).pack(pady=(20, 5))
        
        tk.Label(
            title_frame,
            text="Sistema de Registro Único - Proceso de Admisión 2026",
            font=("Arial", 11),
            bg=self.color_principal,
            fg="#e5e7eb"
        ).pack()
        
        # ========== CONTENEDOR PRINCIPAL ==========
        main_container = tk.Frame(self.root, bg="#f3f4f6")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje de bienvenida
        welcome_frame = tk.Frame(main_container, bg="#f3f4f6")
        welcome_frame.pack(pady=30)
        
        tk.Label(
            welcome_frame,
            text="¡Bienvenido al Proceso de Admisión!",
            font=("Arial", 18, "bold"),
            bg="#f3f4f6",
            fg="#111827"
        ).pack()
        
        tk.Label(
            welcome_frame,
            text="Seleccione una opción para continuar",
            font=("Arial", 12),
            bg="#f3f4f6",
            fg="#6b7280"
        ).pack(pady=5)
        
        # ========== OPCIONES DE ACCESO ==========
        options_frame = tk.Frame(main_container, bg="#f3f4f6")
        options_frame.pack(pady=20)
        
        # Opción 1: Iniciar Sesión
        login_card = self.crear_tarjeta_opcion(
            options_frame,
            "🔐 INICIAR SESIÓN",
            "Si ya tiene una cuenta registrada",
            "Usuarios con cuenta existente",
            self.mostrar_formulario_login
        )
        login_card.grid(row=0, column=0, padx=15)
        
        # Separador
        tk.Label(
            options_frame,
            text="O",
            font=("Arial", 14, "bold"),
            bg="#f3f4f6",
            fg="#9ca3af"
        ).grid(row=0, column=1, padx=10)
        
        # Opción 2: Registrarse
        register_card = self.crear_tarjeta_opcion(
            options_frame,
            "➕ REGISTRARSE",
            "Si es su primera vez en el sistema",
            "Crear cuenta nueva - Registro básico",
            self.mostrar_registro_basico
        )
        register_card.grid(row=0, column=2, padx=15)
        
        # ========== FOOTER ==========
        footer = tk.Frame(self.root, bg="#1f2937", height=50)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Label(
            footer,
            text="© 2026 ULEAM - Universidad Laica Eloy Alfaro de Manabí",
            font=("Arial", 9),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            footer,
            text="📞 Soporte: (05) 2623-740 | 📧 admisiones@uleam.edu.ec",
            font=("Arial", 9),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack(side=tk.RIGHT, padx=20)

    def crear_tarjeta_opcion(self, parent, titulo, subtitulo, descripcion, comando):
        """Crea una tarjeta de opción clickeable"""
        card = tk.Frame(
            parent,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        card.bind("<Button-1>", lambda e: comando())
        
        # Hacer que todos los elementos internos también sean clickeables
        def bind_click(widget):
            widget.bind("<Button-1>", lambda e: comando())
            for child in widget.winfo_children():
                bind_click(child)
        
        inner_frame = tk.Frame(card, bg="white", padx=30, pady=30)
        inner_frame.pack()
        bind_click(inner_frame)
        
        # Título
        title_label = tk.Label(
            inner_frame,
            text=titulo,
            font=("Arial", 16, "bold"),
            bg="white",
            fg=self.color_principal
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            inner_frame,
            text=subtitulo,
            font=("Arial", 11),
            bg="white",
            fg="#4b5563"
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Descripción
        desc_label = tk.Label(
            inner_frame,
            text=descripcion,
            font=("Arial", 9),
            bg="white",
            fg="#9ca3af"
        )
        desc_label.pack(pady=(0, 15))
        
        # Botón
        btn = tk.Button(
            inner_frame,
            text="Continuar →",
            font=("Arial", 10, "bold"),
            bg=self.color_secundario,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=comando
        )
        btn.pack()
        
        # Efecto hover
        def on_enter(e):
            card.config(bg="#eff6ff", borderwidth=3)
            inner_frame.config(bg="#eff6ff")
            for widget in inner_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="#eff6ff")
        
        def on_leave(e):
            card.config(bg="white", borderwidth=2)
            inner_frame.config(bg="white")
            for widget in inner_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="white")
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card

    def mostrar_formulario_login(self):
        """Muestra el formulario de inicio de sesión"""
        login_window = tk.Toplevel(self.root)
        login_window.title("Iniciar Sesión - ULEAM")
        login_window.geometry("450x400")
        login_window.resizable(False, False)
        login_window.transient(self.root)
        login_window.grab_set()
        
        # Centrar
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - 225
        y = (login_window.winfo_screenheight() // 2) - 200
        login_window.geometry(f'450x400+{x}+{y}')
        
        # Header
        header = tk.Frame(login_window, bg=self.color_principal, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔐 Iniciar Sesión",
            font=("Arial", 16, "bold"),
            bg=self.color_principal,
            fg="white"
        ).pack(pady=25)
        
        # Formulario
        form_frame = tk.Frame(login_window, bg="white", padx=40, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Correo
        tk.Label(
            form_frame,
            text="Correo Electrónico:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        correo_entry = ttk.Entry(form_frame, width=35, font=("Arial", 11))
        correo_entry.pack(pady=(0, 15))
        correo_entry.focus()
        
        # Contraseña
        tk.Label(
            form_frame,
            text="Contraseña:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        password_entry = ttk.Entry(form_frame, show="●", width=35, font=("Arial", 11))
        password_entry.pack(pady=(0, 20))
        
        # Info admin
        info_frame = tk.Frame(form_frame, bg="#eff6ff", relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        #tk.Label(
        #    info_frame,
        #    text="💡 Credenciales de Administrador:",
        #    font=("Arial", 9, "bold"),
        #    bg="#eff6ff",
        #    fg="#1e40af"
        #).pack(pady=(5, 2))
        
        #tk.Label(
        #    info_frame,
        #    text="admin@uleam.edu.ec / admin123",
        #    font=("Arial", 9),
        #    bg="#eff6ff",
        #    fg="#6b7280"
        #).pack(pady=(0, 5))
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack()
        
        def realizar_login():
            try:
                correo = correo_entry.get().strip()
                password = password_entry.get()
                
                if not correo or not password:
                    raise ValueError("Complete todos los campos")
                
                if "@" not in correo:
                    raise ValueError("Ingrese un correo válido")
                
                # Autenticar
                usuario = self.auth_service.login(correo, password)
                
                # Cerrar ventanas
                login_window.destroy()
                self.root.destroy()
                
                # Abrir app correspondiente
                root = tk.Tk()
                if usuario.obtener_tipo() == "ADMIN":
                    AdminApp(root, usuario)
                else:
                    PostulanteApp(root, usuario)
                root.mainloop()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                password_entry.delete(0, tk.END)
        
        tk.Button(
            btn_frame,
            text="✓ Ingresar",
            command=realizar_login,
            bg=self.color_acento,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            btn_frame,
            text="✗ Cancelar",
            command=login_window.destroy,
            bg="#6b7280",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=1, padx=5)
        
        # Bind Enter
        login_window.bind('<Return>', lambda e: realizar_login())

    def mostrar_registro_basico(self):
        """Muestra ventana para crear cuenta básica"""
        # Abrir ventana de registro básico
        registro_window = tk.Toplevel(self.root)
        RegistroApp(registro_window, self.usuario_repo)
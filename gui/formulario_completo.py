# -*- coding: utf-8 -*-
"""
Formulario de Registro Completo Multi-Paso
Similar al Sistema Nacional de Nivelación y Admisión
ACTUALIZADO: Ahora puede usarse para completar perfil de postulantes existentes
"""
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

from models.datos_personales_completos import DatosPersonalesCompletos
from factory.fabrica_usuarios import FabricaUsuarios


class FormularioCompletoApp:
    """Formulario de registro por pasos con toda la información del postulante"""

    def __init__(self, root, usuario_repo, cedula_validada=None, postulante_existente=None):
        self.root = root
        self.usuario_repo = usuario_repo
        self.fabrica = FabricaUsuarios()
        self.cedula_validada = cedula_validada
        self.postulante_existente = postulante_existente
        
        # Paso actual del formulario (0-5)
        self.paso_actual = 0
        
        # Diccionario para almacenar todos los datos
        self.datos_formulario = {
            'paso1': {},
            'paso2': {},
            'paso3': {},
            'paso4': {},
            'paso5': {},
            'paso6': {}
        }
        
        # Si hay postulante existente, pre-cargar sus datos básicos
        if postulante_existente:
            self.precargar_datos_existentes()

        self.root.title("Registro Completo - Sistema ULEAM 2026")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        self.centrar_ventana()
        self.crear_interfaz()

    def precargar_datos_existentes(self):
        """Pre-carga los datos básicos del postulante existente"""
        datos = self.postulante_existente.datos_personales
        
        # Pre-cargar correo y otros datos básicos si existen
        self.datos_formulario['paso2']['correo'] = datos.correo if hasattr(datos, 'correo') else ""
        self.datos_formulario['paso2']['celular'] = datos.celular if hasattr(datos, 'celular') else ""

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        """Crea la interfaz principal con barra de progreso y contenedor"""
        
        # ========== ALERTA SUPERIOR ==========
        alerta_frame = tk.Frame(self.root, bg="#fef3c7", height=50)
        alerta_frame.pack(fill=tk.X)
        alerta_frame.pack_propagate(False)
        
        mensaje_alerta = "ℹ️ Complete todos los pasos para finalizar su registro en el sistema."
        if self.postulante_existente:
            mensaje_alerta = "ℹ️ Complete su perfil para acceder a todas las funcionalidades del sistema."
        
        tk.Label(
            alerta_frame,
            text=mensaje_alerta,
            font=("Arial", 10),
            bg="#fef3c7",
            fg="#92400e"
        ).pack(pady=15, padx=20)
        
        # ========== BARRA DE PROGRESO ==========
        self.crear_barra_progreso()
        
        # ========== CONTENEDOR PRINCIPAL ==========
        self.contenedor = tk.Frame(self.root, bg="white")
        self.contenedor.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ========== BOTONES DE NAVEGACIÓN ==========
        self.botones_frame = tk.Frame(self.root, bg="#f3f4f6", height=70)
        self.botones_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.botones_frame.pack_propagate(False)
        
        btn_container = tk.Frame(self.botones_frame, bg="#f3f4f6")
        btn_container.pack(expand=True)
        
        self.btn_anterior = tk.Button(
            btn_container,
            text="← Anterior",
            command=self.paso_anterior,
            bg="#6b7280",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_anterior.grid(row=0, column=0, padx=10)
        
        self.btn_siguiente = tk.Button(
            btn_container,
            text="Siguiente →",
            command=self.paso_siguiente,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.btn_siguiente.grid(row=0, column=1, padx=10)
        
        tk.Button(
            btn_container,
            text="✗ Cancelar",
            command=self.cancelar,
            bg="#ef4444",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2"
        ).grid(row=0, column=2, padx=10)
        
        # Mostrar primer paso
        self.mostrar_paso(0)

    def crear_barra_progreso(self):
        """Crea la barra de progreso con los 6 pasos"""
        progreso_frame = tk.Frame(self.root, bg="white", height=120)
        progreso_frame.pack(fill=tk.X)
        progreso_frame.pack_propagate(False)
        
        container = tk.Frame(progreso_frame, bg="white")
        container.pack(expand=True, pady=20)
        
        self.pasos = [
            "INFORMACIÓN\nPERSONAL -\nIDENTIFICACIÓN",
            "REFERENCIA-\nCONTACTOS",
            "AUTOIDENTIFICACIÓN\nÉTNICA",
            "DISCAPACIDAD",
            "INFORMACIÓN\nTECNOLÓGICA",
            "EDUCACIÓN"
        ]
        
        self.circulos = []
        self.lineas = []
        self.labels = []
        
        for i, paso in enumerate(self.pasos):
            if i > 0:
                linea = tk.Canvas(container, width=80, height=4, bg="white", highlightthickness=0)
                linea.create_rectangle(0, 0, 80, 4, fill="#d1d5db", outline="")
                linea.grid(row=0, column=i*2-1, padx=0)
                self.lineas.append(linea)
            
            paso_frame = tk.Frame(container, bg="white")
            paso_frame.grid(row=0, column=i*2, padx=5)
            
            circulo = tk.Canvas(paso_frame, width=40, height=40, bg="white", highlightthickness=0)
            circulo.create_oval(2, 2, 38, 38, fill="#d1d5db", outline="#9ca3af", width=2)
            circulo.pack()
            self.circulos.append(circulo)
            
            label = tk.Label(
                paso_frame,
                text=paso,
                font=("Arial", 8),
                bg="white",
                fg="#9ca3af",
                justify=tk.CENTER
            )
            label.pack(pady=(5, 0))
            self.labels.append(label)
    
    def actualizar_barra_progreso(self):
        """Actualiza el estado visual de la barra de progreso"""
        for i in range(len(self.pasos)):
            if i < self.paso_actual:
                self.circulos[i].delete("all")
                self.circulos[i].create_oval(2, 2, 38, 38, fill="#10b981", outline="#059669", width=2)
                self.circulos[i].create_text(20, 20, text="✓", font=("Arial", 18, "bold"), fill="white")
                self.labels[i].config(fg="#10b981")
                
                if i < len(self.lineas):
                    self.lineas[i].delete("all")
                    self.lineas[i].create_rectangle(0, 0, 80, 4, fill="#10b981", outline="")
                    
            elif i == self.paso_actual:
                self.circulos[i].delete("all")
                self.circulos[i].create_oval(2, 2, 38, 38, fill="#3b82f6", outline="#2563eb", width=2)
                self.circulos[i].create_text(20, 20, text=str(i+1), font=("Arial", 14, "bold"), fill="white")
                self.labels[i].config(fg="#3b82f6", font=("Arial", 8, "bold"))
            else:
                self.circulos[i].delete("all")
                self.circulos[i].create_oval(2, 2, 38, 38, fill="#f3f4f6", outline="#d1d5db", width=2)
                self.circulos[i].create_text(20, 20, text=str(i+1), font=("Arial", 12), fill="#9ca3af")
                self.labels[i].config(fg="#9ca3af", font=("Arial", 8))
    
    def limpiar_contenedor(self):
        """Limpia el contenedor principal"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()
    
    def mostrar_paso(self, paso):
        """Muestra el paso correspondiente"""
        self.limpiar_contenedor()
        self.paso_actual = paso
        self.actualizar_barra_progreso()
        
        if paso == 0:
            self.btn_anterior.config(state=tk.DISABLED)
        else:
            self.btn_anterior.config(state=tk.NORMAL)
        
        if paso == 5:
            self.btn_siguiente.config(text="✓ Finalizar Registro")
        else:
            self.btn_siguiente.config(text="Siguiente →")
        
        if paso == 0:
            self.crear_paso1_identificacion()
        elif paso == 1:
            self.crear_paso2_referencia()
        elif paso == 2:
            self.crear_paso3_etnia()
        elif paso == 3:
            self.crear_paso4_discapacidad()
        elif paso == 4:
            self.crear_paso5_tecnologia()
        elif paso == 5:
            self.crear_paso6_educacion()
    
    def crear_paso1_identificacion(self):
        """Paso 1: Información Personal e Identificación"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Identificación",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        self.entries_paso1 = {}
        row = 0
        
        # Cédula bloqueada
        tk.Label(form_frame, text="Identificación:", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        cedula_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        if self.cedula_validada:
            cedula_entry.insert(0, self.cedula_validada)
            cedula_entry.config(state="disabled")
        cedula_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso1['cedula'] = cedula_entry
        row += 1
        
        # Nombre completo (calculado)
        tk.Label(form_frame, text="Nombre completo:", font=("Arial", 10), bg="white", fg="#6b7280").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        self.nombre_completo_label = ttk.Label(form_frame, text="", font=("Arial", 10), background="white")
        self.nombre_completo_label.grid(row=row, column=0, sticky=tk.W, pady=(0, 15))
        row += 1
        
        # Apellidos
        tk.Label(form_frame, text="Apellidos: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        apellidos_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        apellidos_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        apellidos_entry.bind("<KeyRelease>", self.actualizar_nombre_completo)
        self.entries_paso1['apellidos'] = apellidos_entry
        row += 1
        
        # Nombres
        tk.Label(form_frame, text="Nombres: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        nombres_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        nombres_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        nombres_entry.bind("<KeyRelease>", self.actualizar_nombre_completo)
        self.entries_paso1['nombres'] = nombres_entry
        row += 1
        
        # Fecha de nacimiento
        tk.Label(form_frame, text="Fecha de nacimiento: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        fecha_nac = DateEntry(form_frame, width=47, font=("Arial", 10), date_pattern='dd/mm/yyyy',
                              maxdate=datetime.now(), year=2005, month=1, day=1)
        fecha_nac.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso1['fecha_nacimiento'] = fecha_nac
        row += 1
        
        # Estado civil
        tk.Label(form_frame, text="Estado civil: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        estado_civil = ttk.Combobox(form_frame, width=47, font=("Arial", 10), state="readonly",
                                    values=["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión libre"])
        estado_civil.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso1['estado_civil'] = estado_civil
        row += 1
        
        # Sexo
        tk.Label(form_frame, text="Sexo: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        sexo_frame = tk.Frame(form_frame, bg="white")
        sexo_frame.grid(row=row, column=0, sticky=tk.W, pady=(0, 15))
        self.sexo_var = tk.StringVar(value="")
        tk.Radiobutton(sexo_frame, text="Masculino", variable=self.sexo_var, value="Masculino", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(sexo_frame, text="Femenino", variable=self.sexo_var, value="Femenino", bg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        row += 1
        
        # Identidad de género
        tk.Label(form_frame, text="Tipo de identidad de género: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        identidad_genero = ttk.Combobox(form_frame, width=47, font=("Arial", 10), state="readonly",
                                        values=["Hombre", "Mujer", "Transgénero", "Prefiero no decirlo", "Otro"])
        identidad_genero.grid(row=row, column=0, sticky=tk.EW, pady=(0, 20))
        self.entries_paso1['identidad_genero'] = identidad_genero
        
        form_frame.columnconfigure(0, weight=1)
    
    def actualizar_nombre_completo(self, event=None):
        """Actualiza el campo de nombre completo automáticamente"""
        nombres = self.entries_paso1.get('nombres', None)
        apellidos = self.entries_paso1.get('apellidos', None)
        
        if nombres and apellidos:
            nombre = nombres.get().strip()
            apellido = apellidos.get().strip()
            if nombre and apellido:
                self.nombre_completo_label.config(text=f"{nombre} {apellido}")

    def crear_paso2_referencia(self):
        """Paso 2: Referencia - Contactos"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Referencia - Contactos",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        self.entries_paso2 = {}
        row = 0
        
        # Correo
        tk.Label(form_frame, text="Correo electrónico: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        correo_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        if self.postulante_existente:
            correo_entry.insert(0, self.datos_formulario['paso2'].get('correo', ''))
        correo_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['correo'] = correo_entry
        row += 1
        
        # Celular
        tk.Label(form_frame, text="Celular: *", font=("Arial", 10, "bold"), bg="white", fg="#1e40af").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        celular_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        if self.postulante_existente:
            celular_entry.insert(0, self.datos_formulario['paso2'].get('celular', ''))
        celular_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['celular'] = celular_entry
        row += 1
        
        # Provincia
        tk.Label(form_frame, text="Provincia:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        provincia = ttk.Combobox(form_frame, width=47, font=("Arial", 10), state="readonly",
                                values=["Manabí", "Guayas", "Pichincha", "Azuay", "El Oro", "Los Ríos", "Otra"])
        provincia.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['provincia'] = provincia
        row += 1
        
        # Cantón
        tk.Label(form_frame, text="Cantón:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        canton_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        canton_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['canton'] = canton_entry
        row += 1
        
        # Parroquia
        tk.Label(form_frame, text="Parroquia:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        parroquia_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        parroquia_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['parroquia'] = parroquia_entry
        row += 1
        
        # Barrio
        tk.Label(form_frame, text="Barrio:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        barrio_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        barrio_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['barrio'] = barrio_entry
        row += 1
        
        # Calle principal
        tk.Label(form_frame, text="Calle principal:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        calle_principal = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        calle_principal.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['calle_principal'] = calle_principal
        row += 1
        
        # Calle secundaria
        tk.Label(form_frame, text="Calle secundaria:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        calle_secundaria = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        calle_secundaria.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries_paso2['calle_secundaria'] = calle_secundaria
        row += 1
        
        # Número de casa
        tk.Label(form_frame, text="Número de casa:", font=("Arial", 10), bg="white").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1
        numero_casa = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        numero_casa.grid(row=row, column=0, sticky=tk.EW, pady=(0, 20))
        self.entries_paso2['numero_casa'] = numero_casa
        
        form_frame.columnconfigure(0, weight=1)

    def crear_paso3_etnia(self):
        """Paso 3: Autoidentificación Étnica"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Autoidentificación Étnica",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            form_frame,
            text="¿Cómo se autoidentifica según su cultura y costumbres?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(10, 20), anchor=tk.W)
        
        self.etnia_var = tk.StringVar(value="")
        
        opciones_etnia = [
            "Mestizo/a",
            "Montubio/a",
            "Afroecuatoriano/a",
            "Indígena",
            "Blanco/a",
            "Otro"
        ]
        
        for opcion in opciones_etnia:
            tk.Radiobutton(
                form_frame,
                text=opcion,
                variable=self.etnia_var,
                value=opcion,
                bg="white",
                font=("Arial", 11),
                anchor=tk.W
            ).pack(pady=8, padx=20, anchor=tk.W)
        
        form_frame.columnconfigure(0, weight=1)

    def crear_paso4_discapacidad(self):
        """Paso 4: Discapacidad"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Discapacidad",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            form_frame,
            text="¿Presenta algún tipo de discapacidad?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(10, 20), anchor=tk.W)
        
        self.discapacidad_var = tk.BooleanVar(value=False)
        
        tk.Radiobutton(
            form_frame,
            text="No",
            variable=self.discapacidad_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            form_frame,
            text="Sí",
            variable=self.discapacidad_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Label(
            form_frame,
            text=" ",
            bg="white"
        ).pack(pady=10)
        
        tk.Label(
            form_frame,
            text="¿Requiere apoyo en el proceso de evaluación?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(10, 20), anchor=tk.W)
        
        self.apoyo_var = tk.BooleanVar(value=False)
        
        tk.Radiobutton(
            form_frame,
            text="No",
            variable=self.apoyo_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            form_frame,
            text="Sí",
            variable=self.apoyo_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(pady=5, padx=20, anchor=tk.W)
        
        form_frame.columnconfigure(0, weight=1)

    def crear_paso5_tecnologia(self):
        """Paso 5: Información Tecnológica"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Información Tecnológica",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Internet
        tk.Label(
            form_frame,
            text="¿Dispone de internet en su domicilio?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(10, 15), anchor=tk.W)
        
        self.internet_var = tk.BooleanVar(value=False)
        
        internet_frame = tk.Frame(form_frame, bg="white")
        internet_frame.pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            internet_frame,
            text="Sí",
            variable=self.internet_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            internet_frame,
            text="No",
            variable=self.internet_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        # Computadora
        tk.Label(
            form_frame,
            text="¿Dispone de una computadora funcional?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(20, 15), anchor=tk.W)
        
        self.computadora_var = tk.BooleanVar(value=False)
        
        comp_frame = tk.Frame(form_frame, bg="white")
        comp_frame.pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            comp_frame,
            text="Sí",
            variable=self.computadora_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            comp_frame,
            text="No",
            variable=self.computadora_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        # Sistema operativo
        tk.Label(
            form_frame,
            text="Sistema operativo:",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(20, 10), anchor=tk.W)
        
        self.so_combo = ttk.Combobox(
            form_frame,
            values=["Windows", "macOS", "Linux", "Otro", "No aplica"],
            state="readonly",
            width=47,
            font=("Arial", 10)
        )
        self.so_combo.pack(pady=5, anchor=tk.W)
        self.so_combo.set("No aplica")
        
        # Cámara web
        tk.Label(
            form_frame,
            text="¿Dispone de cámara web?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(20, 15), anchor=tk.W)
        
        self.camara_var = tk.BooleanVar(value=False)
        
        cam_frame = tk.Frame(form_frame, bg="white")
        cam_frame.pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            cam_frame,
            text="Sí",
            variable=self.camara_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            cam_frame,
            text="No",
            variable=self.camara_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        form_frame.columnconfigure(0, weight=1)

    def crear_paso6_educacion(self):
        """Paso 6: Educación"""
        canvas = tk.Canvas(self.contenedor, bg="white")
        scrollbar = ttk.Scrollbar(self.contenedor, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(
            scrollable_frame,
            text="Educación",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1e40af"
        ).pack(pady=20, padx=40, anchor=tk.W)
        
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Orientación vocacional
        tk.Label(
            form_frame,
            text="¿Ha recibido orientación vocacional?",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(pady=(10, 15), anchor=tk.W)
        
        self.orientacion_var = tk.BooleanVar(value=False)
        
        or_frame = tk.Frame(form_frame, bg="white")
        or_frame.pack(pady=5, padx=20, anchor=tk.W)
        
        tk.Radiobutton(
            or_frame,
            text="Sí",
            variable=self.orientacion_var,
            value=True,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            or_frame,
            text="No",
            variable=self.orientacion_var,
            value=False,
            bg="white",
            font=("Arial", 11)
        ).pack(side=tk.LEFT)
        
        # Institución a la que aspira
        tk.Label(
            form_frame,
            text="Institución a la que aspira ingresar:",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(20, 10), anchor=tk.W)
        
        self.institucion_entry = ttk.Entry(form_frame, width=50, font=("Arial", 10))
        self.institucion_entry.insert(0, "Universidad Laica Eloy Alfaro de Manabí - ULEAM")
        self.institucion_entry.pack(pady=5, anchor=tk.W)
        
        # Nivel máximo de estudios
        tk.Label(
            form_frame,
            text="Nivel máximo de estudios alcanzado:",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(20, 10), anchor=tk.W)
        
        self.nivel_combo = ttk.Combobox(
            form_frame,
            values=["Bachillerato", "Tercer nivel", "Cuarto nivel", "Otro"],
            state="readonly",
            width=47,
            font=("Arial", 10)
        )
        self.nivel_combo.pack(pady=5, anchor=tk.W)
        self.nivel_combo.set("Bachillerato")
        
        # Razón para estudiar
        tk.Label(
            form_frame,
            text="¿Por qué desea estudiar esta carrera?",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(20, 10), anchor=tk.W)
        
        self.razon_text = tk.Text(form_frame, width=58, height=5, font=("Arial", 10), wrap=tk.WORD)
        self.razon_text.pack(pady=5, anchor=tk.W)
        
        form_frame.columnconfigure(0, weight=1)

    def validar_paso_actual(self):
        """Valida que el paso actual esté completo"""
        if self.paso_actual == 0:
            # Paso 1: Identificación
            if not self.entries_paso1['nombres'].get().strip():
                raise ValueError("Debe ingresar sus nombres")
            if not self.entries_paso1['apellidos'].get().strip():
                raise ValueError("Debe ingresar sus apellidos")
            if not self.entries_paso1['estado_civil'].get():
                raise ValueError("Debe seleccionar su estado civil")
            if not self.sexo_var.get():
                raise ValueError("Debe seleccionar su sexo")
            if not self.entries_paso1['identidad_genero'].get():
                raise ValueError("Debe seleccionar su identidad de género")
                
        elif self.paso_actual == 1:
            # Paso 2: Contactos
            if not self.entries_paso2['correo'].get().strip():
                raise ValueError("Debe ingresar su correo electrónico")
            if "@" not in self.entries_paso2['correo'].get():
                raise ValueError("El correo electrónico no es válido")
            if not self.entries_paso2['celular'].get().strip():
                raise ValueError("Debe ingresar su número de celular")
                
        elif self.paso_actual == 2:
            # Paso 3: Etnia
            if not self.etnia_var.get():
                raise ValueError("Debe seleccionar una opción de autoidentificación étnica")

    def guardar_datos_paso(self):
        """Guarda los datos del paso actual"""
        if self.paso_actual == 0:
            self.datos_formulario['paso1'] = {
                'cedula': self.cedula_validada if self.cedula_validada else self.entries_paso1['cedula'].get(),
                'nombres': self.entries_paso1['nombres'].get().strip(),
                'apellidos': self.entries_paso1['apellidos'].get().strip(),
                'fecha_nacimiento': self.entries_paso1['fecha_nacimiento'].get_date(),
                'estado_civil': self.entries_paso1['estado_civil'].get(),
                'sexo': self.sexo_var.get(),
                'identidad_genero': self.entries_paso1['identidad_genero'].get()
            }
        elif self.paso_actual == 1:
            self.datos_formulario['paso2'] = {
                'correo': self.entries_paso2['correo'].get().strip(),
                'celular': self.entries_paso2['celular'].get().strip(),
                'provincia': self.entries_paso2['provincia'].get(),
                'canton': self.entries_paso2['canton'].get().strip(),
                'parroquia': self.entries_paso2['parroquia'].get().strip(),
                'barrio': self.entries_paso2['barrio'].get().strip(),
                'calle_principal': self.entries_paso2['calle_principal'].get().strip(),
                'calle_secundaria': self.entries_paso2['calle_secundaria'].get().strip(),
                'numero_casa': self.entries_paso2['numero_casa'].get().strip()
            }
        elif self.paso_actual == 2:
            self.datos_formulario['paso3'] = {
                'etnia': self.etnia_var.get()
            }
        elif self.paso_actual == 3:
            self.datos_formulario['paso4'] = {
                'tiene_discapacidad': self.discapacidad_var.get(),
                'requiere_apoyo': self.apoyo_var.get()
            }
        elif self.paso_actual == 4:
            self.datos_formulario['paso5'] = {
                'internet': self.internet_var.get(),
                'computadora': self.computadora_var.get(),
                'sistema_operativo': self.so_combo.get(),
                'camara_web': self.camara_var.get()
            }
        elif self.paso_actual == 5:
            self.datos_formulario['paso6'] = {
                'orientacion_vocacional': self.orientacion_var.get(),
                'institucion': self.institucion_entry.get().strip(),
                'nivel_estudios': self.nivel_combo.get(),
                'razon_carrera': self.razon_text.get("1.0", tk.END).strip()
            }

    def paso_siguiente(self):
        """Avanza al siguiente paso o finaliza el registro"""
        try:
            # Validar paso actual
            self.validar_paso_actual()
            
            # Guardar datos del paso
            self.guardar_datos_paso()
            
            if self.paso_actual < 5:
                # Avanzar al siguiente paso
                self.mostrar_paso(self.paso_actual + 1)
            else:
                # Último paso - finalizar registro
                self.finalizar_registro()
                
        except ValueError as e:
            messagebox.showerror("Validación", str(e))

    def paso_anterior(self):
        """Retrocede al paso anterior"""
        if self.paso_actual > 0:
            # Guardar datos antes de retroceder
            try:
                self.guardar_datos_paso()
            except:
                pass  # Ignorar errores al retroceder
            
            self.mostrar_paso(self.paso_actual - 1)

    def cancelar(self):
        """Cancela el registro"""
        respuesta = messagebox.askyesno(
            "Cancelar Registro",
            "¿Está seguro de que desea cancelar el registro?\n\n"
            "Se perderán todos los datos ingresados."
        )
        if respuesta:
            self.root.destroy()

    def finalizar_registro(self):
        """Procesa el registro completo del usuario"""
        try:
            datos = DatosPersonalesCompletos(
                # Paso 1
                nombre=self.datos_formulario['paso1']['nombres'],
                apellidos=self.datos_formulario['paso1']['apellidos'],
                cedula=self.datos_formulario['paso1']['cedula'],
                fecha_nacimiento=self.datos_formulario['paso1']['fecha_nacimiento'],
                estado_civil=self.datos_formulario['paso1']['estado_civil'],
                sexo=self.datos_formulario['paso1']['sexo'],
                identidad_genero=self.datos_formulario['paso1']['identidad_genero'],
                
                # Paso 2
                correo=self.datos_formulario['paso2']['correo'],
                celular=self.datos_formulario['paso2']['celular'],
                provincia=self.datos_formulario['paso2']['provincia'],
                canton=self.datos_formulario['paso2']['canton'],
                parroquia=self.datos_formulario['paso2']['parroquia'],
                barrio=self.datos_formulario['paso2']['barrio'],
                calle_principal=self.datos_formulario['paso2']['calle_principal'],
                calle_secundaria=self.datos_formulario['paso2']['calle_secundaria'],
                numero_casa=self.datos_formulario['paso2']['numero_casa'],
                
                # Paso 3
                etnia=self.datos_formulario['paso3']['etnia'],
                
                # Paso 4
                discapacidad=self.datos_formulario['paso4']['tiene_discapacidad'],
                requiere_apoyo_evaluacion=self.datos_formulario['paso4']['requiere_apoyo'],
                
                # Paso 5
                internet_domicilio=self.datos_formulario['paso5']['internet'],
                computadora_funcional=self.datos_formulario['paso5']['computadora'],
                sistema_operativo=self.datos_formulario['paso5']['sistema_operativo'],
                camara_web=self.datos_formulario['paso5']['camara_web'],
                
                # Paso 6
                orientacion_vocacional=self.datos_formulario['paso6']['orientacion_vocacional'],
                institucion_aspirar=self.datos_formulario['paso6']['institucion'],
                nivel_maximo_estudios=self.datos_formulario['paso6']['nivel_estudios'],
                razon_estudiar_carrera=self.datos_formulario['paso6']['razon_carrera']
            )
            
            if self.postulante_existente:
                password_actual = self.postulante_existente.password
                # Actualizar postulante existente
                postulante_actualizado = self.fabrica.crear_usuario(
                    "Postulante",
                    correo=self.datos_formulario['paso2']['correo'],
                    password=self.postulante_existente.password,
                    datos_personales=datos
                )
                
                self.usuario_repo.actualizar(postulante_actualizado)
                
                messagebox.showinfo(
                    "✓ Perfil Completado",
                    f"¡Su perfil ha sido completado exitosamente!\n\n"
                    f"Nombre: {datos.nombre} {datos.apellidos}\n"
                    f"Cédula: {datos.cedula}\n\n"
                    f"✓ Ya puede acceder a todas las funcionalidades"
                )
            else:
                # Crear nuevo postulante
                password = self.datos_formulario['paso2'].get('password', 'temp123')
                postulante = self.fabrica.crear_usuario(
                    "Postulante",
                    correo=self.datos_formulario['paso2']['correo'],
                    password=self.datos_formulario['paso2'].get('password', 'temp123'),
                    datos_personales=datos
                )
                
                self.usuario_repo.agregar(postulante)
                
                messagebox.showinfo(
                    "✓ Registro Completado",
                    f"¡Felicitaciones! Tu registro se ha completado exitosamente.\n\n"
                    f"📋 DATOS DE ACCESO:\n"
                    f"═══════════════\n"
                    f"Nombre: {datos.nombre} {datos.apellidos}\n"
                    f"Cédula: {datos.cedula}\n"
                    f"Usuario: {datos.correo}\n\n"
                    f"✓ Tu información ha sido guardada\n"
                    f"✓ Puedes iniciar sesión con tu correo y contraseña"
                )
            
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"No se pudo completar el registro:\n\n{str(e)}\n\n"
                f"Por favor, revise que todos los campos estén completos."
            )
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
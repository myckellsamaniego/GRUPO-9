# -*- coding: utf-8 -*-
"""
Ventana de Registro de Nuevos Postulantes
Formulario básico para crear cuenta
"""
import tkinter as tk
from tkinter import messagebox, ttk

from models.datos_personales import DatosPersonales
from factory.fabrica_usuarios import FabricaUsuarios


class RegistroApp:
    """Ventana de registro de nuevos postulantes con cédula pre-validada"""

    def __init__(self, root, usuario_repo, cedula_validada=None):
        self.root = root
        self.usuario_repo = usuario_repo
        self.fabrica = FabricaUsuarios()
        self.cedula_validada = cedula_validada

        self.root.title("Obtener Cuenta - Sistema ULEAM 2026")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 600
        height = 550
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.root, bg="#1e3a8a", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📝 Obtener cuenta",
            font=("Arial", 18, "bold"),
            bg="#1e3a8a",
            fg="white"
        ).pack(pady=20)
        
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root, bg="white")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido del formulario
        form_frame = tk.Frame(scrollable_frame, bg="white", padx=40, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)

        self.entries = {}
        row = 0

        # 1. TIPO DE DOCUMENTO
        tk.Label(
            form_frame,
            text="Tipo de documento: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        self.tipo_doc_var = tk.StringVar(value="Cédula de ciudadanía ecuatoriana")
        tipo_doc_combo = ttk.Combobox(
            form_frame,
            textvariable=self.tipo_doc_var,
            values=[
                "Cédula de ciudadanía ecuatoriana",
                "Pasaporte",
                "Documento extranjero"
            ],
            state="readonly",
            width=45,
            font=("Arial", 10)
        )
        tipo_doc_combo.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        row += 1

        # 2. IDENTIFICACIÓN (CÉDULA)
        tk.Label(
            form_frame,
            text="Identificación: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        cedula_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        if self.cedula_validada:
            cedula_entry.insert(0, self.cedula_validada)
            cedula_entry.config(state="disabled")
        cedula_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["cedula"] = cedula_entry
        row += 1

        # 3. NOMBRES
        tk.Label(
            form_frame,
            text="Nombres: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        nombres_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        nombres_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["nombres"] = nombres_entry
        nombres_entry.focus()
        row += 1

        # 4. APELLIDOS
        tk.Label(
            form_frame,
            text="Apellidos: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        apellidos_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        apellidos_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["apellidos"] = apellidos_entry
        row += 1

        # 5. CELULAR (Opcional)
        tk.Label(
            form_frame,
            text="Celular:",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        celular_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        celular_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["celular"] = celular_entry
        row += 1

        # 6. CORREO
        tk.Label(
            form_frame,
            text="Correo electrónico: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        correo_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        correo_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["correo"] = correo_entry
        row += 1

        # 7. CONFIRMAR CORREO
        tk.Label(
            form_frame,
            text="Confirmar correo electrónico: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        confirmar_correo_entry = ttk.Entry(form_frame, width=47, font=("Arial", 10))
        confirmar_correo_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 15))
        self.entries["confirmar_correo"] = confirmar_correo_entry
        row += 1

        # 8. CONTRASEÑA
        tk.Label(
            form_frame,
            text="Contraseña: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        password_entry = ttk.Entry(form_frame, show="●", width=47, font=("Arial", 10))
        password_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 5))
        self.entries["password"] = password_entry
        row += 1

        # Info de contraseña
        tk.Label(
            form_frame,
            text="La contraseña deberá contener mínimo 6 y máximo 12 caracteres",
            font=("Arial", 8),
            bg="white",
            fg="#4a5568",
            justify=tk.LEFT
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 15))
        row += 1

        # 9. CONFIRMAR CONTRASEÑA
        tk.Label(
            form_frame,
            text="Confirmar contraseña: *",
            font=("Arial", 10),
            bg="white",
            anchor="w"
        ).grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        confirmar_password_entry = ttk.Entry(form_frame, show="●", width=47, font=("Arial", 10))
        confirmar_password_entry.grid(row=row, column=0, sticky=tk.EW, pady=(0, 20))
        self.entries["confirmar_password"] = confirmar_password_entry
        row += 1

        # Configurar expansión de columna
        form_frame.columnconfigure(0, weight=1)

        # BOTONES FINALES
        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.grid(row=row, column=0, pady=20)

        tk.Button(
            buttons_frame,
            text="✓ Crear Cuenta",
            command=self.crear_cuenta,
            bg="#10b981",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons_frame,
            text="✗ Cancelar",
            command=self.root.destroy,
            bg="#6b7280",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            width=15
        ).grid(row=0, column=1, padx=5)
        
        # Empacar canvas y scrollbar
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def crear_cuenta(self):
        """Procesa la creación de una nueva cuenta"""
        try:
            # Obtener valores
            cedula = self.cedula_validada if self.cedula_validada else self.entries["cedula"].get().strip()
            nombres = self.entries["nombres"].get().strip()
            apellidos = self.entries["apellidos"].get().strip()
            celular = self.entries["celular"].get().strip()
            correo = self.entries["correo"].get().strip()
            confirmar_correo = self.entries["confirmar_correo"].get().strip()
            password = self.entries["password"].get()
            confirmar_password = self.entries["confirmar_password"].get()

            # VALIDACIONES

            # 1. Campos obligatorios
            if not all([cedula, nombres, apellidos, correo, password]):
                raise ValueError(
                    "Complete todos los campos obligatorios marcados con *:\n"
                    "• Tipo de documento\n"
                    "• Identificación\n"
                    "• Nombres\n"
                    "• Apellidos\n"
                    "• Correo electrónico\n"
                    "• Contraseña"
                )

            # 2. Validar correos coincidan
            if correo != confirmar_correo:
                raise ValueError("Los correos electrónicos no coinciden")

            # 3. Validar formato de correo
            if "@" not in correo or "." not in correo.split("@")[-1]:
                raise ValueError("Formato de correo inválido")

            # 4. Validar contraseñas coincidan
            if password != confirmar_password:
                raise ValueError("Las contraseñas no coinciden")

            # 5. Validar longitud de contraseña
            if len(password) < 6 or len(password) > 12:
                raise ValueError("La contraseña debe tener entre 6 y 12 caracteres")

            # 6. Validar cédula
            if not cedula.isdigit() or len(cedula) != 10:
                raise ValueError("La cédula debe tener 10 dígitos")

            # 7. Verificar si el correo ya existe
            if self.usuario_repo.buscar_por_correo(correo):
                raise ValueError(
                    "Ya existe una cuenta con ese correo electrónico.\n\n"
                    "Si ya tiene cuenta, use la opción 'Iniciar Sesión'."
                )
            
            # 8. Verificar si la cédula ya existe
            if self.usuario_repo.existe_cedula(cedula):
                raise ValueError(
                    f"Ya existe una cuenta con la cédula {cedula}.\n\n"
                    "Si ya tiene cuenta, use la opción 'Iniciar Sesión'."
                )

            # CREAR USUARIO

            # Crear datos personales (solo campos básicos)
            datos = DatosPersonales(
                nombre=nombres,
                apellidos=apellidos,
                cedula=cedula,
                correo=correo,
                celular=celular,
                direccion="",  # Se puede completar después
                etnia="",      # Se puede completar después
                discapacidad=False
            )

            # Crear postulante
            postulante = self.fabrica.crear_usuario(
                "Postulante",
                correo=correo,
                password=password,
                datos_personales=datos
            )

            # Guardar en el repositorio
            self.usuario_repo.agregar(postulante)

            # CONFIRMACIÓN EXITOSA
            messagebox.showinfo(
                "✓ Cuenta Creada Exitosamente",
                f"Su cuenta ha sido creada correctamente.\n\n"
                f"📋 DATOS DE ACCESO:\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Nombre: {nombres} {apellidos}\n"
                f"Cédula: {cedula}\n"
                f"Usuario: {correo}\n\n"
                f"⚠️ IMPORTANTE:\n"
                f"• Use su correo y contraseña para iniciar sesión\n"
                f"• Guarde sus credenciales en un lugar seguro\n\n"
                f"Cierre esta ventana para volver al inicio de sesión."
            )
            
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("❌ Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("❌ Error Inesperado", f"Ocurrió un error:\n{e}")
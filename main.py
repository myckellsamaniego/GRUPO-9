"""
Sistema de Admisión Universitaria - ULEAM 2026
Punto de entrada principal de la aplicación

Autor: [Tu nombre]
Fecha: 2026
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.login_app import LoginApp
from servicios.autenticacion_servicios import AutenticacionService
from servicios.inicializacion_service import InicializacionService
from repository.usuario_repository_json import UsuarioRepositoryJSON


def main():
    """
    Función principal que inicializa y ejecuta el sistema.
    
    Flujo:
    1. Crear repositorio de usuarios
    2. Inicializar administrador por defecto
    3. Crear servicio de autenticación
    4. Lanzar interfaz de login
    """
    
    try:
        print("=" * 50)
        print("Sistema de Admisión ULEAM 2026")
        print("=" * 50)
        print("\nIniciando sistema...")
        
        # 1. Inicializar repositorio de usuarios
        print("✓ Inicializando repositorio de usuarios...")
        usuario_repo = UsuarioRepositoryJSON()
        
        # 2. Crear administrador inicial si no existe
        print("✓ Verificando administrador del sistema...")
        init_service = InicializacionService(usuario_repo)
        init_service.crear_admin_inicial()
        
        # 3. Crear servicio de autenticación
        print("✓ Configurando servicio de autenticación...")
        auth_service = AutenticacionService(usuario_repo)
        
        # 4. Iniciar interfaz gráfica
        print("✓ Iniciando interfaz gráfica...")
        print("\n" + "=" * 50)
        print("Sistema iniciado correctamente")
        print("=" * 50)
        print("\nCREDENCIALES DE ADMINISTRADOR:")
        print("  Usuario: admin@uleam.edu.ec")
        print("  Contraseña: admin123")
        print("=" * 50 + "\n")
        
        root = tk.Tk()
        LoginApp(root, auth_service)
        root.mainloop()
        
        print("\n✓ Sistema cerrado correctamente")
        
    except Exception as e:
        print(f"\n✗ ERROR CRÍTICO: {e}")
        messagebox.showerror(
            "Error Crítico",
            f"No se pudo iniciar el sistema:\n\n{e}\n\n"
            f"Contacte al administrador del sistema."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
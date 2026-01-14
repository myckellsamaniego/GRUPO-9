"""
Sistema de Admisión Universitaria - ULEAM 2026
Punto de entrada principal de la aplicación

Autor: Sistema de Admisión ULEAM
Fecha: 2026
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.login_app import LoginMejoradoApp
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
    4. Lanzar interfaz de login mejorada
    """
    
    try:
        print("=" * 60)
        print("    SISTEMA DE ADMISIÓN ULEAM 2026")
        print("    Universidad Laica Eloy Alfaro de Manabí")
        print("=" * 60)
        print("\n🔄 Iniciando sistema...")
        
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
        
        # 4. Iniciar interfaz gráfica mejorada
        print("✓ Iniciando interfaz gráfica...")
        print("\n" + "=" * 60)
        print("✓ Sistema iniciado correctamente")
        print("=" * 60)
        print("\n📋 CREDENCIALES DE ADMINISTRADOR:")
        print("  📧 Usuario: admin@uleam.edu.ec")
        print("  🔑 Contraseña: admin123")
        print("=" * 60 + "\n")
        
        root = tk.Tk()
        LoginMejoradoApp(root, auth_service, usuario_repo)
        root.mainloop()
        
        print("\n✓ Sistema cerrado correctamente")
        
    except Exception as e:
        print(f"\n✗ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror(
            "Error Crítico",
            f"No se pudo iniciar el sistema:\n\n{e}\n\n"
            f"Contacte al administrador del sistema."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
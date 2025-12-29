# main.py - Sistema de Inscripción y Admisión ULEAM
# Sistema interactivo para ingresar datos manualmente

from models.universidad import Universidad
from models.sede import Sede
from models.periodo import Periodo
from models.oferta_academica import OfertaAcademica
from models.postulante import Postulante
from models.datos_personales import DatosPersonales
from models.inscripcion import Inscripcion
from models.evaluacion import Evaluacion
from models.administrador import Administrador

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*60)
    print("🎓 SISTEMA DE INSCRIPCIÓN Y ADMISIÓN - ULEAM")
    print("="*60)
    print("\n1. Gestionar Universidad")
    print("2. Gestionar Postulantes")
    print("3. Gestionar Inscripciones")
    print("4. Gestionar Evaluaciones")
    print("5. Consultas y Reportes")
    print("6. Salir")
    print("\n" + "-"*60)

def crear_universidad():
    """Crea y configura la universidad"""
    print("\n📌 CONFIGURACIÓN DE LA UNIVERSIDAD")
    print("-" * 60)
    
    nombre = input("Ingrese el nombre de la universidad: ")
    universidad = Universidad(nombre)
    
    print(f"\n✅ Universidad '{nombre}' creada exitosamente.")
    
    # Agregar sedes
    print("\n¿Desea agregar sedes? (s/n): ", end="")
    if input().lower() == 's':
        agregar_sedes(universidad)
    
    # Agregar periodo académico
    print("\n¿Desea crear el periodo académico? (s/n): ", end="")
    if input().lower() == 's':
        agregar_periodo(universidad)
    
    # Agregar ofertas académicas
    print("\n¿Desea agregar ofertas académicas? (s/n): ", end="")
    if input().lower() == 's':
        agregar_ofertas(universidad)
    
    return universidad

def agregar_sedes(universidad):
    """Agrega sedes a la universidad"""
    print("\n📍 AGREGAR SEDES")
    print("-" * 60)
    
    while True:
        print("\n--- Nueva Sede ---")
        nombre = input("Nombre de la sede: ")
        direccion = input("Dirección: ")
        ciudad = input("Ciudad: ")
        capacidad = int(input("Capacidad: "))
        
        sede = Sede(nombre, direccion, ciudad, capacidad)
        universidad.agregar_sede(sede)
        
        print("\n¿Desea agregar otra sede? (s/n): ", end="")
        if input().lower() != 's':
            break

def agregar_periodo(universidad):
    """Crea y agrega un periodo académico"""
    print("\n📅 CREAR PERIODO ACADÉMICO")
    print("-" * 60)
    
    id_periodo = input("ID del periodo (ej: 2025-2): ")
    nombre = input("Nombre del periodo (ej: Segundo Periodo 2025): ")
    estado = input("Estado (ACTIVO/INACTIVO): ").upper()
    fecha_inicio = input("Fecha de inicio (dd/mm/aaaa): ")
    fecha_fin = input("Fecha de fin (dd/mm/aaaa): ")
    
    periodo = Periodo(id_periodo, nombre, estado, fecha_inicio, fecha_fin)
    universidad.Crear_Periodo(periodo)
    
    return periodo

def agregar_ofertas(universidad):
    """Agrega ofertas académicas"""
    print("\n📚 AGREGAR OFERTAS ACADÉMICAS")
    print("-" * 60)
    
    while True:
        print("\n--- Nueva Oferta ---")
        id_oferta = input("ID de oferta (ej: OFA001): ")
        nombre_carrera = input("Nombre de la carrera: ").upper()
        capacidad = int(input("Capacidad de cupos: "))
        estado = input("Estado (ABIERTO/CERRADO): ").upper()
        
        oferta = OfertaAcademica(id_oferta, nombre_carrera, capacidad, estado)
        universidad.Oferta_Academica(oferta)
        
        print("\n¿Desea agregar otra oferta? (s/n): ", end="")
        if input().lower() != 's':
            break

def crear_postulante():
    """Crea un nuevo postulante con sus datos personales"""
    print("\n👤 REGISTRO DE NUEVO POSTULANTE")
    print("-" * 60)
    
    # Datos de usuario
    print("\n--- Datos de Usuario ---")
    nombre = input("Nombre completo: ")
    usuario = input("Nombre de usuario: ")
    correo = input("Correo electrónico: ")
    clave = input("Contraseña: ")
    
    # Datos personales
    print("\n--- Datos Personales ---")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    cedula = input("Cédula: ")
    direccion = input("Dirección: ")
    celular = input("Celular: ")
    etnia = input("Etnia: ")
    
    print("¿Tiene discapacidad? (SI/NO): ", end="")
    discapacidad = input().upper()
    
    # Crear objetos
    datos = DatosPersonales(nombres, apellidos, cedula, direccion, 
                           celular, correo, etnia, discapacidad)
    
    postulante = Postulante(nombre, usuario, correo, clave)
    postulante._datos_personales = datos  # Asignar datos personales
    
    print(f"\n✅ Postulante '{nombre}' registrado exitosamente.")
    print(f"   Usuario: {usuario}")
    print(f"   Cédula: {cedula}")
    
    return postulante

def crear_inscripcion(postulante, universidad):
    """Crea una inscripción para un postulante"""
    print("\n📝 CREAR INSCRIPCIÓN")
    print("-" * 60)
    
    # Verificar que haya periodos disponibles
    if not universidad._periodos:
        print("\n❌ No hay periodos académicos disponibles.")
        print("   Debe crear un periodo primero.")
        return None
    
    # Mostrar periodos disponibles
    print("\nPeriodos disponibles:")
    for i, periodo in enumerate(universidad._periodos, 1):
        print(f"{i}. {periodo}")
    
    opcion_periodo = int(input("\nSeleccione el periodo: ")) - 1
    periodo = universidad._periodos[opcion_periodo]
    
    # Datos de inscripción
    id_inscripcion = input("\nID de inscripción (ej: INS-2025-001): ")
    fecha = input("Fecha de inscripción (dd/mm/aaaa): ")
    
    print("\nModalidad:")
    print("1. Matutino")
    print("2. Vespertino")
    opcion_modalidad = input("Seleccione: ")
    modalidad = "Matutino" if opcion_modalidad == "1" else "Vespertino"
    
    # Crear inscripción
    inscripcion = Inscripcion(id_inscripcion, fecha, modalidad, periodo)
    inscripcion._postulante = postulante  # Asignar postulante
    
    # Seleccionar carreras (máximo 3 prioridades)
    print("\n📚 Selección de Carreras (máximo 3 prioridades)")
    
    if not universidad._ofertas_academicas:
        print("\n❌ No hay ofertas académicas disponibles.")
        return inscripcion
    
    print("\nOfertas disponibles:")
    for i, oferta in enumerate(universidad._ofertas_academicas, 1):
        print(f"{i}. {oferta.Consultar_Cupos()}")
    
    prioridades = []
    for prioridad in range(1, 4):
        print(f"\n--- Prioridad {prioridad} ---")
        print("0. No seleccionar más carreras")
        opcion = int(input(f"Seleccione carrera para prioridad {prioridad}: "))
        
        if opcion == 0:
            break
        
        oferta = universidad._ofertas_academicas[opcion - 1]
        prioridades.append({
            'prioridad': prioridad,
            'oferta': oferta,
            'id_oferta': oferta._id_oferta
        })
        print(f"✅ {oferta._nombre_carrera} seleccionada como prioridad {prioridad}")
    
    inscripcion._prioridades = prioridades
    inscripcion.Crear_Inscripcion()
    
    # Agregar al postulante
    if not hasattr(postulante, '_inscripciones'):
        postulante._inscripciones = []
    postulante._inscripciones.append(inscripcion)
    
    return inscripcion

def crear_evaluacion(postulante, universidad):
    """Crea una evaluación para un postulante"""
    print("\n📋 PROGRAMAR EVALUACIÓN")
    print("-" * 60)
    
    id_evaluacion = input("ID de evaluación (ej: EVAL-2025-001): ")
    fecha = input("Fecha de evaluación (dd/mm/aaaa): ")
    hora = input("Hora (HH:MM): ")
    
    print("\nTipo de evaluación:")
    print("1. Presencial")
    print("2. Virtual")
    opcion_tipo = input("Seleccione: ")
    tipo = "Presencial" if opcion_tipo == "1" else "Virtual"
    
    lugar = ""
    if tipo == "Presencial":
        if universidad._sedes:
            print("\nSedes disponibles:")
            for i, sede in enumerate(universidad._sedes, 1):
                print(f"{i}. {sede.Consultar_Sede()}")
            
            opcion_sede = int(input("\nSeleccione sede: ")) - 1
            sede = universidad._sedes[opcion_sede]
            lugar = sede._nombre
        else:
            lugar = input("Lugar: ")
    else:
        lugar = "Plataforma Virtual"
    
    # Crear evaluación
    evaluacion = Evaluacion(id_evaluacion, fecha, hora, lugar, tipo)
    evaluacion._postulante = postulante  # Asignar postulante
    
    evaluacion.Programar()
    
    # Agregar al postulante
    if not hasattr(postulante, '_evaluaciones'):
        postulante._evaluaciones = []
    postulante._evaluaciones.append(evaluacion)
    
    return evaluacion

def mostrar_consultas(postulantes, universidad):
    """Muestra menú de consultas y reportes"""
    while True:
        print("\n📊 CONSULTAS Y REPORTES")
        print("-" * 60)
        print("1. Listar todos los postulantes")
        print("2. Ver inscripciones de un postulante")
        print("3. Ver evaluaciones de un postulante")
        print("4. Ver ofertas académicas disponibles")
        print("5. Ver información de la universidad")
        print("6. Volver al menú principal")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            listar_postulantes(postulantes)
        elif opcion == "2":
            ver_inscripciones_postulante(postulantes)
        elif opcion == "3":
            ver_evaluaciones_postulante(postulantes)
        elif opcion == "4":
            ver_ofertas(universidad)
        elif opcion == "5":
            ver_info_universidad(universidad)
        elif opcion == "6":
            break
        
        pausar()

def listar_postulantes(postulantes):
    """Lista todos los postulantes registrados"""
    print("\n👥 POSTULANTES REGISTRADOS")
    print("-" * 60)
    
    if not postulantes:
        print("No hay postulantes registrados.")
        return
    
    for i, postulante in enumerate(postulantes, 1):
        print(f"\n{i}. {postulante.mostrar_informacion()}")

def ver_inscripciones_postulante(postulantes):
    """Muestra las inscripciones de un postulante"""
    if not postulantes:
        print("\n❌ No hay postulantes registrados.")
        return
    
    print("\nPostulantes:")
    for i, p in enumerate(postulantes, 1):
        print(f"{i}. {p._nombre} ({p._usuario})")
    
    opcion = int(input("\nSeleccione postulante: ")) - 1
    postulante = postulantes[opcion]
    
    print(f"\n📝 Inscripciones de {postulante._nombre}")
    print("-" * 60)
    
    if hasattr(postulante, '_inscripciones') and postulante._inscripciones:
        for insc in postulante._inscripciones:
            print(f"\n{insc.Consultar()}")
            if hasattr(insc, '_prioridades') and insc._prioridades:
                print("   Carreras seleccionadas:")
                for p in insc._prioridades:
                    print(f"      {p['prioridad']}. {p['oferta']._nombre_carrera}")
    else:
        print("No tiene inscripciones registradas.")

def ver_evaluaciones_postulante(postulantes):
    """Muestra las evaluaciones de un postulante"""
    if not postulantes:
        print("\n❌ No hay postulantes registrados.")
        return
    
    print("\nPostulantes:")
    for i, p in enumerate(postulantes, 1):
        print(f"{i}. {p._nombre} ({p._usuario})")
    
    opcion = int(input("\nSeleccione postulante: ")) - 1
    postulante = postulantes[opcion]
    
    print(f"\n📋 Evaluaciones de {postulante._nombre}")
    print("-" * 60)
    
    if hasattr(postulante, '_evaluaciones') and postulante._evaluaciones:
        for ev in postulante._evaluaciones:
            print(f"\n{ev.Consultar()}")
    else:
        print("No tiene evaluaciones programadas.")

def ver_ofertas(universidad):
    """Muestra todas las ofertas académicas"""
    print("\n📚 OFERTAS ACADÉMICAS")
    print("-" * 60)
    
    if not universidad._ofertas_academicas:
        print("No hay ofertas académicas registradas.")
        return
    
    for oferta in universidad._ofertas_academicas:
        print(f"\n• {oferta.Consultar_Cupos()}")

def ver_info_universidad(universidad):
    """Muestra información general de la universidad"""
    print("\n🏛️  INFORMACIÓN DE LA UNIVERSIDAD")
    print("-" * 60)
    print(f"Nombre: {universidad._nombre}")
    print(f"Sedes: {len(universidad._sedes)}")
    print(f"Ofertas Académicas: {len(universidad._ofertas_academicas)}")
    print(f"Periodos Académicos: {len(universidad._periodos)}")

def main():
    """Función principal del sistema"""
    universidad = None
    postulantes = []
    
    print("\n¡Bienvenido al Sistema de Inscripción y Admisión ULEAM!")
    pausar()
    
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Gestionar Universidad
            if universidad is None:
                universidad = crear_universidad()
            else:
                print("\n⚠️  Ya existe una universidad configurada.")
                print("¿Desea reconfigurarla? (s/n): ", end="")
                if input().lower() == 's':
                    universidad = crear_universidad()
            pausar()
        
        elif opcion == "2":
            # Gestionar Postulantes
            postulante = crear_postulante()
            postulantes.append(postulante)
            pausar()
        
        elif opcion == "3":
            # Gestionar Inscripciones
            if not postulantes:
                print("\n❌ Debe registrar postulantes primero.")
            elif universidad is None:
                print("\n❌ Debe configurar la universidad primero.")
            else:
                print("\nPostulantes disponibles:")
                for i, p in enumerate(postulantes, 1):
                    print(f"{i}. {p._nombre} ({p._usuario})")
                
                opcion_post = int(input("\nSeleccione postulante: ")) - 1
                crear_inscripcion(postulantes[opcion_post], universidad)
            pausar()
        
        elif opcion == "4":
            # Gestionar Evaluaciones
            if not postulantes:
                print("\n❌ Debe registrar postulantes primero.")
            elif universidad is None:
                print("\n❌ Debe configurar la universidad primero.")
            else:
                print("\nPostulantes disponibles:")
                for i, p in enumerate(postulantes, 1):
                    print(f"{i}. {p._nombre} ({p._usuario})")
                
                opcion_post = int(input("\nSeleccione postulante: ")) - 1
                crear_evaluacion(postulantes[opcion_post], universidad)
            pausar()
        
        elif opcion == "5":
            # Consultas y Reportes
            if universidad is None:
                print("\n❌ Debe configurar la universidad primero.")
                pausar()
            else:
                mostrar_consultas(postulantes, universidad)
        
        elif opcion == "6":
            # Salir
            print("\n¡Gracias por usar el sistema!")
            print("Hasta pronto. 👋")
            break
        
        else:
            print("\n❌ Opción inválida. Intente nuevamente.")
            pausar()

if __name__ == "__main__":
    main()

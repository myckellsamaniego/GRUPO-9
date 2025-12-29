# main.py

from models.administrador import Administrador
from models.postulante import Postulante
from models.universidad import Universidad
from models.datos_personales import DatosPersonales
from models.inscripcion import Inscripcion
from models.evaluacion import Evaluacion
from models.sede import Sede
from models.oferta_academica import OfertaAcademica
from models.resultado import Resultado
from models.periodo import Periodo

def menu_principal():
    print("\n=== SISTEMA INTEGRAL DE INSCRIPCIÓN Y ADMISIÓN UNIVERSITARIA ===")
    print("1. Ingresar como Administrador")
    print("2. Ingresar como Postulante")
    print("3. Salir")
    return input("Seleccione una opción: ")

def menu_administrador(admin: Administrador):
    # FIX: Listas para almacenar objetos y darles persistencia
    periodos_registrados = []
    ofertas_registradas = []
    evaluaciones_registradas = []
    sedes_registradas = [] 
    
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Gestionar Períodos")
        print("2. Gestionar Oferta Académica")
        print("3. Gestionar Evaluaciones")
        print("4. Gestionar Sedes")
        print("5. Consultar Resultados")
        print("6. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        # --- OPCIÓN 1: Gestionar Períodos 
        if opcion == "1":
            print("1. Registrar período\n2. Actualizar período")
            sub = input("Seleccione: ")
            
            if sub == "1":
                periodo_nuevo = Periodo() 
                periodo_nuevo.Registrar_Tipo()
                periodos_registrados.append(periodo_nuevo)
                
            elif sub == "2":
                if not periodos_registrados:
                    print("Error: No hay períodos registrados para actualizar.")
                    continue
                
                print("\n--- Períodos Disponibles ---")
                for i, p in enumerate(periodos_registrados):
                    print(f"{i + 1}. {p._nombre} (Estado: {p._estado})") 
                
                try:
                    seleccion = int(input("Seleccione el NÚMERO del período a actualizar: ")) - 1
                    if 0 <= seleccion < len(periodos_registrados):
                        periodo_a_actualizar = periodos_registrados[seleccion]
                        estado_nuevo = input("Ingrese nuevo estado: ")
                        periodo_a_actualizar.Actualizar_Tipo(estado_nuevo)
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número.")
            else:
                 print("Opción no válida.")

        # --- OPCIÓN 2: Gestionar Oferta Académica 
        elif opcion == "2":
            print("1. Registrar Oferta\n2. Actualizar cupos\n3. Consultar cupos")
            sub = input("Seleccione: ")
            
            if sub == "1":
                oferta_nueva = OfertaAcademica()
                oferta_nueva.Registrar_Oferta() 
                ofertas_registradas.append(oferta_nueva)
                
            elif sub == "2":
                if not ofertas_registradas:
                    print("Error: No hay ofertas académicas registradas para actualizar.")
                    continue
                    
                print("\n--- Ofertas Disponibles ---")
                for i, o in enumerate(ofertas_registradas):
                    print(f"{i + 1}. {o.nombre_carrera} (Cupos: {o._capacidad})") 
                
                try:
                    seleccion = int(input("Seleccione el NÚMERO de la oferta a actualizar: ")) - 1
                    if 0 <= seleccion < len(ofertas_registradas):
                        oferta_a_actualizar = ofertas_registradas[seleccion]
                        nuevos_cupos = input("Ingrese nuevos cupos: ")
                        oferta_a_actualizar.Actualizar_Cupos(nuevos_cupos)
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número.")
            
            elif sub == "3":
                if not ofertas_registradas:
                    print("Error: No hay ofertas académicas registradas para consultar.")
                    continue

                print("\n--- Ofertas Disponibles ---")
                for i, o in enumerate(ofertas_registradas):
                    print(f"{i + 1}. {o.Consultar_Cupos()}")
            else:
                 print("Opción no válida.")


        # --- OPCIÓN 3: Gestionar Evaluaciones 
        elif opcion == "3":
            print("1. Programar evaluación\n2. Modificar evaluación\n3. Consultar evaluación")
            sub = input("Seleccione: ")
            
            if sub == "1":
                evaluacion_nueva = Evaluacion()
                evaluacion_nueva.Programar()
                evaluaciones_registradas.append(evaluacion_nueva)
                
            elif sub == "2":
                if not evaluaciones_registradas:
                    print("Error: No hay evaluaciones programadas para modificar.")
                    continue
                    
                print("\n--- Evaluaciones Disponibles ---")
                for i, e in enumerate(evaluaciones_registradas):
                    print(f"{i + 1}. {e._id_evaluacion} - {e._fecha} en {e._lugar}") 
                
                try:
                    seleccion = int(input("Seleccione el NÚMERO de la evaluación a modificar: ")) - 1
                    if 0 <= seleccion < len(evaluaciones_registradas):
                        evaluacion_a_modificar = evaluaciones_registradas[seleccion]
                        evaluacion_a_modificar.Modificar()
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número.")
            
            elif sub == "3":
                if not evaluaciones_registradas:
                    print("Error: No hay evaluaciones programadas para consultar.")
                    continue

                print("\n--- Evaluaciones Programadas ---")
                for i, e in enumerate(evaluaciones_registradas):
                    print(f"{i + 1}. {e.Consultar()}")
            else:
                 print("Opción no válida.")

        # --- OPCIÓN 4: Gestionar Sedes 
        elif opcion == "4":
            print("1. Registrar sede\n2. Modificar sede\n3. Consultar sede")
            sub = input("Seleccione: ")
            
            if sub == "1":
                sede_nueva = Sede()
                sede_nueva.Registrar_Sede()
                sedes_registradas.append(sede_nueva)
                
            elif sub == "2":
                if not sedes_registradas:
                    print("Error: No hay sedes registradas para modificar.")
                    continue
                    
                print("\n--- Sedes Disponibles ---")
                for i, s in enumerate(sedes_registradas):
                    print(f"{i + 1}. {s._nombre} ({s._ciudad})") 
                
                try:
                    seleccion = int(input("Seleccione el NÚMERO de la sede a modificar: ")) - 1
                    if 0 <= seleccion < len(sedes_registradas):
                        sede_a_modificar = sedes_registradas[seleccion]
                        sede_a_modificar.Modificar() 
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número.")
            
            elif sub == "3":
                if not sedes_registradas:
                    print("Error: No hay sedes registradas para consultar.")
                    continue

                print("\n--- Sedes Registradas ---")
                for i, s in enumerate(sedes_registradas):
                    print(f"{i + 1}. {s.Consultar_Sede()}")
            else:
                 print("Opción no válida.")

        # --- OPCIÓN 5: Consultar Resultados (Muestra aviso si está vacío) ---
        elif opcion == "5":
            resultado = Resultado()
            print(resultado.Mostrar_Resultado())

        elif opcion == "6":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")


def menu_postulante(post: Postulante):
    # LÍNEAS CLAVE: Inicializa las propiedades para guardar los objetos
    if not hasattr(post, '_datos_personales'):
        post._datos_personales = None
    if not hasattr(post, '_inscripcion'):
        post._inscripcion = None
        
    while True:
        print("\n--- MENÚ POSTULANTE ---")
        print("1. Registrar datos personales")
        print("2. Realizar inscripción")
        print("3. Consultar inscripción")
        print("4. Consultar resultado")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        # --- OPCIÓN 1: Registrar datos personales 
        if opcion == "1":
            datos = DatosPersonales()
            datos.Registrar()
            # **Guardamos el objeto** en el postulante
            post._datos_personales = datos 

        # --- OPCIÓN 2: Realizar inscripción 
        elif opcion == "2":
            if post._datos_personales is None:
                print("Error: Primero debe registrar sus datos personales (Opción 1).")
                continue
                
            ins = Inscripcion()
            ins.Crear_Inscripcion() # Usamos el método de la clase
            # **Guardamos el objeto** en el postulante
            post._inscripcion = ins

        # --- OPCIÓN 3: Consultar inscripción 
        elif opcion == "3":
            if post._inscripcion is None:
                print("Error: No ha realizado ninguna inscripción.")
                continue
            
            print("\n--- DETALLES DE INSCRIPCIÓN ---")
            # Mostramos los datos personales si existen
            if post._datos_personales:
                 print(post._datos_personales.Consultar())
            # Mostramos la inscripción
            print(post._inscripcion.Consultar())


        # --- OPCIÓN 4: Consultar resultado ---
        elif opcion == "4":
            res = Resultado()
            print(res.Mostrar_Resultado()) 

        elif opcion == "5":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")

# FUNCIÓN PRINCIPAL (INICIO DEL PROGRAMA)

def main():
    print("=== Bienvenido al Sistema de Inscripción Universitaria ===")
    nombre_uni = input("Ingrese el nombre de la universidad: ")
    
    universidad = Universidad(nombre_uni)
    print(f"\nUniversidad registrada: {universidad.nombre}")

    while True:
        opcion = menu_principal()
        
        if opcion == "1":
            # Parámetros para Administrador 
            adminID = input("ID del administrador: ")
            nombre = input("Nombre del administrador: ")
            correo = input("Correo: ")
            clave = input("Clave: ")
            admin = Administrador(adminID, nombre, correo, clave)
            
            print(f"Bienvenido Administrador {admin.nombres}")
            menu_administrador(admin)

        elif opcion == "2":
            # Parámetros para Postulante 
            nombre = input("Nombre del postulante: ")
            usuario = input("Usuario: ")
            correo = input("Correo: ")
            clave = input("Clave: ")
            post = Postulante(nombre, usuario, correo, clave) 
            
            print(f"Bienvenido Postulante {post.nombres}")
            menu_postulante(post)

        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
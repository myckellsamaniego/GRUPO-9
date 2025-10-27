# main.py

#prueba
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
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Gestionar Períodos")
        print("2. Gestionar Oferta Académica")
        print("3. Gestionar Evaluaciones")
        print("4. Gestionar Sedes")
        print("5. Consultar Resultados")
        print("6. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            periodo = Periodo()
            print("1. Registrar período\n2. Actualizar período")
            sub = input("Seleccione: ")
            if sub == "1":
                periodo.registrarTipo()
            else:
                periodo.actualizarTipo()

        elif opcion == "2":
            oferta = OfertaAcademica()
            print("1. Actualizar cupos\n2. Consultar cupos")
            sub = input("Seleccione: ")
            if sub == "1":
                oferta.actualizarCupos()
            else:
                oferta.consultarCupos()

        elif opcion == "3":
            eval = Evaluacion()
            print("1. Programar evaluación\n2. Modificar evaluación")
            sub = input("Seleccione: ")
            if sub == "1":
                eval.programarEvaluacion()
            else:
                eval.modificar()

        elif opcion == "4":
            sede = Sede()
            print("1. Registrar sede\n2. Modificar sede\n3. Consultar sede")
            sub = input("Seleccione: ")
            if sub == "1":
                sede.registrarSede()
            elif sub == "2":
                sede.modificarSede()
            else:
                sede.consultarSede()

        elif opcion == "5":
            resultado = Resultado()
            resultado.mostrarResultado()

        elif opcion == "6":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")

def menu_postulante(post: Postulante):
    while True:
        print("\n--- MENÚ POSTULANTE ---")
        print("1. Registrar datos personales")
        print("2. Realizar inscripción")
        print("3. Consultar inscripción")
        print("4. Consultar resultado")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            datos = DatosPersonales()
            datos.registrar()

        elif opcion == "2":
            ins = Inscripcion()
            ins.crearInscripcion()

        elif opcion == "3":
            ins = Inscripcion()
            ins.consultar()

        elif opcion == "4":
            res = Resultado()
            res.mostrarResultado()

        elif opcion == "5":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")

def main():
    print("=== Bienvenido al Sistema de Inscripción Universitaria ===")
    nombre_uni = input("Ingrese el nombre de la universidad: ")
    universidad = Universidad(nombre_uni)
    print(f"\nUniversidad registrada: {universidad.nombre}")

    while True:
        opcion = menu_principal()
        if opcion == "1":
            nombre = input("Nombre del administrador: ")
            correo = input("Correo: ")
            clave = input("Clave: ")
            admin = Administrador(nombre, correo, clave)
            print(f"Bienvenido Administrador {admin.nombres}")
            menu_administrador(admin)

        elif opcion == "2":
            nombre = input("Nombre del postulante: ")
            correo = input("Correo: ")
            clave = input("Clave: ")
            post = Postulante(nombre, correo, clave)
            print(f"Bienvenido Postulante {post.nombres}")
            menu_postulante(post)

        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()

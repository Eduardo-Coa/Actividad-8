"""Demostracion de Builder y Factory Method con Estudiante."""

from app.patterns.builder import EstudianteBuilder
from app.patterns.factory_method import obtener_creator


def main() -> None:
    """Ejecuta una demostracion de los dos patrones implementados."""
    estudiante = (
        EstudianteBuilder()
        .con_codigo("est001")
        .con_nombre("Ana Maria Lopez")
        .con_edad(20)
        .con_semestre(4)
        .con_correo("ANA.LOPEZ@universidad.edu")
        .con_programa("Ciencia de Datos")
        .construir()
    )

    creator = obtener_creator("memoria")
    repositorio = creator.crear_repositorio()
    repositorio.guardar(estudiante)

    print("Actividad 8 - Builder y Factory Method")
    print("Entidad base: Estudiante")
    print("Builder: estudiante construido correctamente")
    print(f"Codigo normalizado: {estudiante.codigo}")
    print(f"Correo normalizado: {estudiante.correo}")
    print("Factory Method: repositorio creado por creator")
    print(f"Total estudiantes guardados: {len(repositorio.listar())}")


if __name__ == "__main__":
    main()

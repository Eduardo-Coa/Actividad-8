"""Demostracion de patrones Facade y Decorator para la actividad 8."""

from datetime import datetime

from app.decorators.servicio_sesion_decorator import (
    DecoradorLog,
    DecoradorValidacion,
    ServicioSesionConcreto,
)
from app.facades.sistema_seguimiento_facade import SistemaSeguimientoFacade


def demo_facade() -> None:
    """Demuestra Facade con psicologos y sesiones de seguimiento."""
    print("\n--- FACADE: sistema de seguimiento ---")
    facade = SistemaSeguimientoFacade()
    facade.registrar_psicologo(
        "PSI-001",
        "Laura Perez",
        "laura@universidad.edu",
        "Ansiedad academica",
    )
    facade.registrar_psicologo(
        "PSI-002",
        "Carlos Ruiz",
        "carlos@universidad.edu",
        "Orientacion universitaria",
    )

    facade.agendar_sesion(
        "EST-001",
        "PSI-001",
        datetime(2026, 6, 2, 10, 0),
        45,
        "Seguimiento emocional",
    )
    facade.agendar_sesion(
        "EST-002",
        "PSI-002",
        datetime(2026, 6, 3, 14, 0),
        60,
        "Acompanamiento academico",
    )

    print(f"Resumen: {facade.resumen()}")
    for sesion in facade.sesiones_por_estudiante("EST-001"):
        print(f"Sesion de {sesion.codigo_estudiante}: {sesion.motivo}")


def demo_decorator() -> None:
    """Demuestra Decorator encadenando validacion y log."""
    print("\n--- DECORATOR: servicio de sesion ---")
    facade = SistemaSeguimientoFacade()
    psicologo = facade.registrar_psicologo(
        "PSI-003",
        "Marta Gomez",
        "marta@universidad.edu",
        "Gestion emocional",
    )
    sesion = facade.agendar_sesion(
        "EST-003",
        "PSI-003",
        datetime(2026, 6, 4, 9, 30),
        50,
        "Plan de seguimiento",
    )

    servicio = DecoradorLog(DecoradorValidacion(ServicioSesionConcreto()))
    print(servicio.describir(sesion, psicologo))


def main() -> None:
    """Ejecuta las demostraciones de la actividad."""
    print("Actividad 8 - Patrones GoF aplicados a sesiones y psicologos.")
    demo_facade()
    demo_decorator()


if __name__ == "__main__":
    main()

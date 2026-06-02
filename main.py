"""Demostracion de patrones GoF para la actividad 8."""

from datetime import datetime

from app.builders.cuestionario_builder import CuestionarioBuilder
from app.commands.comandos_cuestionario import (
    EliminarCuestionarioComando,
    HistorialComandos,
    RegistrarCuestionarioComando,
)
from app.config_Singleton.configuracion_app import ConfiguracionApp
from app.decorators.repositorio_con_log import RepositorioConLog
from app.decorators.servicio_sesion_decorator import (
    DecoradorLog,
    DecoradorValidacion,
    ServicioSesionConcreto,
)
from app.facades.sistema_evaluacion_facade import SistemaEvaluacionFacade
from app.facades.sistema_seguimiento_facade import SistemaSeguimientoFacade
from app.factories.generador_reporte import GeneradorReporteCSV, GeneradorReporteTexto
from app.repositories.repositorio_memoria import RepositorioMemoria
from app.strategies.estrategia_ordenamiento import (
    ListadorCuestionarios,
    OrdenarPorCodigoAsc,
    OrdenarPorFechaDesc,
    OrdenarPorPuntajeDesc,
)

SEP = "-" * 60


def seccion(titulo: str) -> None:
    """Imprime un titulo de seccion para la demostracion."""
    print(f"\n{SEP}\n  {titulo}\n{SEP}")


def demo_facade_seguimiento() -> None:
    """Demuestra Facade con psicologos y sesiones de seguimiento."""
    seccion("8. FACADE - Seguimiento psicologico")
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

    print(f"  Resumen: {facade.resumen()}")
    for sesion in facade.sesiones_por_estudiante("EST-001"):
        print(f"  Sesion de {sesion.codigo_estudiante}: {sesion.motivo}")


def demo_decorator_seguimiento() -> None:
    """Demuestra Decorator encadenando validacion y log."""
    seccion("9. DECORATOR - Servicio de sesion")
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
    """Ejecuta las demostraciones disponibles."""
    # 1. Builder
    seccion("1. BUILDER - Construccion paso a paso")
    c1 = (
        CuestionarioBuilder()
        .codigo("EST-2026-001")
        .fecha("20/05/2026 09:00")
        .respuestas([1, 0, 2, 1, 0, 2, 1, 0, 1])
        .construir()
    )
    c2 = (
        CuestionarioBuilder()
        .codigo("EST-2026-002")
        .fecha("20/05/2026 10:30")
        .respuestas([3, 3, 3, 3, 3, 3, 3, 3, 3])
        .construir()
    )
    c3 = (
        CuestionarioBuilder()
        .codigo("EST-2026-003")
        .fecha("19/05/2026 14:00")
        .respuestas([0, 0, 1, 0, 0, 1, 0, 0, 0])
        .construir()
    )
    for c in (c1, c2, c3):
        print(
            f"  {c.codigo_estudiante:<16} "
            f"puntaje={c.puntaje_total:>3}  {c.nivel_severidad}"
        )

    cuestionarios = [c1, c2, c3]

    # 2. Factory Method
    seccion("2. FACTORY METHOD - Generadores de reporte")
    print("\n  [Reporte Texto]")
    print(GeneradorReporteTexto().generar(cuestionarios))
    print("\n  [Reporte CSV - primeras 2 lineas]")
    csv = GeneradorReporteCSV().generar(cuestionarios)
    print("\n".join(f"  {linea}" for linea in csv.splitlines()[:2]))

    # 3. Singleton
    seccion("3. SINGLETON - Configuracion global")
    cfg_a = ConfiguracionApp()
    cfg_b = ConfiguracionApp()
    print(f"  cfg_a is cfg_b : {cfg_a is cfg_b}")
    print(f"  App            : {cfg_a.nombre_app} v{cfg_a.version}")
    print(f"  Umbral severo  : >= {cfg_a.umbral_severo} pts")

    # 4. Decorator
    seccion("4. DECORATOR - Repositorio con log")
    repo_log = RepositorioConLog(RepositorioMemoria())
    for c in cuestionarios:
        repo_log.guardar(c)
    repo_log.obtener_todos()
    repo_log.obtener_por_id(c1.id)
    print("  Operaciones registradas:")
    for entrada in repo_log.log:
        print(f"    {entrada}")

    # 5. Strategy
    seccion("5. STRATEGY - Ordenamiento intercambiable")
    listador = ListadorCuestionarios(OrdenarPorFechaDesc())
    print("  Por fecha (mas reciente primero):")
    for c in listador.listar(cuestionarios):
        fecha = c.fecha_aplicacion.strftime("%d/%m/%Y %H:%M")
        print(f"    {fecha}  {c.codigo_estudiante}")

    listador.cambiar_estrategia(OrdenarPorPuntajeDesc())
    print("  Por puntaje (mayor primero):")
    for c in listador.listar(cuestionarios):
        print(f"    {c.puntaje_total:>3} pts  {c.codigo_estudiante}")

    listador.cambiar_estrategia(OrdenarPorCodigoAsc())
    print("  Por codigo (A-Z):")
    for c in listador.listar(cuestionarios):
        print(f"    {c.codigo_estudiante}")

    # 6. Facade
    seccion("6. FACADE - Interfaz simplificada")
    facade = SistemaEvaluacionFacade(RepositorioMemoria())
    facade.registrar(
        "EST-2026-004",
        "20/05/2026 08:00",
        [2, 1, 2, 1, 2, 1, 2, 1, 2],
    )
    facade.registrar(
        "EST-2026-005",
        "20/05/2026 16:00",
        [0, 0, 1, 0, 0, 0, 1, 0, 0],
    )
    stats = facade.estadisticas()
    print(f"  Total          : {stats['total']}")
    print(f"  Promedio       : {stats['promedio']} pts")
    print(f"  Casos severos  : {stats['casos_severos']}")
    print()
    print(facade.reporte())

    # 7. Command
    seccion("7. COMMAND - Undo/Redo de operaciones CRUD")
    repo_cmd = RepositorioMemoria()
    historial = HistorialComandos()

    print(f"  Registros iniciales          : {len(repo_cmd.obtener_todos())}")
    historial.ejecutar(RegistrarCuestionarioComando(repo_cmd, c1))
    historial.ejecutar(RegistrarCuestionarioComando(repo_cmd, c2))
    print(f"  Tras insertar c1 y c2        : {len(repo_cmd.obtener_todos())}")
    historial.deshacer()
    print(f"  Tras deshacer ultimo insert  : {len(repo_cmd.obtener_todos())}")
    historial.ejecutar(EliminarCuestionarioComando(repo_cmd, c1.id))
    print(f"  Tras eliminar c1             : {len(repo_cmd.obtener_todos())}")
    historial.deshacer()
    print(f"  Tras deshacer la eliminacion : {len(repo_cmd.obtener_todos())}")

    demo_facade_seguimiento()
    demo_decorator_seguimiento()

    print(f"\n{SEP}\n  Patrones ejecutados correctamente.\n{SEP}\n")


if __name__ == "__main__":
    main()

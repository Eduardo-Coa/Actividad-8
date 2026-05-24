"""Demostracion de los 7 patrones GoF aplicados al sistema PHQ-9."""

from app.builders.cuestionario_builder import CuestionarioBuilder
from app.commands.comandos_cuestionario import (
    EliminarCuestionarioComando,
    HistorialComandos,
    RegistrarCuestionarioComando,
)
from app.config.configuracion_app import ConfiguracionApp
from app.decorators.repositorio_con_log import RepositorioConLog
from app.facades.sistema_evaluacion_facade import SistemaEvaluacionFacade
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
    print(f"\n{SEP}\n  {titulo}\n{SEP}")


def main() -> None:
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
        print(f"  {c.codigo_estudiante:<16} puntaje={c.puntaje_total:>3}  {c.nivel_severidad}")

    cuestionarios = [c1, c2, c3]

    # 2. Factory Method
    seccion("2. FACTORY METHOD - Generadores de reporte")
    print("\n  [Reporte Texto]")
    print(GeneradorReporteTexto().generar(cuestionarios))
    print("\n  [Reporte CSV - primeras 2 lineas]")
    csv = GeneradorReporteCSV().generar(cuestionarios)
    print("\n".join(f"  {ln}" for ln in csv.splitlines()[:2]))

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
        print(f"    {c.fecha_aplicacion.strftime('%d/%m/%Y %H:%M')}  {c.codigo_estudiante}")

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
    facade.registrar("EST-2026-004", "20/05/2026 08:00", [2, 1, 2, 1, 2, 1, 2, 1, 2])
    facade.registrar("EST-2026-005", "20/05/2026 16:00", [0, 0, 1, 0, 0, 0, 1, 0, 0])
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

    print(f"\n{SEP}\n  Los 7 patrones ejecutados correctamente.\n{SEP}\n")


if __name__ == "__main__":
    main()

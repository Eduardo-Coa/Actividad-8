"""Pruebas unitarias — 7 patrones GoF aplicados al sistema PHQ-9.

14 casos: 2 por patrón (Builder, Factory Method, Singleton,
Decorator, Strategy, Facade, Command).
"""

import uuid
from datetime import datetime

import pytest

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
from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.repositories.repositorio_memoria import RepositorioMemoria
from app.strategies.estrategia_ordenamiento import (
    ListadorCuestionarios,
    OrdenarPorFechaDesc,
    OrdenarPorPuntajeDesc,
)


# ── Helper ─────────────────────────────────────────────────────────────────


def _nuevo(
    codigo: str = "EST-001",
    respuestas: list | None = None,
    fecha: datetime | None = None,
) -> CuestionarioPHQ9:
    return CuestionarioPHQ9(
        id=str(uuid.uuid4()),
        codigo_estudiante=codigo,
        fecha_aplicacion=fecha or datetime(2026, 5, 20, 10, 0),
        respuestas=respuestas or [1, 1, 1, 1, 1, 1, 1, 1, 1],
    )


# ── 1. Builder ─────────────────────────────────────────────────────────────


class TestBuilder:
    def test_construye_cuestionario_con_datos_correctos(self):
        c = (
            CuestionarioBuilder()
            .codigo("EST-2026-001")
            .fecha("20/05/2026 10:00")
            .respuestas([1, 0, 2, 1, 0, 2, 1, 0, 1])
            .construir()
        )
        assert c.codigo_estudiante == "EST-2026-001"
        assert c.puntaje_total == 8
        assert c.nivel_severidad == "Leve"

    def test_lanza_error_si_faltan_campos_obligatorios(self):
        with pytest.raises(ValueError, match="fecha"):
            (
                CuestionarioBuilder()
                .codigo("EST-001")
                .respuestas([0] * 9)
                .construir()
            )


# ── 2. Factory Method ──────────────────────────────────────────────────────


class TestFactoryMethod:
    def test_generador_texto_incluye_columnas_codigo_y_puntaje(self):
        resultado = GeneradorReporteTexto().generar([_nuevo()])
        assert "CÓDIGO" in resultado
        assert "PUNTAJE" in resultado

    def test_generador_csv_primera_linea_es_cabecera_correcta(self):
        resultado = GeneradorReporteCSV().generar([_nuevo()])
        cabecera = resultado.splitlines()[0]
        assert cabecera.startswith(
            "id,codigo_estudiante,fecha_aplicacion,puntaje_total"
        )


# ── 3. Singleton ───────────────────────────────────────────────────────────


class TestSingleton:
    def setup_method(self):
        ConfiguracionApp.resetear()

    def test_dos_llamadas_retornan_el_mismo_objeto(self):
        a = ConfiguracionApp()
        b = ConfiguracionApp()
        assert a is b

    def test_cambio_en_una_referencia_se_refleja_en_otra(self):
        a = ConfiguracionApp()
        a.version = "9.9.9"
        b = ConfiguracionApp()
        assert b.version == "9.9.9"


# ── 4. Decorator ───────────────────────────────────────────────────────────


class TestDecorator:
    def test_operacion_guardar_queda_registrada_en_el_log(self):
        repo = RepositorioConLog(RepositorioMemoria())
        repo.guardar(_nuevo("EST-001"))
        assert any("guardar" in entrada for entrada in repo.log)

    def test_decorator_delega_obtener_todos_al_repositorio_base(self):
        base = RepositorioMemoria()
        base.guardar(_nuevo("EST-001"))
        base.guardar(_nuevo("EST-002"))
        repo = RepositorioConLog(base)
        assert len(repo.obtener_todos()) == 2


# ── 5. Strategy ────────────────────────────────────────────────────────────


class TestStrategy:
    def test_ordenar_por_fecha_desc_pone_mas_reciente_primero(self):
        c1 = _nuevo(fecha=datetime(2026, 5, 1, 10, 0))
        c2 = _nuevo(fecha=datetime(2026, 5, 20, 10, 0))
        resultado = ListadorCuestionarios(OrdenarPorFechaDesc()).listar([c1, c2])
        assert resultado[0].fecha_aplicacion > resultado[1].fecha_aplicacion

    def test_ordenar_por_puntaje_desc_pone_caso_mas_severo_primero(self):
        bajo = _nuevo(respuestas=[1] * 9)   # puntaje 9
        alto = _nuevo(respuestas=[3] * 9)   # puntaje 27
        resultado = ListadorCuestionarios(OrdenarPorPuntajeDesc()).listar(
            [bajo, alto]
        )
        assert resultado[0].puntaje_total > resultado[1].puntaje_total


# ── 6. Facade ──────────────────────────────────────────────────────────────


class TestFacade:
    def test_registrar_agrega_el_cuestionario_al_repositorio(self):
        facade = SistemaEvaluacionFacade(RepositorioMemoria())
        facade.registrar("EST-001", "20/05/2026 10:00", [1] * 9)
        assert facade.estadisticas()["total"] == 1

    def test_estadisticas_calcula_promedio_correcto(self):
        facade = SistemaEvaluacionFacade(RepositorioMemoria())
        facade.registrar("EST-001", "20/05/2026 10:00", [1] * 9)  # puntaje 9
        facade.registrar("EST-002", "20/05/2026 11:00", [3] * 9)  # puntaje 27
        assert facade.estadisticas()["promedio"] == 18.0


# ── 7. Command ─────────────────────────────────────────────────────────────


class TestCommand:
    def test_registrar_y_deshacer_elimina_el_cuestionario(self):
        repo = RepositorioMemoria()
        historial = HistorialComandos()
        historial.ejecutar(RegistrarCuestionarioComando(repo, _nuevo("EST-001")))
        assert len(repo.obtener_todos()) == 1
        historial.deshacer()
        assert len(repo.obtener_todos()) == 0

    def test_eliminar_y_deshacer_restaura_el_cuestionario(self):
        repo = RepositorioMemoria()
        c = _nuevo("EST-001")
        repo.guardar(c)
        historial = HistorialComandos()
        historial.ejecutar(EliminarCuestionarioComando(repo, c.id))
        assert len(repo.obtener_todos()) == 0
        historial.deshacer()
        assert len(repo.obtener_todos()) == 1

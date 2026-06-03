"""Pruebas unitarias para los patrones Strategy y Command aplicados a GAD-7."""

import json
import pytest

from app.patterns.strategy import (
    EstrategiaCSV,
    EstrategiaJSON,
    EstrategiaTextoPlano,
    ReporteGAD7,
    ResultadoGAD7,
)
from app.patterns.command import (
    AlmacenGAD7,
    ComandoCrearCuestionario,
    ComandoEliminarCuestionario,
    CuestionarioGAD7,
    InvocadorGAD7,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def resultados():
    return [
        ResultadoGAD7("EST001", [2, 2, 1, 2, 1, 2, 2], 12, "MODERADO"),
        ResultadoGAD7("EST002", [0, 0, 1, 0, 1, 0, 0],  2, "NORMAL"),
    ]


@pytest.fixture
def cuestionario():
    return CuestionarioGAD7(
        codigo_estudiante="EST001",
        respuestas=[3, 3, 3, 2, 2, 2, 0],
        puntaje_total=15,
        nivel_severidad="SEVERO",
        id="id-001",
    )


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY
# ══════════════════════════════════════════════════════════════════════════════

class TestEstrategiaJSON:

    def test_exporta_lista_valida_como_json(self, resultados):
        """El resultado debe ser un JSON válido con los campos correctos."""
        reporte = ReporteGAD7(EstrategiaJSON())
        salida = reporte.generar(resultados)
        datos = json.loads(salida)
        assert len(datos) == 2
        assert datos[0]["codigo_estudiante"] == "EST001"
        assert datos[0]["nivel_severidad"] == "MODERADO"

    def test_exporta_lista_vacia_como_json_vacio(self):
        """Una lista vacía debe producir un arreglo JSON vacío."""
        reporte = ReporteGAD7(EstrategiaJSON())
        salida = reporte.generar([])
        assert json.loads(salida) == []


class TestEstrategiaTextoPlano:

    def test_contiene_encabezado_y_datos(self, resultados):
        """El texto debe incluir el encabezado y los datos de cada estudiante."""
        reporte = ReporteGAD7(EstrategiaTextoPlano())
        salida = reporte.generar(resultados)
        assert "=== Resultados GAD-7 ===" in salida
        assert "EST001" in salida
        assert "MODERADO" in salida

    def test_cada_estudiante_en_linea_separada(self, resultados):
        """Cada resultado debe estar en su propia línea."""
        reporte = ReporteGAD7(EstrategiaTextoPlano())
        lineas = reporte.generar(resultados).split("\n")
        # encabezado + 2 resultados = 3 líneas
        assert len(lineas) == 3


class TestEstrategiaCSV:

    def test_primera_linea_es_encabezado(self, resultados):
        """La primera línea del CSV debe ser el encabezado."""
        reporte = ReporteGAD7(EstrategiaCSV())
        lineas = reporte.generar(resultados).split("\n")
        assert lineas[0].strip() == "codigo_estudiante,puntaje_total,nivel_severidad"

    def test_csv_contiene_puntaje_correcto(self, resultados):
        """El puntaje debe aparecer en la fila correspondiente."""
        reporte = ReporteGAD7(EstrategiaCSV())
        salida = reporte.generar(resultados)
        assert "EST001,12,MODERADO" in salida


class TestCambioEstrategia:

    def test_cambiar_estrategia_en_tiempo_de_ejecucion(self, resultados):
        """El contexto debe permitir cambiar la estrategia sin crear uno nuevo."""
        reporte = ReporteGAD7(EstrategiaJSON())
        salida_json = reporte.generar(resultados)
        assert salida_json.startswith("[")

        reporte.cambiar_estrategia(EstrategiaTextoPlano())
        salida_texto = reporte.generar(resultados)
        assert "===" in salida_texto


# ══════════════════════════════════════════════════════════════════════════════
# COMMAND
# ══════════════════════════════════════════════════════════════════════════════

class TestComandoCrear:

    def test_ejecutar_agrega_cuestionario(self, cuestionario):
        """Ejecutar el comando debe agregar el cuestionario al almacén."""
        almacen = AlmacenGAD7()
        invocador = InvocadorGAD7()
        invocador.ejecutar(ComandoCrearCuestionario(almacen, cuestionario))
        assert almacen.obtener("id-001") is not None

    def test_deshacer_elimina_cuestionario_creado(self, cuestionario):
        """Deshacer la creación debe dejar el almacén vacío."""
        almacen = AlmacenGAD7()
        invocador = InvocadorGAD7()
        invocador.ejecutar(ComandoCrearCuestionario(almacen, cuestionario))
        invocador.deshacer_ultimo()
        assert almacen.obtener("id-001") is None


class TestComandoEliminar:

    def test_ejecutar_elimina_cuestionario(self, cuestionario):
        """Ejecutar el comando debe eliminar el cuestionario del almacén."""
        almacen = AlmacenGAD7()
        almacen.agregar(cuestionario)
        invocador = InvocadorGAD7()
        invocador.ejecutar(ComandoEliminarCuestionario(almacen, "id-001"))
        assert almacen.obtener("id-001") is None

    def test_deshacer_restaura_cuestionario_eliminado(self, cuestionario):
        """Deshacer la eliminación debe restaurar el cuestionario."""
        almacen = AlmacenGAD7()
        almacen.agregar(cuestionario)
        invocador = InvocadorGAD7()
        invocador.ejecutar(ComandoEliminarCuestionario(almacen, "id-001"))
        invocador.deshacer_ultimo()
        restaurado = almacen.obtener("id-001")
        assert restaurado is not None
        assert restaurado.codigo_estudiante == "EST001"


class TestInvocador:

    def test_deshacer_sin_historial_retorna_false(self):
        """Deshacer con historial vacío debe retornar False."""
        invocador = InvocadorGAD7()
        assert invocador.deshacer_ultimo() is False

    def test_multiples_comandos_deshacer_orden_lifo(self, cuestionario):
        """Deshacer múltiples comandos debe seguir orden LIFO."""
        c2 = CuestionarioGAD7("EST002", [1]*7, 7, "LEVE", id="id-002")
        almacen = AlmacenGAD7()
        invocador = InvocadorGAD7()
        invocador.ejecutar(ComandoCrearCuestionario(almacen, cuestionario))
        invocador.ejecutar(ComandoCrearCuestionario(almacen, c2))
        # deshacer el último (id-002)
        invocador.deshacer_ultimo()
        assert almacen.obtener("id-002") is None
        assert almacen.obtener("id-001") is not None

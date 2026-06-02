"""Patrón Facade: interfaz unificada al subsistema de evaluación PHQ-9."""

from __future__ import annotations

from typing import Dict, List

from app.builders.cuestionario_builder import CuestionarioBuilder
from app.factories.generador_reporte import GeneradorReporteTexto
from app.interfaces.i_repositorio_cuestionario import IRepositorioCuestionario
from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.strategies.estrategia_ordenamiento import (
    ListadorCuestionarios,
    OrdenarPorFechaDesc,
)


class SistemaEvaluacionFacade:
    """Simplifica las operaciones más frecuentes del sistema PHQ-9.

    Coordina internamente Builder, Factory Method y Strategy, exponiendo
    solo tres métodos de alto nivel al cliente externo.

    Args:
        repositorio: repositorio de persistencia a usar.
    """

    def __init__(self, repositorio: IRepositorioCuestionario) -> None:
        self._repositorio = repositorio
        self._generador = GeneradorReporteTexto()
        self._listador = ListadorCuestionarios(OrdenarPorFechaDesc())

    def registrar(
        self,
        codigo: str,
        fecha_str: str,
        respuestas: List[int],
    ) -> CuestionarioPHQ9:
        """Construye y persiste un cuestionario en un solo paso.

        Args:
            codigo: código institucional del estudiante.
            fecha_str: fecha en formato DD/MM/AAAA HH:MM.
            respuestas: lista de 9 enteros 0-3.

        Returns:
            El cuestionario creado y guardado.
        """
        cuestionario = (
            CuestionarioBuilder()
            .codigo(codigo)
            .fecha(fecha_str)
            .respuestas(respuestas)
            .construir()
        )
        self._repositorio.guardar(cuestionario)
        return cuestionario

    def reporte(self) -> str:
        """Genera un reporte de texto ordenado por fecha descendente."""
        ordenados = self._listador.listar(self._repositorio.obtener_todos())
        return self._generador.generar(ordenados)

    def estadisticas(self) -> Dict[str, object]:
        """Calcula estadísticas generales del repositorio.

        Returns:
            Dict con claves: total, promedio, casos_severos.
        """
        todos = self._repositorio.obtener_todos()
        if not todos:
            return {"total": 0, "promedio": 0.0, "casos_severos": 0}
        total = len(todos)
        promedio = round(sum(c.puntaje_total for c in todos) / total, 2)
        casos_severos = sum(1 for c in todos if c.puntaje_total >= 20)
        return {
            "total": total,
            "promedio": promedio,
            "casos_severos": casos_severos,
        }

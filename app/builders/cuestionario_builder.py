"""Patrón Builder: construye CuestionarioPHQ9 paso a paso."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from app.models.cuestionario_phq9 import CuestionarioPHQ9
from app.utils.constantes_negocio import FORMATO_FECHA_DISPLAY


class CuestionarioBuilder:
    """Construye un CuestionarioPHQ9 mediante encadenamiento de métodos.

    Garantiza que el objeto solo se crea cuando todos los campos
    obligatorios están presentes, evitando instancias incompletas.

    Ejemplo::

        c = (
            CuestionarioBuilder()
            .codigo("EST-2026-001")
            .fecha("20/05/2026 10:00")
            .respuestas([1, 0, 2, 1, 0, 2, 1, 0, 1])
            .construir()
        )
    """

    def __init__(self) -> None:
        self._codigo: Optional[str] = None
        self._fecha_str: Optional[str] = None
        self._respuestas: Optional[List[int]] = None

    def codigo(self, codigo: str) -> CuestionarioBuilder:
        """Establece el código institucional del estudiante."""
        self._codigo = codigo
        return self

    def fecha(self, fecha_str: str) -> CuestionarioBuilder:
        """Establece la fecha en formato DD/MM/AAAA HH:MM."""
        self._fecha_str = fecha_str
        return self

    def respuestas(self, respuestas: List[int]) -> CuestionarioBuilder:
        """Establece los 9 valores de respuesta (0-3)."""
        self._respuestas = respuestas
        return self

    def construir(self) -> CuestionarioPHQ9:
        """Valida campos y crea el cuestionario.

        Returns:
            Instancia de CuestionarioPHQ9 completamente validada.

        Raises:
            ValueError: si falta algún campo obligatorio.
        """
        faltantes = [
            nombre
            for nombre, valor in (
                ("codigo", self._codigo),
                ("fecha", self._fecha_str),
                ("respuestas", self._respuestas),
            )
            if not valor and valor != []
        ]
        if faltantes:
            raise ValueError(
                f"Campos obligatorios faltantes: {', '.join(faltantes)}"
            )
        fecha = datetime.strptime(self._fecha_str, FORMATO_FECHA_DISPLAY)
        return CuestionarioPHQ9(
            id=str(uuid.uuid4()),
            codigo_estudiante=self._codigo,
            fecha_aplicacion=fecha,
            respuestas=self._respuestas,
        )

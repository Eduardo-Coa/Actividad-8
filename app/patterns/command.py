"""Patrón Command aplicado a GAD-7.

Problema: las operaciones CRUD sobre cuestionarios GAD-7 deben poder
deshacerse (undo). Encapsular cada operación como un objeto permite
almacenarlas en un historial y revertirlas.

Definición formal: Command encapsula una solicitud como un objeto,
permitiendo parametrizar clientes con distintas solicitudes, encolar
operaciones y soportar operaciones deshacer/rehacer.
(Gamma et al., Design Patterns, 1994)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Modelo simplificado GAD-7 ─────────────────────────────────────────────────

@dataclass
class CuestionarioGAD7:
    codigo_estudiante: str
    respuestas: List[int]
    puntaje_total: int
    nivel_severidad: str
    id: str = ""


# ── Receptor: almacén en memoria ──────────────────────────────────────────────

class AlmacenGAD7:
    """Receptor que mantiene los cuestionarios en memoria."""

    def __init__(self) -> None:
        self._datos: Dict[str, CuestionarioGAD7] = {}

    def agregar(self, cuestionario: CuestionarioGAD7) -> None:
        self._datos[cuestionario.id] = cuestionario

    def eliminar(self, id_cuestionario: str) -> Optional[CuestionarioGAD7]:
        return self._datos.pop(id_cuestionario, None)

    def obtener(self, id_cuestionario: str) -> Optional[CuestionarioGAD7]:
        return self._datos.get(id_cuestionario)

    def listar(self) -> List[CuestionarioGAD7]:
        return list(self._datos.values())


# ── Interfaz Command ──────────────────────────────────────────────────────────

class Comando(ABC):
    """Contrato para todos los comandos del sistema GAD-7."""

    @abstractmethod
    def ejecutar(self) -> None:
        """Ejecuta la operación."""

    @abstractmethod
    def deshacer(self) -> None:
        """Revierte la operación."""


# ── Comandos concretos ────────────────────────────────────────────────────────

class ComandoCrearCuestionario(Comando):
    """Crea un cuestionario en el almacén; deshacer lo elimina."""

    def __init__(self, almacen: AlmacenGAD7, cuestionario: CuestionarioGAD7) -> None:
        self._almacen = almacen
        self._cuestionario = cuestionario

    def ejecutar(self) -> None:
        self._almacen.agregar(self._cuestionario)

    def deshacer(self) -> None:
        self._almacen.eliminar(self._cuestionario.id)


class ComandoEliminarCuestionario(Comando):
    """Elimina un cuestionario; deshacer lo restaura."""

    def __init__(self, almacen: AlmacenGAD7, id_cuestionario: str) -> None:
        self._almacen = almacen
        self._id = id_cuestionario
        self._respaldo: Optional[CuestionarioGAD7] = None

    def ejecutar(self) -> None:
        self._respaldo = self._almacen.eliminar(self._id)

    def deshacer(self) -> None:
        if self._respaldo is not None:
            self._almacen.agregar(self._respaldo)


# ── Invocador ─────────────────────────────────────────────────────────────────

class InvocadorGAD7:
    """Invocador que ejecuta comandos y mantiene historial para undo."""

    def __init__(self) -> None:
        self._historial: List[Comando] = []

    def ejecutar(self, comando: Comando) -> None:
        """Ejecuta el comando y lo agrega al historial."""
        comando.ejecutar()
        self._historial.append(comando)

    def deshacer_ultimo(self) -> bool:
        """Deshace el último comando ejecutado. Retorna False si no hay historial."""
        if not self._historial:
            return False
        self._historial.pop().deshacer()
        return True

"""Pruebas del patron Builder aplicado a Estudiante."""

import pytest

from app.exceptions import EstudianteInvalidoError
from app.patterns.builder import EstudianteBuilder


def test_builder_construye_estudiante_valido() -> None:
    """Debe construir un estudiante completo y normalizado."""
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

    assert estudiante.codigo == "EST001"
    assert estudiante.correo == "ana.lopez@universidad.edu"
    assert estudiante.programa == "Ciencia de Datos"


def test_builder_rechaza_estudiante_sin_edad() -> None:
    """Debe fallar cuando faltan datos obligatorios."""
    builder = (
        EstudianteBuilder()
        .con_codigo("est002")
        .con_nombre("Carlos Ruiz")
        .con_semestre(2)
        .con_correo("carlos@universidad.edu")
        .con_programa("Psicologia")
    )

    with pytest.raises(EstudianteInvalidoError):
        builder.construir()

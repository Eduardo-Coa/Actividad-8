"""Pruebas del patron Factory Method aplicado a Estudiante."""

from app.patterns.builder import EstudianteBuilder
from app.patterns.factory_method import obtener_creator
from app.repositories.estudiante_repository import (
    EstudianteJsonRepository,
    EstudianteMemoryRepository,
)


def crear_estudiante_prueba():
    """Crea un estudiante valido para las pruebas."""
    return (
        EstudianteBuilder()
        .con_codigo("est010")
        .con_nombre("Laura Gomez")
        .con_edad(19)
        .con_semestre(3)
        .con_correo("laura@universidad.edu")
        .con_programa("Ciencia de Datos")
        .construir()
    )


def test_factory_method_crea_repositorio_en_memoria() -> None:
    """Debe crear un repositorio en memoria usando el creator."""
    repositorio = obtener_creator("memoria").crear_repositorio()
    repositorio.guardar(crear_estudiante_prueba())

    assert isinstance(repositorio, EstudianteMemoryRepository)
    assert len(repositorio.listar()) == 1


def test_factory_method_crea_repositorio_json(tmp_path) -> None:
    """Debe crear un repositorio JSON usando el creator."""
    ruta = tmp_path / "estudiantes.json"
    repositorio = obtener_creator("json", str(ruta)).crear_repositorio()
    repositorio.guardar(crear_estudiante_prueba())

    assert isinstance(repositorio, EstudianteJsonRepository)
    assert repositorio.listar()[0].codigo == "EST010"

"""Pruebas de Facade y Decorator aplicados a sesiones y psicologos."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.decorators.servicio_sesion_decorator import (
    DecoradorLog,
    DecoradorValidacion,
    ServicioSesionConcreto,
)
from app.facades.sistema_seguimiento_facade import SistemaSeguimientoFacade
from app.models.psicologo import Psicologo
from app.models.sesion_seguimiento import SesionSeguimiento


def crear_psicologo(id_psicologo: str = "PSI-001") -> Psicologo:
    return Psicologo(
        id=id_psicologo,
        nombre="Laura Perez",
        correo="laura@universidad.edu",
        especialidad="Ansiedad academica",
    )


def crear_sesion(id_psicologo: str = "PSI-001") -> SesionSeguimiento:
    return SesionSeguimiento(
        codigo_estudiante="EST-001",
        id_psicologo=id_psicologo,
        fecha_hora=datetime(2026, 6, 2, 10, 0),
        duracion_minutos=45,
        motivo="Seguimiento emocional",
    )


class TestFacade:
    def test_agendar_sesion_registra_psicologo_y_sesion(self) -> None:
        facade = SistemaSeguimientoFacade()

        facade.registrar_psicologo(
            "PSI-001",
            "Laura Perez",
            "laura@universidad.edu",
            "Ansiedad academica",
        )
        sesion = facade.agendar_sesion(
            "EST-001",
            "PSI-001",
            datetime(2026, 6, 2, 10, 0),
            45,
            "Seguimiento emocional",
        )

        assert sesion.codigo_estudiante == "EST-001"
        assert facade.resumen() == {"psicologos": 1, "sesiones": 1}

    def test_agendar_sesion_rechaza_psicologo_inexistente(self) -> None:
        facade = SistemaSeguimientoFacade()

        with pytest.raises(ValueError, match="No existe"):
            facade.agendar_sesion(
                "EST-001",
                "PSI-999",
                datetime(2026, 6, 2, 10, 0),
                45,
                "Seguimiento emocional",
            )


class TestDecorator:
    def test_log_agrega_marca_de_tiempo_al_resultado(self) -> None:
        servicio = DecoradorLog(ServicioSesionConcreto())

        resultado = servicio.describir(crear_sesion(), crear_psicologo())

        assert "Log: descripcion generada en" in resultado
        assert "Sesion AGENDADA" in resultado

    def test_validacion_rechaza_psicologo_que_no_corresponde(self) -> None:
        servicio = DecoradorValidacion(ServicioSesionConcreto())

        with pytest.raises(ValueError, match="no pertenece"):
            servicio.describir(crear_sesion("PSI-001"), crear_psicologo("PSI-002"))

"""Builder aplicado a la entidad Estudiante."""

from __future__ import annotations

from datetime import datetime

from app.exceptions import EstudianteInvalidoError
from app.models.estudiante import Estudiante


class EstudianteBuilder:
    """Construye estudiantes paso a paso.

    El builder evita constructores largos en la UI o en servicios, y
    centraliza la preparacion de los datos antes de crear la entidad.
    """

    def __init__(self) -> None:
        self._codigo = ""
        self._nombre_completo = ""
        self._edad: int | None = None
        self._semestre: int | None = None
        self._correo = ""
        self._programa = ""
        self._fecha_registro = datetime.now()

    def con_codigo(self, codigo: str) -> EstudianteBuilder:
        """Asigna el codigo institucional.

        Args:
            codigo: codigo del estudiante.

        Returns:
            Builder actual.
        """
        self._codigo = codigo
        return self

    def con_nombre(self, nombre_completo: str) -> EstudianteBuilder:
        """Asigna el nombre completo.

        Args:
            nombre_completo: nombres y apellidos.

        Returns:
            Builder actual.
        """
        self._nombre_completo = nombre_completo
        return self

    def con_edad(self, edad: int) -> EstudianteBuilder:
        """Asigna la edad.

        Args:
            edad: edad del estudiante.

        Returns:
            Builder actual.
        """
        self._edad = edad
        return self

    def con_semestre(self, semestre: int) -> EstudianteBuilder:
        """Asigna el semestre.

        Args:
            semestre: semestre academico.

        Returns:
            Builder actual.
        """
        self._semestre = semestre
        return self

    def con_correo(self, correo: str) -> EstudianteBuilder:
        """Asigna el correo.

        Args:
            correo: correo del estudiante.

        Returns:
            Builder actual.
        """
        self._correo = correo
        return self

    def con_programa(self, programa: str) -> EstudianteBuilder:
        """Asigna el programa academico.

        Args:
            programa: programa del estudiante.

        Returns:
            Builder actual.
        """
        self._programa = programa
        return self

    def con_fecha_registro(
        self,
        fecha_registro: datetime,
    ) -> EstudianteBuilder:
        """Asigna la fecha de registro.

        Args:
            fecha_registro: fecha de creacion del estudiante.

        Returns:
            Builder actual.
        """
        self._fecha_registro = fecha_registro
        return self

    def construir(self) -> Estudiante:
        """Construye el estudiante validado.

        Returns:
            Estudiante listo para persistir.
        """
        if self._edad is None or self._semestre is None:
            raise EstudianteInvalidoError(
                "Edad y semestre son obligatorios para construir."
            )
        return Estudiante(
            codigo=self._codigo,
            nombre_completo=self._nombre_completo,
            edad=self._edad,
            semestre=self._semestre,
            correo=self._correo,
            programa=self._programa,
            fecha_registro=self._fecha_registro,
        )

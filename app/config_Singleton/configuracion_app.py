"""Patrón Singleton: configuración global única de la aplicación."""

from __future__ import annotations

from typing import Optional


class ConfiguracionApp:
    """Configuración global de la aplicación (instancia única).

    Todos los módulos obtienen la misma instancia; cualquier cambio
    en una referencia se refleja en todas las demás.

    Ejemplo::

        cfg = ConfiguracionApp()
        print(cfg.nombre_app)   # 'Sistema PHQ-9'
    """

    _instancia: Optional[ConfiguracionApp] = None

    def __new__(cls) -> ConfiguracionApp:
        if cls._instancia is None:
            obj = super().__new__(cls)
            obj._inicializar()
            cls._instancia = obj
        return cls._instancia

    def _inicializar(self) -> None:
        self.nombre_app: str = "Sistema PHQ-9"
        self.version: str = "1.0.0"
        self.ruta_datos: str = "data/cuestionarios.json"
        self.umbral_severo: int = 20
        self.umbral_modsevero: int = 15
        self.umbral_moderado: int = 10
        self.umbral_leve: int = 5

    @classmethod
    def resetear(cls) -> None:
        """Elimina la instancia activa. Solo para pruebas unitarias."""
        cls._instancia = None

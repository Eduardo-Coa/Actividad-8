# Actividad 8 — Patrones de Diseño GoF

**Materia:** Lenguaje de Programación · 3er semestre, Ciencia de Datos  
**Lenguaje:** Python 3.10+

---

## Descripción

Demostración de 7 patrones de diseño GoF aplicados a un sistema de evaluación del cuestionario **PHQ-9** (escala de depresión). Cada patrón resuelve un problema concreto dentro del dominio.

---

## Patrones implementados

| # | Patrón | Carpeta | Propósito |
|---|--------|---------|-----------|
| 1 | **Builder** | `app/builders/` | Construcción paso a paso de un cuestionario |
| 2 | **Factory Method** | `app/factories/` | Generación de reportes en texto y CSV |
| 3 | **Singleton** | `app/config/` | Configuración global única de la aplicación |
| 4 | **Decorator** | `app/decorators/` | Repositorio con registro de operaciones (log) |
| 5 | **Strategy** | `app/strategies/` | Ordenamiento intercambiable de cuestionarios |
| 6 | **Facade** | `app/facades/` | Interfaz simplificada para registrar y consultar resultados |
| 7 | **Command** | `app/commands/` | Operaciones CRUD con soporte de deshacer (undo) |

---

## Estructura

```
Actividad 8/
├── main.py              # Punto de entrada; ejecuta los 7 patrones
├── app/
│   ├── models/          # Entidad Cuestionario PHQ-9
│   ├── interfaces/      # Contratos (ABCs)
│   ├── repositories/    # Almacenamiento en memoria
│   ├── builders/        # Patrón Builder
│   ├── factories/       # Patrón Factory Method
│   ├── config/          # Patrón Singleton
│   ├── decorators/      # Patrón Decorator
│   ├── strategies/      # Patrón Strategy
│   ├── facades/         # Patrón Facade
│   └── commands/        # Patrón Command
└── tests/               # Pruebas unitarias por patrón
```

---

## Ejecución

```bash
# Ejecutar la demostración completa
python main.py

# Ejecutar los tests
python -m pytest

# Verificar estilo PEP 8
flake8 . --max-line-length=79
```

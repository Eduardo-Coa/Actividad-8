# Actividad 8 — Patrones de Diseño GoF

**Materia:** Lenguaje de Programación · 3er semestre, Ciencia de Datos
**Lenguaje:** Python 3.10+
**Repositorio:** https://github.com/Eduardo-Coa/Actividad-8

---

## Equipo

| Integrante | Rama | Módulo |
|---|---|---|
| Didier Eduardo Coa | `dev_dcoa37` | Sistema PHQ-9 — 7 patrones GoF |
| C. Huertas | `dev_chuertas21` | Módulo de seguimiento psicológico |
| D. Pérez | `dev_dperez37` | Sistema GAD-7 — Strategy y Command |
| W. Ramírez | `dev_wramirez72` | Gestión de estudiantes — Builder y Factory Method |

---

## Descripción general

Sistema de apoyo a la salud mental estudiantil que combina tres instrumentos clínicos estandarizados:

- **PHQ-9** (Patient Health Questionnaire) — detección de depresión
- **GAD-7** (Generalized Anxiety Disorder) — detección de ansiedad
- **Gestión de estudiantes** — registro y validación de datos académicos

Cada módulo demuestra patrones de diseño GoF aplicados a problemas concretos del dominio.

---

## Patrones implementados

| Patrón | Categoría | Integrante | Aplicación |
|---|---|---|---|
| **Builder** | Creacional | Eduardo Coa | Construcción paso a paso de `CuestionarioPHQ9` |
| **Builder** | Creacional | W. Ramírez | Construcción de `Estudiante` con `EstudianteBuilder` |
| **Factory Method** | Creacional | Eduardo Coa | Generadores de reporte en texto y CSV |
| **Factory Method** | Creacional | W. Ramírez | Selección de repositorio en memoria o JSON |
| **Singleton** | Creacional | Eduardo Coa | `ConfiguracionApp` — configuración global única |
| **Decorator** | Estructural | Eduardo Coa | `RepositorioConLog` — log transparente de operaciones |
| **Decorator** | Estructural | C. Huertas | `ServicioSesionDecorator` — seguimiento de sesiones |
| **Facade** | Estructural | Eduardo Coa | `SistemaEvaluacionFacade` — interfaz unificada PHQ-9 |
| **Facade** | Estructural | C. Huertas | `SistemaSeguimientoFacade` — gestión de psicólogos y sesiones |
| **Strategy** | Comportamiento | Eduardo Coa | Ordenamiento de cuestionarios por fecha, puntaje o código |
| **Strategy** | Comportamiento | D. Pérez | Exportación GAD-7 en JSON, texto plano y CSV |
| **Command** | Comportamiento | Eduardo Coa | CRUD con undo/redo sobre repositorio PHQ-9 |
| **Command** | Comportamiento | D. Pérez | CRUD con undo/redo sobre almacén GAD-7 |

---

## Módulos por integrante

### Eduardo Coa — Sistema PHQ-9 (`dev_dcoa37`)

Implementa los **7 patrones GoF** aplicados al cuestionario PHQ-9 (escala 0–27 pts).

```
app/
├── builders/cuestionario_builder.py       # Builder
├── factories/generador_reporte.py         # Factory Method
├── config_Singleton/configuracion_app.py  # Singleton
├── decorators/repositorio_con_log.py      # Decorator
├── strategies/estrategia_ordenamiento.py  # Strategy
├── facades/sistema_evaluacion_facade.py   # Facade
├── commands/comandos_cuestionario.py      # Command
├── models/cuestionario_phq9.py
├── interfaces/i_repositorio_cuestionario.py
└── repositories/repositorio_memoria.py
tests/test_patrones.py                     # 14 pruebas (2 por patrón)
```

Clasificación de severidad PHQ-9:

| Puntaje | Nivel |
|---|---|
| 0 – 4 | Mínimo |
| 5 – 9 | Leve |
| 10 – 14 | Moderado |
| 15 – 19 | Moderadamente severo |
| 20 – 27 | Severo |

---

### C. Huertas — Seguimiento psicológico (`dev_chuertas21`)

Extiende el sistema PHQ-9 con un módulo de seguimiento entre estudiantes y psicólogos.

```
app/
├── models/psicologo.py                        # Entidad Psicologo
├── models/sesion_seguimiento.py               # Entidad SesionSeguimiento
├── decorators/servicio_sesion_decorator.py    # Decorator
├── facades/sistema_seguimiento_facade.py      # Facade
└── src/exceptions/validation_errors.py       # Excepciones de dominio
tests/test_facade_decorator.py
```

Funcionalidades clave:
- Registro de psicólogos con validación de correo
- Agendamiento de sesiones (estados: `AGENDADA`, `REALIZADA`, `CANCELADA`)
- Consulta de sesiones por estudiante

---

### D. Pérez — Sistema GAD-7 (`dev_dperez37`)

Implementa **Strategy** y **Command** aplicados al cuestionario GAD-7 (escala de ansiedad, 0–21 pts).

```
app/patterns/
├── strategy.py   # Exportación en JSON, texto plano y CSV
└── command.py    # CRUD con undo sobre AlmacenGAD7
tests/test_patterns.py
```

Estrategias de exportación disponibles: `EstrategiaJSON`, `EstrategiaTextoPlano`, `EstrategiaCSV`.

---

### W. Ramírez — Gestión de estudiantes (`dev_wramirez72`)

Implementa **Builder** y **Factory Method** para el registro y persistencia de estudiantes.

```
app/
├── models/estudiante.py                        # Entidad Estudiante
├── patterns/builder.py                         # EstudianteBuilder
├── patterns/factory_method.py                  # EstudianteRepositoryCreator
└── repositories/estudiante_repository.py       # Memoria y JSON
tests/
├── test_builder.py
└── test_factory_method.py
```

Validaciones del modelo `Estudiante`: edad (14–100), semestre (1–12), correo válido.
Repositorios disponibles: en memoria o persistido en archivo JSON.

---

## Estructura global del proyecto

```
Actividad 8/
├── main.py
├── app/
│   ├── builders/
│   ├── commands/
│   ├── config_Singleton/
│   ├── decorators/
│   ├── facades/
│   ├── factories/
│   ├── interfaces/
│   ├── models/
│   ├── patterns/
│   ├── repositories/
│   ├── strategies/
│   └── utils/
├── tests/
└── docs/
```

---

## Ejecución

```bash
# Ejecutar la demostración completa
python main.py

# Ejecutar todos los tests
python -m pytest

# Ejecutar tests de un módulo específico
python -m pytest tests/test_patrones.py -v

# Verificar estilo PEP 8
flake8 . --max-line-length=79
```

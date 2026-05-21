# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Actividad académica para la materia **Lenguaje de Programación** — 3er semestre, Ciencia de Datos.
Todo el código debe estar escrito en **Python 3.10+**.

---

## Principios obligatorios

### SOLID
- **S** — Single Responsibility: cada clase/función tiene una única razón para cambiar.
- **O** — Open/Closed: abierto para extensión, cerrado para modificación (usar herencia o composición, no `if-elif` interminables).
- **L** — Liskov Substitution: las subclases deben poder sustituir a su clase base sin romper el comportamiento.
- **I** — Interface Segregation: interfaces pequeñas y específicas; no forzar dependencias innecesarias.
- **D** — Dependency Inversion: depender de abstracciones (`ABC`, protocolos), no de implementaciones concretas.

### Clean Code
- Nombres descriptivos y pronunciables (`calcular_promedio`, no `cp`).
- Funciones cortas (máx. ~20 líneas); hacen una sola cosa.
- Sin números mágicos — usar constantes con nombre.
- Sin comentarios que expliquen el *qué*; solo los que expliquen el *por qué* cuando no es obvio.
- DRY: no duplicar lógica; extraer a función o clase si aparece más de una vez.

### PEP 8
- Indentación: 4 espacios.
- Líneas máx. 79 caracteres (docstrings/comentarios: 72).
- 2 líneas en blanco entre clases/funciones de nivel superior; 1 línea entre métodos.
- Imports ordenados: stdlib → third-party → local, separados por línea en blanco.
- Nombres: `snake_case` para variables/funciones, `PascalCase` para clases, `UPPER_CASE` para constantes.
- Espacios alrededor de operadores (`x = 1 + 2`), sin espacios dentro de paréntesis (`f(a, b)`).

### Heurísticas de Nielsen (para interfaces de consola/CLI)
1. **Visibilidad del estado** — mostrar siempre en qué paso/estado se encuentra el programa.
2. **Coincidencia sistema-mundo real** — usar lenguaje del dominio, no jerga técnica, en los mensajes al usuario.
3. **Control y libertad** — ofrecer opción de cancelar o volver atrás cuando sea posible.
4. **Consistencia** — los mensajes, prompts y formatos de salida deben ser uniformes.
5. **Prevención de errores** — validar entradas antes de procesarlas y guiar al usuario con ejemplos en el prompt.
6. **Reconocimiento antes que recuerdo** — mostrar opciones disponibles; no obligar al usuario a memorizar comandos.
7. **Flexibilidad** — el programa debe manejar tanto entradas en mayúsculas como minúsculas.
8. **Diseño minimalista** — no mostrar información irrelevante; cada línea de salida debe tener propósito.
9. **Mensajes de error claros** — describir el problema en lenguaje llano y sugerir la solución.
10. **Ayuda y documentación** — incluir opción `ayuda` o `--help` con instrucciones de uso.

---

## Comandos de desarrollo

```bash
# Ejecutar el programa principal
python main.py

# Ejecutar todos los tests
python -m pytest

# Ejecutar un test específico
python -m pytest tests/test_<modulo>.py::NombreTest::nombre_metodo -v

# Verificar estilo PEP 8
flake8 . --max-line-length=79

# Verificar tipos estáticos
mypy . --strict

# Formatear automáticamente
black . --line-length 79
```

---

## Arquitectura del proyecto

```
Actividad 7/
├── main.py                # Punto de entrada; solo instancia y arranca la app
├── app/
│   ├── models/            # Entidades del dominio (clases de datos puras)
│   ├── services/          # Lógica de negocio (depende de abstracciones)
│   ├── repositories/      # Acceso a datos (archivos, BD, memoria)
│   ├── interfaces/        # ABCs / Protocolos que definen contratos
│   └── ui/                # Capa de presentación (consola/CLI)
└── tests/                 # Espeja la estructura de app/
```

- `models/` no importa nada de `services/` ni `ui/`.
- `services/` recibe dependencias por inyección (constructor); nunca instancia repositorios directamente.
- `ui/` solo llama a `services/`; no contiene lógica de negocio.
- Los contratos entre capas se definen en `interfaces/` usando `abc.ABC` o `typing.Protocol`.

---

## Convenciones de este proyecto

- Toda función pública lleva **docstring** en formato Google Style.
- Los tipos deben anotarse en todas las firmas (`def foo(x: int) -> str:`).
- Las excepciones de dominio se definen en `app/exceptions.py` y heredan de una base común.
- Los mensajes que ve el usuario se centralizan en `app/ui/mensajes.py` como constantes.

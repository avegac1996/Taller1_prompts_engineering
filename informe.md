# Informe de entrega - Taller 1: Prompts Engineering

## Datos generales

- **Asignatura:** Taller 1: Prompts Engineering
- **Tema:** Crear una aplicación de Lista de Tareas en Python desde la terminal utilizando prompt engineering.
- **Nombre del estudiante:** Jhossua Vega
- **Fecha de entrega:** jueves, 2 de julio de 2026

## Proveedor y modelo de IA utilizado

- **Proveedor:** Cascade (asistente de código integrado en el IDE)
- **Modelo de IA:** OpenAI GPT-4o

## Prompts utilizados

Se diseñaron cuatro prompts estructurados siguiendo la guía de **El buen prompt**, ampliada con secciones de **QA** y **UX** para garantizar un entregable robusto, ordenado y profesional. Los prompts completos están en `prompts.md`.

1. **Prompt 1 - Arquitectura, dominio, persistencia y pruebas:** diseño de la clase `TaskManager`, persistencia JSON, validaciones y suite de pruebas unitarias.
2. **Prompt 2 - Interfaz de línea de comandos (CLI):** integración de `argparse` con subcomandos, manejo de errores y códigos de salida.
3. **Prompt 3 - Funcionalidades avanzadas, filtros y control de calidad:** prioridades, fechas límite, filtros (`hoy`, `vencidas`), ordenamiento, búsqueda y detección de tareas vencidas.
4. **Prompt 4 - UX profesional, colores, exportación CSV y documentación:** colores opcionales, formato alineado, exportación CSV, README, requirements, `.gitignore`, informe y capturas.

## Resultado final

La aplicación entregada es una **Lista de Tareas profesional** que se ejecuta completamente desde la terminal. El código está organizado en una capa de dominio (`TaskManager`) separada de la capa de presentación (CLI), lo que facilita el mantenimiento, las pruebas y futuras extensiones.

### Funciones principales

| Comando | Descripción |
|---------|-------------|
| `add` | Agregar tarea con título, descripción, prioridad y fecha límite |
| `list` | Listar tareas con filtros (`todas`, `pendientes`, `completadas`, `hoy`, `vencidas`) y ordenamiento |
| `done` | Marcar tarea como completada |
| `delete` | Eliminar tarea por ID |
| `edit` | Editar título, descripción, prioridad o fecha límite |
| `search` | Buscar tareas por palabra clave (case-insensitive) |
| `stats` | Estadísticas: total, completadas, pendientes, vencidas y progreso |
| `export` | Exportar tareas a CSV codificado en UTF-8 |

### Persistencia

Las tareas se almacenan en un archivo JSON en el directorio personal del usuario:

```text
%USERPROFILE%\.todo_cli\tasks.json
```

## Calidad y pruebas (QA)

- Se implementó una **suite de 23 pruebas unitarias** en `tests/test_todo.py` usando `unittest` y archivos temporales.
- Las pruebas cubren: validaciones, CRUD, búsqueda, filtros, ordenamiento, detección de vencidas, exportación CSV y persistencia.
- Los errores se manejan con mensajes claros dirigidos a `stderr` y códigos de salida distintos de cero.
- El archivo JSON corrupto se recupera devolviendo una lista vacía, evitando que la aplicación se detenga.

Comando para ejecutar las pruebas:

```powershell
python -m unittest discover tests
```

## Experiencia de usuario (UX)

- Colores semánticos opcionales con `colorama`: alta (rojo), media (amarillo), baja (verde).
- Fechas límite vencidas se resaltan en rojo para tareas pendientes.
- Tabla alineada sin emojis, compatible con CMD, PowerShell y Windows Terminal.
- Mensajes de error indican la causa y el formato esperado.
- La ayuda del programa (`python todo.py --help`) está en español y es clara.

## Repositorio en GitHub

- **URL:** [https://github.com/avegac1996/Taller1_prompts_engineering.git](https://github.com/avegac1996/Taller1_prompts_engineering.git)

## Estado del repositorio local

El repositorio Git está inicializado en:

```text
C:\Users\JhossuaVega\Downloads\taller_ia
```

Los commits incluyen el código fuente, las pruebas, la documentación y las capturas de verificación.

## Cómo ejecutar la aplicación

```powershell
# Instalar dependencia opcional
pip install -r requirements.txt

# Ejemplos de uso
python todo.py add "Estudiar prompts" -p alta --due 2026-07-05
python todo.py list
python todo.py list --status vencidas --sort fecha
python todo.py done 1
python todo.py stats
python todo.py export tareas.csv
```

## Capturas de verificación

Las pruebas manuales en terminal se documentan en `capturas.md`.


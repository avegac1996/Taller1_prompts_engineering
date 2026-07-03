# Lista de Tareas - Terminal (Python)

Aplicación profesional de lista de tareas (Todo List) que se ejecuta completamente desde la terminal. Construida con prompt engineering, enfoque de calidad (QA) y buena experiencia de usuario (UX).

## Requisitos

- Python 3.10 o superior (probado en Python 3.14)
- (Opcional) `colorama` para colores en Windows: `pip install -r requirements.txt`

## Instalación

```powershell
pip install -r requirements.txt
```

## Uso básico

```powershell
python todo.py add "Estudiar prompts" -p alta --due 2026-07-05
python todo.py add "Hacer ejercicio" -d "30 minutos" -p media
python todo.py list
python todo.py done 1
python todo.py stats
python todo.py export tareas.csv
```

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `add` | Agregar una tarea |
| `list` | Listar tareas con filtros y ordenamiento |
| `done` | Marcar tarea como completada |
| `delete` | Eliminar una tarea |
| `edit` | Editar una tarea |
| `search` | Buscar tareas por palabra clave |
| `stats` | Ver estadísticas |
| `export` | Exportar tareas a CSV |

## Filtros y ordenamiento

```powershell
# Filtrar por estado
python todo.py list --status pendientes
python todo.py list --status completadas
python todo.py list --status hoy
python todo.py list --status vencidas

# Filtrar por prioridad
python todo.py list --priority alta

# Ordenar resultados
python todo.py list --sort prioridad
python todo.py list --sort fecha
```

## Persistencia

Las tareas se guardan en un archivo JSON en el directorio personal del usuario:

```text
%USERPROFILE%\.todo_cli\tasks.json
```

## Calidad y pruebas

El proyecto incluye una suite de pruebas unitarias en `tests/test_todo.py`.

```powershell
python -m unittest discover tests
```

Las pruebas cubren validaciones, CRUD, filtros, búsqueda, ordenamiento, detección de tareas vencidas y exportación CSV.

## Colores en terminal

Si instalas `colorama`, las prioridades se muestran con colores semánticos:

- **Alta:** rojo
- **Media:** amarillo
- **Baja:** verde
- **Fechas vencidas:** rojo (solo tareas pendientes)

Sin `colorama`, el programa funciona exactamente igual en texto plano.

## Créditos

Generado mediante prompts estructurados con enfoque de QA y UX usando el asistente Cascade con OpenAI GPT-4o.


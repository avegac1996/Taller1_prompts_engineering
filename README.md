# Lista de Tareas - Terminal (Python)

Aplicación de lista de tareas (Todo List) que funciona completamente desde la línea de comandos, construida con prompt engineering.

## Requisitos

- Python 3.10 o superior
- (Opcional) `colorama` para colores en Windows: `pip install -r requirements.txt`

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python todo.py add "Estudiar prompts" -p alta --due 2026-07-05
python todo.py list
python todo.py done 1
python todo.py stats
python todo.py export tareas.csv
```

## Comandos disponibles

| Comando | Descripción |
|--------|--------------|
| `add` | Agregar una tarea |
| `list` | Listar tareas (con filtros y ordenamiento) |
| `done` | Marcar tarea como completada |
| `delete` | Eliminar una tarea |
| `edit` | Editar una tarea |
| `search` | Buscar tareas por palabra clave |
| `stats` | Ver estadísticas |
| `export` | Exportar tareas a CSV |

## Persistencia

Las tareas se guardan en `%USERPROFILE%\.todo_cli\tasks.json`.

## Créditos

Generado mediante prompts estructurados usando el asistente Cascade con OpenAI GPT-4o.


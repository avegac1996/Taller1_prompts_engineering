# Capturas de verificación - Taller 1

A continuación se documentan las pruebas realizadas en la terminal para cada uno de los prompts. Se aplican criterios de calidad (QA) y experiencia de usuario (UX). Los datos se almacenan en `%USERPROFILE%\.todo_cli\tasks.json`.

---

## Prompt 1 - Arquitectura, dominio, persistencia y pruebas

### Ejecución de la suite de pruebas unitarias

```powershell
$ python -m unittest discover tests
.........................
----------------------------------------------------------------------
Ran 23 tests in 0.090s

OK
```

### Persistencia y recuperación de JSON corrupto

```powershell
# Si el archivo JSON se corrompe, la aplicación se recupera devolviendo una lista vacía.
```

---

## Prompt 2 - Interfaz de línea de comandos (CLI)

### Ayuda general

```powershell
$ python todo.py --help
usage: todo [-h] {add,list,done,delete,edit,search,stats,export} ...

Lista de tareas multiplataforma desde la terminal.

positional arguments:
  {add,list,done,delete,edit,search,stats,export}
    add                 Agregar una tarea
    list                Listar tareas
    done                Marcar una tarea como completada
    delete              Eliminar una tarea
    edit                Editar una tarea
    search              Buscar tareas por palabra clave
    stats               Ver estadísticas
    export              Exportar tareas a CSV

options:
  -h, --help            show this help message and exit
```

### Manejo de errores

```powershell
$ python todo.py add "Test" -p invalida
usage: todo add [-h] [-d DESCRIPTION] [-p {baja,media,alta}] [--due DUE] title
todo add: error: argument -p/--priority: invalid choice: 'invalida' (choose from baja, media, alta)
Exit: 2

$ python todo.py done 999
No se encontró la tarea #999.
Exit: 1
```

---

## Prompt 3 - Funcionalidades avanzadas, filtros y control de calidad

### Agregar tareas con prioridad y fecha límite

```powershell
$ python todo.py add "Estudiar prompts" -d "Repasar estructura" -p alta --due 2026-07-02
Tarea agregada: #1 - Estudiar prompts

$ python todo.py add "Hacer ejercicio" -p media
Tarea agregada: #2 - Hacer ejercicio

$ python todo.py add "Pagar servicios" -p alta --due 2026-07-01
Tarea agregada: #3 - Pagar servicios

$ python todo.py add "Leer libro" -p baja --due 2026-07-10
Tarea agregada: #4 - Leer libro
```

### Listado general

```powershell
$ python todo.py list
[ ] #  1 | Estudiar prompts               | Prioridad: ALTA | Fecha: 2026-07-02
      Repasar estructura
[ ] #  2 | Hacer ejercicio                | Prioridad: MEDIA | Fecha: sin fecha
[ ] #  3 | Pagar servicios                | Prioridad: ALTA | Fecha: 2026-07-01
[ ] #  4 | Leer libro                     | Prioridad: BAJA | Fecha: 2026-07-10
```

### Filtros por estado

```powershell
$ python todo.py list --status hoy
[ ] #  1 | Estudiar prompts               | Prioridad: ALTA | Fecha: 2026-07-02
      Repasar estructura

$ python todo.py list --status vencidas
[ ] #  3 | Pagar servicios                | Prioridad: ALTA | Fecha: 2026-07-01

$ python todo.py list --status pendientes
[ ] #  2 | Hacer ejercicio                | Prioridad: MEDIA | Fecha: sin fecha
[ ] #  3 | Pagar servicios                | Prioridad: ALTA | Fecha: 2026-07-01
[ ] #  4 | Leer libro                     | Prioridad: BAJA | Fecha: 2026-07-10
```

### Filtros por prioridad y ordenamiento

```powershell
$ python todo.py list --priority alta
[ ] #  1 | Estudiar prompts               | Prioridad: ALTA | Fecha: 2026-07-02
      Repasar estructura
[ ] #  3 | Pagar servicios                | Prioridad: ALTA | Fecha: 2026-07-01

$ python todo.py list --sort fecha
[ ] #  3 | Pagar servicios                | Prioridad: ALTA | Fecha: 2026-07-01
[ ] #  1 | Estudiar prompts               | Prioridad: ALTA | Fecha: 2026-07-02
      Repasar estructura
[ ] #  4 | Leer libro                     | Prioridad: BAJA | Fecha: 2026-07-10
[ ] #  2 | Hacer ejercicio                | Prioridad: MEDIA | Fecha: sin fecha
```

### Búsqueda y edición

```powershell
$ python todo.py search "libro"
[ ] #4 | Leer libro | pendiente

$ python todo.py edit 2 --due 2026-07-05
Tarea #2 actualizada.
```

---

## Prompt 4 - UX profesional, colores, exportación CSV y documentación

### Estadísticas

```powershell
$ python todo.py done 1
Tarea #1 marcada como completada.

$ python todo.py stats
Total de tareas: 4
Completadas: 1
Pendientes: 3
Vencidas: 1
Progreso: 25.0%
```

### Exportación a CSV

```powershell
$ python todo.py export tareas.csv
Exportadas 4 tareas a tareas.csv

$ Get-Content tareas.csv -Encoding UTF8
id,titulo,descripcion,prioridad,fecha_limite,estado,creada
1,Estudiar prompts,Repasar estructura,alta,2026-07-02,completada,2026-07-02T22:56:51
2,Hacer ejercicio,,media,2026-07-05,pendiente,2026-07-02T22:56:51
3,Pagar servicios,,alta,2026-07-01,pendiente,2026-07-02T22:56:51
4,Leer libro,,baja,2026-07-10,pendiente,2026-07-02T22:56:51
```

### Colores en terminal

Si se instala `colorama` (`pip install -r requirements.txt`), las prioridades se muestran con colores semánticos:

- **Alta:** rojo
- **Media:** amarillo
- **Baja:** verde
- **Fechas vencidas:** rojo (solo para tareas pendientes)

Sin `colorama`, el programa funciona exactamente igual en texto plano.


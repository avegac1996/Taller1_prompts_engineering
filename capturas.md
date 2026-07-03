# Capturas de verificación - Taller 1

A continuación se muestran las pruebas realizadas en la terminal para cada uno de los prompts. Los datos se guardan en `%USERPROFILE%\.todo_cli\tasks.json`.

---

## Prompt 1 - Estructura base: add, list, done, delete

```powershell
$ python todo.py add "Comprar leche"
Tarea agregada: #1 - Comprar leche

$ python todo.py add "Llamar al banco"
Tarea agregada: #2 - Llamar al banco

$ python todo.py list
[ ] #  1 | Comprar leche                  | Prioridad: MEDIA | Fecha: sin fecha
[ ] #  2 | Llamar al banco                | Prioridad: MEDIA | Fecha: sin fecha

$ python todo.py done 1
Tarea #1 marcada como completada.

$ python todo.py list
[x] #  1 | Comprar leche                  | Prioridad: MEDIA | Fecha: sin fecha
[ ] #  2 | Llamar al banco                | Prioridad: MEDIA | Fecha: sin fecha

$ python todo.py delete 2
Tarea #2 eliminada.

$ python todo.py list
[x] #  1 | Comprar leche                  | Prioridad: MEDIA | Fecha: sin fecha
```

---

## Prompt 2 - Edición, búsqueda, prioridades y fechas límite

```powershell
$ python todo.py add "Proyecto IA" -p alta --due 2026-07-10
Tarea agregada: #1 - Proyecto IA

$ python todo.py add "Leer libro" -d "Capítulo 3" -p baja
Tarea agregada: #2 - Leer libro

$ python todo.py list
[ ] #  1 | Proyecto IA                    | Prioridad: ALTA | Fecha: 2026-07-10
[ ] #  2 | Leer libro                     | Prioridad: BAJA | Fecha: sin fecha
      Capítulo 3

$ python todo.py edit 1 --due 2026-07-08
Tarea #1 actualizada.

$ python todo.py search "libro"
[ ] #2 | Leer libro | pendiente

$ python todo.py list --priority alta
[ ] #  1 | Proyecto IA                    | Prioridad: ALTA | Fecha: 2026-07-08
```

---

## Prompt 3 - Estadísticas, exportación a CSV y colores opcionales

```powershell
$ python todo.py stats
Total de tareas: 2
Completadas: 0
Pendientes: 2
Progreso: 0.0%

$ python todo.py export tareas.csv
Exportadas 2 tareas a tareas.csv

$ Get-Content tareas.csv -Encoding UTF8
id,titulo,descripcion,prioridad,fecha_limite,estado,creada
1,Proyecto IA,,alta,2026-07-08,pendiente,2026-07-02T22:41:32
2,Leer libro,Capítulo 3,baja,,pendiente,2026-07-02T22:41:32
```

> Nota: Si se instala `colorama` (`pip install colorama`), los nombres de prioridad se muestran en colores: alta en rojo, media en amarillo y baja en verde.

---

## Ayuda general del programa

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


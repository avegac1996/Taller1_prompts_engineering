# Prompts utilizados para construir la aplicación

A continuación se muestran los tres prompts estructurados que se usaron para generar el programa paso a paso. Cada prompt sigue la guía: **Rol**, **Contexto**, **Tarea**, **Restricciones** y **Formato**.

---

## Prompt 1 - Estructura base y persistencia

```text
[1. Rol]
Actúa como un desarrollador Python senior especializado en aplicaciones de línea de comandos.

[2. Contexto]
Estoy construyendo una lista de tareas (Todo List) que se ejecuta únicamente desde la terminal en Python 3.

[3. Tarea]
Necesito la estructura base del programa: un script de Python que permita agregar, listar, marcar como completada y eliminar tareas. Las tareas deben guardarse en un archivo JSON para que persistan entre ejecuciones.

[4. Restricciones]
- Usa únicamente la biblioteca estándar de Python.
- El parser de comandos debe ser argparse.
- Los datos deben almacenarse en un archivo JSON dentro del directorio personal del usuario.
- Incluye manejo de errores básico (por ejemplo, ID no encontrado).
- El código debe estar bien comentado.

[5. Formato]
Devuélveme únicamente el bloque de código Python completo y bien comentado, sin explicaciones adicionales.
```

### Resultado esperado

Archivo base `todo.py` con subcomandos `add`, `list`, `done`, `delete` y almacenamiento JSON en `%USERPROFILE%\.todo_cli\tasks.json`.

---

## Prompt 2 - Funciones adicionales: edición, búsqueda, prioridades y fechas

```text
[1. Rol]
Actúa como un desarrollador Python senior especializado en aplicaciones de línea de comandos.

[2. Contexto]
Ya tengo el script base de una lista de tareas en Python con subcomandos add, list, done, delete y persistencia en JSON.

[3. Tarea]
Extiende el script agregando las siguientes funcionalidades:
- Comando edit para modificar título, descripción, prioridad o fecha límite de una tarea por ID.
- Comando search para buscar tareas por palabra clave en título o descripción.
- Campo de prioridad (baja, media, alta) y fecha límite (AAAA-MM-DD) al crear y editar tareas.
- Filtros en list para mostrar tareas pendientes, completadas o por prioridad, y ordenar por prioridad o fecha.

[4. Restricciones]
- Usa argparse subcomandos para cada operación.
- Valida que la fecha sea AAAA-MM-DD.
- Valida que la prioridad sea baja, media o alta.
- Muestra mensajes claros de error cuando el ID no existe.
- El código debe seguir comentado y bien estructurado.

[5. Formato]
Devuélveme el script completo actualizado, como un único bloque de código, sin introducciones.
```

### Resultado esperado

Ampliación del archivo `todo.py` con subcomandos `edit`, `search`, filtros `--status`, `--priority`, `--sort`, y metadatos `prioridad` y `fecha_limite`.

---

## Prompt 3 - Mejora de la experiencia: colores, estadísticas y exportación

```text
[1. Rol]
Actúa como un desarrollador Python senior especializado en aplicaciones de línea de comandos.

[2. Contexto]
Tengo un script de lista de tareas en Python con add, list, done, delete, edit, search, prioridades y fechas límite.

[3. Tarea]
Mejora la experiencia del usuario añadiendo:
- Colores en la terminal para distinguir prioridades (usa colorama si está disponible, pero que el programa siga funcionando si no está instalado).
- Comando stats que muestre el total de tareas, completadas, pendientes y porcentaje de progreso.
- Comando export que escriba todas las tareas a un archivo CSV.

[4. Restricciones]
- No uses dependencias obligatorias; colorama debe ser opcional.
- El archivo CSV debe usar codificación UTF-8 y encabezados.
- La salida de list debe seguir siendo legible y alineada.
- El archivo JSON de persistencia debe seguir en el directorio personal del usuario.
- Entrega el código completo, comentado y listo para ejecutar.

[5. Formato]
Devuélveme únicamente el bloque de código Python final y bien comentado, sin explicaciones previas.
```

### Resultado esperado

Versión final de `todo.py` con soporte de colores opcionales, `stats` y `export`, conservando todas las funcionalidades anteriores.


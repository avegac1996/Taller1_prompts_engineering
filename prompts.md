# Prompts utilizados para construir la aplicación

A continuación se presentan los prompts estructurados que se usaron para generar la aplicación profesional de Lista de Tareas. Cada prompt sigue la guía de **El buen prompt** ampliada con secciones de **QA** y **UX** para garantizar un entregable robusto, ordenado y fácil de usar.

---

## Prompt 1 - Arquitectura, dominio, persistencia y pruebas

```text
[1. Rol]
Actúa como Ingeniero de Software Senior especializado en Python, aplicaciones CLI y desarrollo guiado por pruebas (TDD).

[2. Contexto]
Estoy desarrollando una aplicación de Lista de Tareas (Todo List) que se ejecuta exclusivamente desde la terminal, para una entrega universitaria de Prompt Engineering. El entorno objetivo es Python 3.14 en Windows. El proyecto debe ser mantenible, testable y listo para subir a GitHub.

[3. Tarea]
Diseña la capa de dominio y persistencia de la aplicación en un archivo llamado todo.py:
- Crea una clase TaskManager que gestione las tareas en un archivo JSON ubicado en el directorio personal del usuario.
- Implementa los métodos: add, get, complete, delete, edit, list, search, stats y export_csv.
- Define validaciones para prioridad (baja, media, alta) y fecha límite (AAAA-MM-DD).
- Maneja JSON corrupto sin detener la aplicación.
- Crea la carpeta tests/ con pruebas unitarias usando unittest y archivos temporales, cubriendo: CRUD, validaciones, persistencia y búsqueda.

[4. Restricciones]
- Usa únicamente la biblioteca estándar de Python en la lógica de negocio.
- Separa responsabilidades: la clase TaskManager no debe depender de argparse ni de la interfaz de usuario.
- Los IDs deben ser únicos, secuenciales y persistentes.
- El código debe estar comentado y seguir buenas prácticas de nombres y estructura.

[5. Criterios de aceptación QA]
- Las 23+ pruebas unitarias deben ejecutarse con `python -m unittest discover tests` y pasar todas.
- Si el archivo JSON está corrupto, la aplicación debe recuperarse devolviendo una lista vacía.
- La validación de prioridad y fecha debe lanzar ValueError con mensajes claros.

[6. Consideraciones UX]
- Los mensajes de error deben dirigirse a stderr y usar códigos de salida distintos de cero.
- Las operaciones exitosas deben mostrar confirmaciones concisas.

[7. Formato]
Devuélveme el archivo todo.py completo y comentado, junto con el contenido de tests/test_todo.py, en bloques de código separados y sin explicaciones adicionales.
```

### Resultado esperado

- Clase `TaskManager` con persistencia JSON en `%USERPROFILE%\.todo_cli\tasks.json`.
- Métodos de negocio: add, get, complete, delete, edit, list, search, stats, export_csv.
- Validaciones de prioridad y fecha.
- Suite de pruebas `tests/test_todo.py` con cobertura de CRUD, validaciones y persistencia.

---

## Prompt 2 - Interfaz de línea de comandos (CLI)

```text
[1. Rol]
Actúa como Ingeniero de Software Senior especializado en Python y CLI tools.

[2. Contexto]
Ya tengo la clase TaskManager del Prompt 1 con persistencia JSON, validaciones y pruebas unitarias. Ahora necesito exponer la funcionalidad al usuario mediante una interfaz de terminal profesional.

[3. Tarea]
Construye la interfaz CLI de la aplicación en todo.py:
- Usa argparse con subcomandos: add, list, done, delete, edit, search, stats y export.
- Cada subcomando debe invocar los métodos de TaskManager y mostrar resultados claros.
- Maneja errores de validación (prioridad o fecha inválida) y errores de negocio (ID no encontrado) con mensajes en stderr y salida 1.
- Asegura que el programa se pueda ejecutar con `python todo.py --help` y que la ayuda sea legible.

[4. Restricciones]
- Mantén la clase TaskManager separada de la CLI; no mezcles lógica de argumentos con lógica de negocio.
- No agregues dependencias externas para la CLI.
- Usa nombres de argumentos consistentes y descripciones en español.

[5. Criterios de aceptación QA]
- `python todo.py --help` muestra todos los subcomandos y sus opciones.
- `python todo.py done 999` devuelve un mensaje de error y código de salida 1.
- `python todo.py add "Tarea" --priority invalida` devuelve error de validación.
- La ejecución manual de los comandos principales debe ser exitosa.

[6. Consideraciones UX]
- La ayuda debe estar en español y ser concisa.
- Las operaciones exitosas deben confirmar la acción con el ID y título de la tarea.
- Los errores deben indicar exactamente qué salió mal y cómo corregirlo.

[7. Formato]
Devuélveme el archivo todo.py completo y actualizado, con la CLI integrada y comentada, sin explicaciones adicionales.
```

### Resultado esperado

- `todo.py` con clase `TaskManager` + funciones `cmd_*` y `main()` basada en `argparse`.
- Subcomandos: `add`, `list`, `done`, `delete`, `edit`, `search`, `stats`, `export`.
- Manejo de errores con `stderr` y códigos de salida.

---

## Prompt 3 - Funcionalidades avanzadas, filtros y control de calidad

```text
[1. Rol]
Actúa como Ingeniero de Software Senior y QA Lead en Python CLI.

[2. Contexto]
La aplicación ya tiene capa de dominio y CLI básica. Necesito agregar funcionalidades avanzadas que permitan al usuario gestionar y consultar tareas de forma flexible, sin perder robustez ni testabilidad.

[3. Tarea]
Extiende todo.py y tests/test_todo.py con:
- Campos prioridad (baja, media, alta) y fecha límite (AAAA-MM-DD) en add y edit.
- Filtros en list: todas, pendientes, completadas, hoy (fecha límite igual a hoy), vencidas (fecha límite pasada y no completada).
- Ordenamiento en list: por fecha de creación, prioridad o fecha límite.
- Búsqueda case-insensitive por palabra clave en título o descripción.
- Detección de tareas vencidas y conteo en stats.
- Tests unitarios adicionales para cada filtro, ordenamiento y detección de vencidas.

[4. Restricciones]
- Usa argparse choices para restringir los valores válidos de prioridad y filtros.
- La fecha límite se almacena como string ISO AAAA-MM-DD.
- La lógica de filtros debe estar en TaskManager, no en la CLI.
- No alteres el formato JSON existente; los nuevos campos son opcionales.

[5. Criterios de aceptación QA]
- `python todo.py list --status vencidas` muestra solo tareas pendientes con fecha límite anterior a hoy.
- `python todo.py list --priority alta` muestra solo tareas de alta prioridad.
- `python todo.py list --sort fecha` ordena por fecha límite.
- `python todo.py stats` muestra el total, completadas, pendientes, vencidas y progreso.
- La suite de tests unitarios cubre al menos 20 casos y todos pasan.

[6. Consideraciones UX]
- La salida de list debe ser una tabla alineada con columnas: estado, ID, título, prioridad, fecha límite.
- Las fechas vencidas deben resaltarse visualmente cuando estén activas (se implementará con color en el siguiente prompt).
- Los filtros vacíos deben mostrar un mensaje claro: "No hay tareas que coincidan con el filtro."

[7. Formato]
Devuélveme el archivo todo.py completo y actualizado, junto con el archivo tests/test_todo.py completo, en bloques de código separados y sin introducciones.
```

### Resultado esperado

- Filtros `--status` con opciones: `todas`, `pendientes`, `completadas`, `hoy`, `vencidas`.
- Filtros `--priority` y `--sort`.
- Búsqueda case-insensitive.
- Detección de tareas vencidas en `stats` y `list`.
- Suite de pruebas ampliada.

---

## Prompt 4 - UX profesional, colores, exportación CSV y documentación

```text
[1. Rol]
Actúa como Ingeniero de Software Senior con enfoque en UX/UI de terminal y documentación técnica.

[2. Contexto]
La aplicación de Lista de Tareas ya tiene dominio, CLI, filtros y pruebas. El entregable final debe ser profesional, visualmente claro y acompañado de documentación completa para subir a GitHub.

[3. Tarea]
Politea la experiencia de usuario y prepara la entrega:
- Agrega soporte de colores opcional usando colorama. Si colorama no está instalado, la aplicación funciona sin colores.
- Usa colores semánticos: alta (rojo), media (amarillo), baja (verde). Las fechas vencidas de tareas pendientes deben mostrarse en rojo.
- Mejora el formato de list para que sea legible, alineado y no use emojis.
- Implementa el comando export para generar un CSV UTF-8 con encabezados.
- Crea el README.md con instalación, uso, ejemplos de comandos y sección de calidad/tests.
- Crea el requirements.txt con colorama como dependencia opcional.
- Crea el .gitignore para Python y archivos CSV generados.
- Crea el informe.md de entrega con: proveedor/modelo de IA, prompts utilizados, resultado final, enlace a GitHub e instrucciones para push.
- Crea el capturas.md con las pruebas manuales en terminal por cada prompt.

[4. Restricciones]
- colorama es la única dependencia opcional y debe estar en requirements.txt.
- El CSV debe ser legible y usar codificación UTF-8.
- La documentación debe ser clara, profesional y sin explicaciones excesivas.
- No se deben exponer secretos ni credenciales en la documentación.

[5. Criterios de aceptación QA]
- `pip install -r requirements.txt` instala colorama sin errores.
- Con colorama instalado, `python todo.py list` muestra prioridades en colores.
- Sin colorama, el programa funciona exactamente igual.
- `python todo.py export tareas.csv` genera un archivo CSV correcto.
- El README e informe contienen toda la información requerida por la rubrícula.

[6. Consideraciones UX]
- La salida debe ser amigable en Windows Terminal, CMD y PowerShell.
- Los mensajes de error deben indicar el comando correcto o el formato esperado.
- El README debe incluir ejemplos de comandos copy-pasteables.

[7. Formato]
Devuélveme el contenido completo de los archivos: todo.py, README.md, requirements.txt, .gitignore, informe.md y capturas.md, en bloques de código separados y sin introducciones.
```

### Resultado esperado

- `todo.py` con colores opcionales, formato profesional, export CSV, stats completos.
- `README.md`, `requirements.txt`, `.gitignore`, `informe.md`, `capturas.md`.
- Proyecto listo para ejecutar, probar y subir a GitHub.


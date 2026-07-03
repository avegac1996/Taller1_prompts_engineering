# Informe de entrega - Taller 1: Prompts Engineering

## Datos generales

- **Asignatura:** Taller 1: Prompts Engineering
- **Tema:** Crear una aplicación de Lista de Tareas en Python desde la terminal utilizando prompt engineering.
- **Entrega:** jueves, 2 de julio de 2026

## Proveedor y modelo de IA utilizado

- **Proveedor:** Cascade (asistente de código integrado en el IDE)
- **Modelo de IA:** Modelo de lenguaje OpenAI GPT-4o

## Prompts utilizados

Se utilizaron tres prompts estructurados siguiendo la guía de "El buen prompt": **Rol**, **Contexto**, **Tarea**, **Restricciones** y **Formato**. Los prompts completos están documentados en el archivo `prompts.md` del repositorio.

1. **Prompt 1:** Estructura base de la lista de tareas con persistencia JSON (`add`, `list`, `done`, `delete`).
2. **Prompt 2:** Extensión del programa con `edit`, `search`, prioridades, fechas límite y filtros.
3. **Prompt 3:** Mejora de la experiencia con colores opcionales, `stats` y exportación a CSV.

## Resultado final

La aplicación final es un script de Python ejecutable desde la terminal llamado `todo.py`. Sus funciones principales son:

- `add`: agregar tareas con título, descripción, prioridad y fecha límite.
- `list`: listar tareas con filtros por estado y prioridad, y ordenar por fecha o prioridad.
- `done`: marcar tareas como completadas.
- `delete`: eliminar tareas.
- `edit`: editar tareas existentes.
- `search`: buscar tareas por palabra clave.
- `stats`: ver estadísticas de progreso.
- `export`: exportar las tareas a un archivo CSV.

La persistencia se realiza en un archivo JSON ubicado en el directorio personal del usuario (`%USERPROFILE%\.todo_cli\tasks.json`), por lo que los datos se mantienen entre ejecuciones.

## Repositorio en GitHub

- **Enlace:** [https://github.com/JhossuaVega/taller1_prompts_engineering](https://github.com/JhossuaVega/taller1_prompts_engineering)

> Nota: reemplaza el enlace anterior por el enlace real del repositorio una vez que hayas subido el proyecto a GitHub.

## Capturas de verificación

Las capturas de las pruebas en terminal se incluyen en el archivo `capturas.md` o en la carpeta `capturas/` del repositorio.


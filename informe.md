# Informe de entrega - Taller 1: Prompts Engineering

## Datos generales

- **Asignatura:** Taller 1: Prompts Engineering
- **Tema:** Crear una aplicación de Lista de Tareas en Python desde la terminal utilizando prompt engineering.
- **Nombre del estudiante:** Jhossua Vega

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

## Estado del repositorio local

El repositorio Git ya está inicializado en:

```text
C:\Users\JhossuaVega\Downloads\taller_ia
```

El historial de commits incluye los archivos principales del proyecto y las capturas de verificación.

## Instrucciones para subir a GitHub

1. Crea un repositorio nuevo en GitHub llamado `taller1_prompts_engineering` (sin inicializarlo con README).
2. Ejecuta en la terminal dentro de la carpeta del proyecto:

```powershell
git remote add origin https://github.com/TU_USUARIO/taller1_prompts_engineering.git
git branch -M main
git push -u origin main
```

3. Inicia sesión en GitHub cuando se te solicite y actualiza el enlace de este informe.

## Capturas de verificación

Las capturas de las pruebas en terminal se incluyen en el archivo `capturas.md` del repositorio.


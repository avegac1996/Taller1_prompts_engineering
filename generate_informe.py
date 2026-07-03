"""Genera el informe completo en Word (.docx) a partir de los archivos del proyecto."""

import subprocess
from pathlib import Path

PROJECT = Path(__file__).parent
MD_OUTPUT = PROJECT / "informe_completo.md"
DOCX_OUTPUT = PROJECT / "Informe_Taller1_PromptsEngineering.docx"


def read_file(path: Path) -> str:
    if not path.exists():
        return f"*Archivo {path.name} no encontrado.*"
    return path.read_text(encoding="utf-8")


def add(lines, text=""):
    lines.append(text)


def add_heading(lines, text, level=1):
    add(lines, f"{'#' * level} {text}")
    add(lines, "")


def add_para(lines, text):
    add(lines, text)
    add(lines, "")


def add_code(lines, text, lang=""):
    # Usa 4 backticks para evitar conflictos con triple backticks internos.
    add(lines, f"````{lang}")
    add(lines, text)
    add(lines, "````")
    add(lines, "")


def main():
    lines = []

    add_heading(lines, "Informe de entrega - Taller 1: Prompts Engineering", level=1)

    add_heading(lines, "1. Datos generales", level=2)
    add_para(lines, "- **Asignatura:** Taller 1: Prompts Engineering")
    add_para(lines, "- **Tema:** Crear una aplicación de Lista de Tareas en Python desde la terminal utilizando prompt engineering.")
    add_para(lines, "- **Nombre del estudiante:** Jhossua Vega")
    add_para(lines, "- **Fecha de entrega:** jueves, 2 de julio de 2026")

    add_heading(lines, "2. Proveedor y modelo de IA", level=2)
    add_para(lines, "- **Proveedor:** Cascade (asistente de código integrado en el IDE)")
    add_para(lines, "- **Modelo de IA:** OpenAI GPT-4o")

    add_heading(lines, "3. Repositorio en GitHub", level=2)
    add_para(lines, "URL: https://github.com/avegac1996/Taller1_prompts_engineering.git")

    add_heading(lines, "4. Prompts utilizados", level=2)
    add_para(lines, "Se diseñaron cuatro prompts estructurados con enfoque de QA y UX. El detalle completo se presenta a continuación.")
    add(lines, read_file(PROJECT / "prompts.md"))
    add(lines, "")

    add_heading(lines, "5. Resultado final", level=2)
    add_para(lines, "La aplicación entregada es una Lista de Tareas profesional que se ejecuta completamente desde la terminal. Incluye capa de dominio (clase `TaskManager`), interfaz CLI con `argparse`, validaciones, filtros, estadísticas, exportación CSV y una suite de pruebas unitarias.")

    add_heading(lines, "5.1. Código fuente - todo.py", level=3)
    add_para(lines, "El siguiente listado muestra el archivo principal de la aplicación:")
    add_code(lines, read_file(PROJECT / "todo.py"), lang="python")

    add_heading(lines, "5.2. Pruebas unitarias - tests/test_todo.py", level=3)
    add_para(lines, "Se implementó una suite de 23 pruebas unitarias que cubren validaciones, CRUD, búsqueda, filtros, ordenamiento, detección de tareas vencidas, exportación CSV y persistencia.")
    add_code(lines, read_file(PROJECT / "tests" / "test_todo.py"), lang="python")

    add_heading(lines, "6. Evidencia de ejecución", level=2)
    add_para(lines, "A continuación se incluyen las capturas de las pruebas manuales realizadas en la terminal.")
    add(lines, read_file(PROJECT / "capturas.md"))
    add(lines, "")

    add_heading(lines, "7. Documentación del proyecto", level=2)

    add_heading(lines, "7.1. README.md", level=3)
    add(lines, read_file(PROJECT / "README.md"))
    add(lines, "")

    add_heading(lines, "7.2. requirements.txt", level=3)
    add_code(lines, read_file(PROJECT / "requirements.txt"), lang="text")

    add_heading(lines, "7.3. .gitignore", level=3)
    add_code(lines, read_file(PROJECT / ".gitignore"), lang="text")

    add_heading(lines, "8. Plan de calidad y conclusiones", level=2)
    add_para(lines, "1. **Arquitectura:** La lógica de negocio está separada de la interfaz CLI mediante la clase `TaskManager`, facilitando las pruebas y el mantenimiento.")
    add_para(lines, "2. **Persistencia:** Las tareas se almacenan en un archivo JSON en el directorio personal del usuario (`%USERPROFILE%\\.todo_cli\\tasks.json`). El sistema se recupera automáticamente ante archivos corruptos.")
    add_para(lines, "3. **Validación:** Se validan prioridades (`baja`, `media`, `alta`) y fechas en formato ISO (`AAAA-MM-DD`). Los errores se reportan por `stderr` con códigos de salida distintos de cero.")
    add_para(lines, "4. **Pruebas:** 23 pruebas unitarias se ejecutan exitosamente con `python -m unittest discover tests`.")
    add_para(lines, "5. **UX:** Colores semánticos opcionales, tabla alineada, fechas vencidas resaltadas y mensajes de error informativos.")
    add_para(lines, "6. **Entrega:** El proyecto se encuentra en GitHub y es ejecutable en Python 3.14 desde la terminal.")

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    subprocess.run(
        [
            "pandoc",
            str(MD_OUTPUT),
            "-o",
            str(DOCX_OUTPUT),
            "--from=markdown",
            "--to=docx",
            "--toc",
            "--toc-depth=2",
        ],
        check=True,
    )

    print(f"Documento generado: {DOCX_OUTPUT}")
    print(f"Markdown intermedio: {MD_OUTPUT}")


if __name__ == "__main__":
    main()

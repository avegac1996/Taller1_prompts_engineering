"""Lista de Tareas - Aplicación de línea de comandos en Python."""

import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

# Intenta importar colorama para colores multiplataforma; si no está
# disponible, la aplicación sigue funcionando sin colores.
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except Exception:  # pragma: no cover
    HAS_COLOR = False

    class _DummyColor:
        def __getattr__(self, name):
            return ""

    Fore = _DummyColor()
    Style = _DummyColor()

# Ubicación de la base de datos JSON en el directorio personal del usuario.
DATA_DIR = Path.home() / ".todo_cli"
DATA_FILE = DATA_DIR / "tasks.json"

ESTADO_PENDIENTE = "pendiente"
ESTADO_COMPLETADA = "completada"

# Mapas para trabajar con prioridades de forma ordenada.
PRIORIDADES = {"baja": 1, "media": 2, "alta": 3}
NOMBRE_PRIORIDAD = {1: "baja", 2: "media", 3: "alta"}


def _color_prioridad(prioridad):
    """Devuelve el nombre de la prioridad con color si es posible."""
    nombre = NOMBRE_PRIORIDAD.get(prioridad, str(prioridad)).upper()
    if not HAS_COLOR:
        return nombre
    colores = {
        "alta": Fore.RED,
        "media": Fore.YELLOW,
        "baja": Fore.GREEN,
    }
    return f"{colores.get(nombre.lower(), '')}{nombre}{Style.RESET_ALL}"


def _asegurar_datos():
    """Crea el directorio y archivo JSON si no existen."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def _cargar_tareas():
    """Carga las tareas desde el archivo JSON."""
    _asegurar_datos()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error al leer el archivo de datos: {exc}", file=sys.stderr)
        return []


def _guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON."""
    _asegurar_datos()
    DATA_FILE.write_text(
        json.dumps(tareas, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _nuevo_id(tareas):
    """Calcula el siguiente identificador numérico."""
    return max((tarea["id"] for tarea in tareas), default=0) + 1


def _validar_prioridad(valor):
    """Convierte texto a número de prioridad."""
    if valor is None:
        return None
    valor = valor.lower().strip()
    if valor in PRIORIDADES:
        return PRIORIDADES[valor]
    raise ValueError(f"Prioridad inválida: {valor}. Opciones: baja, media, alta.")


def _validar_fecha(valor):
    """Valida que la fecha tenga formato YYYY-MM-DD."""
    if valor is None:
        return None
    try:
        datetime.datetime.strptime(valor, "%Y-%m-%d")
        return valor
    except ValueError as exc:
        raise ValueError(f"Fecha inválida: {valor}. Use AAAA-MM-DD.") from exc


def cmd_add(args):
    """Agrega una nueva tarea a la lista."""
    tareas = _cargar_tareas()
    tarea = {
        "id": _nuevo_id(tareas),
        "titulo": args.title,
        "descripcion": args.description or "",
        "prioridad": _validar_prioridad(args.priority) or PRIORIDADES["media"],
        "fecha_limite": _validar_fecha(args.due),
        "estado": ESTADO_PENDIENTE,
        "creada": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    tareas.append(tarea)
    _guardar_tareas(tareas)
    print(f"Tarea agregada: #{tarea['id']} - {tarea['titulo']}")


def cmd_list(args):
    """Muestra las tareas con filtros y ordenamiento opcionales."""
    tareas = _cargar_tareas()
    if not tareas:
        print("No hay tareas registradas.")
        return

    filtradas = tareas
    if args.status == "pendientes":
        filtradas = [t for t in filtradas if t["estado"] == ESTADO_PENDIENTE]
    elif args.status == "completadas":
        filtradas = [t for t in filtradas if t["estado"] == ESTADO_COMPLETADA]

    if args.priority:
        prioridad = _validar_prioridad(args.priority)
        filtradas = [t for t in filtradas if t["prioridad"] == prioridad]

    criterio = args.sort or "creada"
    if criterio == "prioridad":
        filtradas = sorted(filtradas, key=lambda t: t["prioridad"], reverse=True)
    elif criterio == "fecha":
        filtradas = sorted(filtradas, key=lambda t: t["fecha_limite"] or "")
    else:
        filtradas = sorted(filtradas, key=lambda t: t["id"])

    if not filtradas:
        print("No hay tareas que coincidan con el filtro.")
        return

    for t in filtradas:
        marcador = "x" if t["estado"] == ESTADO_COMPLETADA else " "
        fecha = t["fecha_limite"] or "sin fecha"
        prioridad = _color_prioridad(t["prioridad"])
        print(
            f"[{marcador}] #{t['id']:>3} | {t['titulo']:<30} "
            f"| Prioridad: {prioridad:<8} | Fecha: {fecha}"
        )
        if t["descripcion"]:
            print(f"      {t['descripcion']}")


def cmd_done(args):
    """Marca una tarea como completada."""
    tareas = _cargar_tareas()
    for tarea in tareas:
        if tarea["id"] == args.id:
            tarea["estado"] = ESTADO_COMPLETADA
            tarea["completada"] = datetime.datetime.now().isoformat(timespec="seconds")
            _guardar_tareas(tareas)
            print(f"Tarea #{tarea['id']} marcada como completada.")
            return
    print(f"No se encontró la tarea #{args.id}.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    """Elimina una tarea por su ID."""
    tareas = _cargar_tareas()
    nuevas = [t for t in tareas if t["id"] != args.id]
    if len(nuevas) == len(tareas):
        print(f"No se encontró la tarea #{args.id}.", file=sys.stderr)
        sys.exit(1)
    _guardar_tareas(nuevas)
    print(f"Tarea #{args.id} eliminada.")


def cmd_edit(args):
    """Edita los campos de una tarea existente."""
    tareas = _cargar_tareas()
    for tarea in tareas:
        if tarea["id"] == args.id:
            if args.title:
                tarea["titulo"] = args.title
            if args.description is not None:
                tarea["descripcion"] = args.description
            if args.priority:
                tarea["prioridad"] = _validar_prioridad(args.priority)
            if args.due:
                tarea["fecha_limite"] = _validar_fecha(args.due)
            tarea["actualizada"] = datetime.datetime.now().isoformat(timespec="seconds")
            _guardar_tareas(tareas)
            print(f"Tarea #{tarea['id']} actualizada.")
            return
    print(f"No se encontró la tarea #{args.id}.", file=sys.stderr)
    sys.exit(1)


def cmd_search(args):
    """Busca tareas por palabra clave en título o descripción."""
    tareas = _cargar_tareas()
    consulta = args.query.lower()
    encontradas = [
        t
        for t in tareas
        if consulta in t["titulo"].lower() or consulta in t["descripcion"].lower()
    ]
    if not encontradas:
        print("No se encontraron coincidencias.")
        return
    for t in encontradas:
        marcador = "x" if t["estado"] == ESTADO_COMPLETADA else " "
        print(f"[{marcador}] #{t['id']} | {t['titulo']} | {t['estado']}")


def cmd_stats(args):
    """Muestra estadísticas del listado de tareas."""
    tareas = _cargar_tareas()
    total = len(tareas)
    completadas = sum(1 for t in tareas if t["estado"] == ESTADO_COMPLETADA)
    pendientes = total - completadas
    print(f"Total de tareas: {total}")
    print(f"Completadas: {completadas}")
    print(f"Pendientes: {pendientes}")
    if total:
        print(f"Progreso: {completadas / total * 100:.1f}%")


def cmd_export(args):
    """Exporta las tareas a un archivo CSV."""
    tareas = _cargar_tareas()
    if not tareas:
        print("No hay tareas para exportar.")
        return
    ruta = Path(args.path)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(
            ["id", "titulo", "descripcion", "prioridad", "fecha_limite", "estado", "creada"]
        )
        for t in tareas:
            escritor.writerow(
                [
                    t["id"],
                    t["titulo"],
                    t["descripcion"],
                    NOMBRE_PRIORIDAD.get(t["prioridad"], t["prioridad"]),
                    t["fecha_limite"] or "",
                    t["estado"],
                    t["creada"],
                ]
            )
    print(f"Exportadas {len(tareas)} tareas a {ruta}")


def _construir_parser():
    """Construye el parser de argumentos con todos los subcomandos."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Lista de tareas multiplataforma desde la terminal.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Agregar una tarea")
    add.add_argument("title", help="Título de la tarea")
    add.add_argument("-d", "--description", help="Descripción opcional")
    add.add_argument(
        "-p", "--priority", choices=["baja", "media", "alta"], default="media"
    )
    add.add_argument("--due", help="Fecha límite en formato AAAA-MM-DD")
    add.set_defaults(func=cmd_add)

    listar = sub.add_parser("list", help="Listar tareas")
    listar.add_argument(
        "--status", choices=["todas", "pendientes", "completadas"], default="todas"
    )
    listar.add_argument("--priority", choices=["baja", "media", "alta"])
    listar.add_argument(
        "--sort", choices=["creada", "prioridad", "fecha"], default="creada"
    )
    listar.set_defaults(func=cmd_list)

    done = sub.add_parser("done", help="Marcar una tarea como completada")
    done.add_argument("id", type=int, help="ID de la tarea")
    done.set_defaults(func=cmd_done)

    delete = sub.add_parser("delete", help="Eliminar una tarea")
    delete.add_argument("id", type=int, help="ID de la tarea")
    delete.set_defaults(func=cmd_delete)

    edit = sub.add_parser("edit", help="Editar una tarea")
    edit.add_argument("id", type=int, help="ID de la tarea")
    edit.add_argument("-t", "--title", help="Nuevo título")
    edit.add_argument("-d", "--description", help="Nueva descripción")
    edit.add_argument("-p", "--priority", choices=["baja", "media", "alta"])
    edit.add_argument("--due", help="Nueva fecha límite AAAA-MM-DD")
    edit.set_defaults(func=cmd_edit)

    search = sub.add_parser("search", help="Buscar tareas por palabra clave")
    search.add_argument("query", help="Texto a buscar")
    search.set_defaults(func=cmd_search)

    stats = sub.add_parser("stats", help="Ver estadísticas")
    stats.set_defaults(func=cmd_stats)

    export = sub.add_parser("export", help="Exportar tareas a CSV")
    export.add_argument("path", help="Ruta del archivo CSV de salida")
    export.set_defaults(func=cmd_export)

    return parser


def main():
    parser = _construir_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

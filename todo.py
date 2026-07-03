"""Lista de Tareas - Aplicación CLI profesional en Python."""

import argparse
import csv
import datetime
import json
import sys
from pathlib import Path

# Colorama es opcional; si no está instalado la aplicación sigue funcionando.
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    _HAS_COLOR = True
except Exception:  # pragma: no cover
    _HAS_COLOR = False

    class _DummyColor:
        def __getattr__(self, name):
            return ""

    Fore = _DummyColor()
    Style = _DummyColor()

# Ubicación por defecto de la base de datos JSON.
DEFAULT_DATA_DIR = Path.home() / ".todo_cli"
DEFAULT_DATA_FILE = DEFAULT_DATA_DIR / "tasks.json"

ESTADO_PENDIENTE = "pendiente"
ESTADO_COMPLETADA = "completada"

# Mapas de prioridad para ordenar y mostrar.
PRIORIDADES = {"baja": 1, "media": 2, "alta": 3}
NOMBRE_PRIORIDAD = {1: "baja", 2: "media", 3: "alta"}


def parse_priority(value):
    """Convierte un texto de prioridad a su valor numérico."""
    if value is None:
        return None
    value = value.lower().strip()
    if value in PRIORIDADES:
        return PRIORIDADES[value]
    raise ValueError(f"Prioridad inválida: {value}. Opciones: baja, media, alta.")


def parse_date(value):
    """Valida que la fecha tenga formato ISO YYYY-MM-DD."""
    if value is None:
        return None
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError as exc:
        raise ValueError(f"Fecha inválida: {value}. Use AAAA-MM-DD.") from exc


def is_overdue(due_date):
    """Indica si una fecha límite ya pasó y no se completó."""
    if not due_date:
        return False
    today = datetime.date.today().isoformat()
    return due_date < today


def _priority_color(priority):
    """Devuelve el nombre de la prioridad con color semántico."""
    name = NOMBRE_PRIORIDAD.get(priority, str(priority)).upper()
    if not _HAS_COLOR:
        return name
    colors = {"alta": Fore.RED, "media": Fore.YELLOW, "baja": Fore.GREEN}
    return f"{colors.get(name.lower(), '')}{name}{Style.RESET_ALL}"


def _due_color(due_date, status):
    """Devuelve la fecha límite, resaltada en rojo si está vencida."""
    if not due_date:
        return "sin fecha"
    if _HAS_COLOR and status == ESTADO_PENDIENTE and is_overdue(due_date):
        return f"{Fore.RED}{due_date}{Style.RESET_ALL}"
    return due_date


class TaskManager:
    """Gestiona la persistencia y operaciones de la lista de tareas."""

    def __init__(self, data_file=None):
        self.data_file = Path(data_file) if data_file else DEFAULT_DATA_FILE
        self.data_dir = self.data_file.parent
        self._ensure_storage()

    def _ensure_storage(self):
        """Crea el directorio y archivo JSON si no existen."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self.data_file.write_text("[]", encoding="utf-8")

    def load(self):
        """Carga las tareas desde el archivo JSON."""
        self._ensure_storage()
        try:
            return json.loads(self.data_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Error al leer el archivo de datos: {exc}", file=sys.stderr)
            return []

    def save(self, tasks):
        """Guarda las tareas en el archivo JSON."""
        self._ensure_storage()
        self.data_file.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    @staticmethod
    def _next_id(tasks):
        """Calcula el siguiente identificador numérico."""
        return max((t["id"] for t in tasks), default=0) + 1

    def add(self, title, description=None, priority="media", due_date=None):
        """Agrega una nueva tarea y devuelve su representación."""
        tasks = self.load()
        task = {
            "id": self._next_id(tasks),
            "titulo": title,
            "descripcion": description or "",
            "prioridad": parse_priority(priority) or PRIORIDADES["media"],
            "fecha_limite": parse_date(due_date),
            "estado": ESTADO_PENDIENTE,
            "creada": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        tasks.append(task)
        self.save(tasks)
        return task

    def list(self, status=None, priority=None, sort_by="creada"):
        """Devuelve las tareas filtradas y ordenadas."""
        tasks = self.load()

        if status and status != "todas":
            if status == "pendientes":
                tasks = [t for t in tasks if t["estado"] == ESTADO_PENDIENTE]
            elif status == "completadas":
                tasks = [t for t in tasks if t["estado"] == ESTADO_COMPLETADA]
            elif status == "hoy":
                today = datetime.date.today().isoformat()
                tasks = [t for t in tasks if t["fecha_limite"] == today]
            elif status == "vencidas":
                tasks = [
                    t
                    for t in tasks
                    if t["estado"] == ESTADO_PENDIENTE and is_overdue(t["fecha_limite"])
                ]

        if priority:
            p = parse_priority(priority)
            tasks = [t for t in tasks if t["prioridad"] == p]

        if sort_by == "prioridad":
            tasks = sorted(tasks, key=lambda t: t["prioridad"], reverse=True)
        elif sort_by == "fecha":
            tasks = sorted(tasks, key=lambda t: t["fecha_limite"] or "")
        else:
            tasks = sorted(tasks, key=lambda t: t["id"])

        return tasks

    def get(self, task_id):
        """Busca una tarea por ID."""
        for t in self.load():
            if t["id"] == task_id:
                return t
        return None

    def complete(self, task_id):
        """Marca una tarea como completada. Devuelve True si existía."""
        tasks = self.load()
        for t in tasks:
            if t["id"] == task_id:
                t["estado"] = ESTADO_COMPLETADA
                t["completada"] = datetime.datetime.now().isoformat(timespec="seconds")
                self.save(tasks)
                return True
        return False

    def delete(self, task_id):
        """Elimina una tarea por ID. Devuelve True si se eliminó."""
        tasks = self.load()
        new_tasks = [t for t in tasks if t["id"] != task_id]
        if len(new_tasks) == len(tasks):
            return False
        self.save(new_tasks)
        return True

    def edit(self, task_id, title=None, description=None, priority=None, due_date=None):
        """Edita una tarea existente. Devuelve True si existía."""
        tasks = self.load()
        for t in tasks:
            if t["id"] == task_id:
                if title:
                    t["titulo"] = title
                if description is not None:
                    t["descripcion"] = description
                if priority:
                    t["prioridad"] = parse_priority(priority)
                if due_date:
                    t["fecha_limite"] = parse_date(due_date)
                t["actualizada"] = datetime.datetime.now().isoformat(timespec="seconds")
                self.save(tasks)
                return True
        return False

    def search(self, query):
        """Busca tareas por palabra clave en título o descripción."""
        q = query.lower()
        return [
            t
            for t in self.load()
            if q in t["titulo"].lower() or q in t["descripcion"].lower()
        ]

    def stats(self):
        """Calcula estadísticas del listado de tareas."""
        tasks = self.load()
        total = len(tasks)
        done = sum(1 for t in tasks if t["estado"] == ESTADO_COMPLETADA)
        pending = total - done
        overdue = sum(
            1
            for t in tasks
            if t["estado"] == ESTADO_PENDIENTE and is_overdue(t["fecha_limite"])
        )
        return {
            "total": total,
            "completadas": done,
            "pendientes": pending,
            "vencidas": overdue,
            "progreso": (done / total * 100) if total else 0.0,
        }

    def export_csv(self, path):
        """Exporta las tareas a un archivo CSV. Devuelve la cantidad exportada."""
        tasks = self.load()
        if not tasks:
            return 0
        path = Path(path)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["id", "titulo", "descripcion", "prioridad", "fecha_limite", "estado", "creada"]
            )
            for t in tasks:
                writer.writerow(
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
        return len(tasks)


def _get_manager():
    """Devuelve una instancia del gestor con la ruta por defecto."""
    return TaskManager()


def _format_task(task):
    """Formatea una tarea para mostrarla en la terminal."""
    marker = "x" if task["estado"] == ESTADO_COMPLETADA else " "
    due = _due_color(task["fecha_limite"], task["estado"])
    priority = _priority_color(task["prioridad"])
    lines = [
        f"[{marker}] #{task['id']:>3} | {task['titulo']:<30} "
        f"| Prioridad: {priority:<8} | Fecha: {due}"
    ]
    if task["descripcion"]:
        lines.append(f"      {task['descripcion']}")
    return "\n".join(lines)


def _print_tasks(tasks):
    """Imprime una lista de tareas formateadas."""
    if not tasks:
        print("No hay tareas que coincidan con el filtro.")
        return
    for t in tasks:
        print(_format_task(t))


def _error(message):
    """Imprime un mensaje de error y termina con código de salida 1."""
    print(message, file=sys.stderr)
    sys.exit(1)


def cmd_add(args):
    """Comando: agregar tarea."""
    try:
        task = _get_manager().add(
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due,
        )
        print(f"Tarea agregada: #{task['id']} - {task['titulo']}")
    except ValueError as exc:
        _error(f"Error: {exc}")


def cmd_list(args):
    """Comando: listar tareas."""
    try:
        manager = _get_manager()
        if not manager.list():
            print("No hay tareas registradas.")
            return
        tasks = manager.list(
            status=args.status, priority=args.priority, sort_by=args.sort
        )
        _print_tasks(tasks)
    except ValueError as exc:
        _error(f"Error: {exc}")


def cmd_done(args):
    """Comando: completar tarea."""
    if _get_manager().complete(args.id):
        print(f"Tarea #{args.id} marcada como completada.")
    else:
        _error(f"No se encontró la tarea #{args.id}.")


def cmd_delete(args):
    """Comando: eliminar tarea."""
    if _get_manager().delete(args.id):
        print(f"Tarea #{args.id} eliminada.")
    else:
        _error(f"No se encontró la tarea #{args.id}.")


def cmd_edit(args):
    """Comando: editar tarea."""
    try:
        if _get_manager().edit(
            task_id=args.id,
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due,
        ):
            print(f"Tarea #{args.id} actualizada.")
        else:
            _error(f"No se encontró la tarea #{args.id}.")
    except ValueError as exc:
        _error(f"Error: {exc}")


def cmd_search(args):
    """Comando: buscar tareas."""
    tasks = _get_manager().search(args.query)
    if not tasks:
        print("No se encontraron coincidencias.")
        return
    for t in tasks:
        marker = "x" if t["estado"] == ESTADO_COMPLETADA else " "
        print(f"[{marker}] #{t['id']} | {t['titulo']} | {t['estado']}")


def cmd_stats(args):
    """Comando: estadísticas."""
    stats = _get_manager().stats()
    print(f"Total de tareas: {stats['total']}")
    print(f"Completadas: {stats['completadas']}")
    print(f"Pendientes: {stats['pendientes']}")
    print(f"Vencidas: {stats['vencidas']}")
    if stats["total"]:
        print(f"Progreso: {stats['progreso']:.1f}%")


def cmd_export(args):
    """Comando: exportar a CSV."""
    count = _get_manager().export_csv(args.path)
    if count:
        print(f"Exportadas {count} tareas a {args.path}")
    else:
        print("No hay tareas para exportar.")


def _build_parser():
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
        "--status",
        choices=["todas", "pendientes", "completadas", "hoy", "vencidas"],
        default="todas",
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
    """Punto de entrada de la aplicación."""
    parser = _build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

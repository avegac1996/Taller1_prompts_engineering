"""Pruebas unitarias para la aplicación de lista de tareas."""

import sys
import tempfile
import unittest
from pathlib import Path

# Permite importar el módulo principal del proyecto.
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo import (
    ESTADO_COMPLETADA,
    ESTADO_PENDIENTE,
    PRIORIDADES,
    TaskManager,
    is_overdue,
    parse_date,
    parse_priority,
)


class TestValidaciones(unittest.TestCase):
    """Valida las funciones de parseo de prioridad y fecha."""

    def test_parse_priority_validas(self):
        self.assertEqual(parse_priority("baja"), PRIORIDADES["baja"])
        self.assertEqual(parse_priority("MEDIA"), PRIORIDADES["media"])
        self.assertEqual(parse_priority("  alta "), PRIORIDADES["alta"])

    def test_parse_priority_invalida(self):
        with self.assertRaises(ValueError):
            parse_priority("urgente")

    def test_parse_priority_none(self):
        self.assertIsNone(parse_priority(None))

    def test_parse_date_valida(self):
        self.assertEqual(parse_date("2026-07-05"), "2026-07-05")

    def test_parse_date_invalida(self):
        with self.assertRaises(ValueError):
            parse_date("05-07-2026")

    def test_parse_date_none(self):
        self.assertIsNone(parse_date(None))


class TestFechasVencidas(unittest.TestCase):
    """Valida la detección de tareas vencidas."""

    def test_is_overdue_pasada(self):
        self.assertTrue(is_overdue("2020-01-01"))

    def test_is_overdue_hoy(self):
        from datetime import date

        self.assertFalse(is_overdue(date.today().isoformat()))

    def test_is_overdue_sin_fecha(self):
        self.assertFalse(is_overdue(None))
        self.assertFalse(is_overdue(""))


class TestTaskManager(unittest.TestCase):
    """Prueba el gestor de tareas con un archivo temporal."""

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.tempdir.name) / "tasks.json"
        self.manager = TaskManager(str(self.data_file))

    def tearDown(self):
        self.tempdir.cleanup()

    def test_add_and_list(self):
        t1 = self.manager.add("Tarea 1", priority="alta", due_date="2026-07-10")
        t2 = self.manager.add("Tarea 2", description="desc", priority="baja")
        tasks = self.manager.list()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["id"], t1["id"])
        self.assertEqual(tasks[1]["titulo"], t2["titulo"])

    def test_complete(self):
        task = self.manager.add("Tarea")
        self.assertTrue(self.manager.complete(task["id"]))
        self.assertFalse(self.manager.complete(999))
        completed = self.manager.list(status="completadas")
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["estado"], ESTADO_COMPLETADA)

    def test_delete(self):
        task = self.manager.add("Tarea")
        self.assertTrue(self.manager.delete(task["id"]))
        self.assertFalse(self.manager.delete(task["id"]))
        self.assertEqual(len(self.manager.list()), 0)

    def test_edit(self):
        task = self.manager.add("Tarea")
        self.assertTrue(
            self.manager.edit(
                task["id"], title="Nuevo título", priority="media", due_date="2026-08-01"
            )
        )
        updated = self.manager.get(task["id"])
        self.assertEqual(updated["titulo"], "Nuevo título")
        self.assertEqual(updated["prioridad"], PRIORIDADES["media"])
        self.assertEqual(updated["fecha_limite"], "2026-08-01")

    def test_edit_no_existente(self):
        self.assertFalse(self.manager.edit(999, title="Nuevo"))

    def test_search(self):
        self.manager.add("Comprar leche")
        self.manager.add("Llamar al banco", description="urgente")
        results = self.manager.search("leche")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["titulo"], "Comprar leche")
        results = self.manager.search("banco")
        self.assertEqual(len(results), 1)

    def test_search_case_insensitive(self):
        self.manager.add("Estudiar Python")
        results = self.manager.search("PYTHON")
        self.assertEqual(len(results), 1)

    def test_stats(self):
        self.manager.add("T1")
        t2 = self.manager.add("T2")
        self.manager.complete(t2["id"])
        stats = self.manager.stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["completadas"], 1)
        self.assertEqual(stats["pendientes"], 1)
        self.assertEqual(stats["vencidas"], 0)
        self.assertEqual(stats["progreso"], 50.0)

    def test_stats_vencidas(self):
        self.manager.add("T1", due_date="2020-01-01")
        stats = self.manager.stats()
        self.assertEqual(stats["vencidas"], 1)

    def test_list_filters(self):
        t1 = self.manager.add("T1", priority="alta")
        self.manager.add("T2", priority="baja")
        self.manager.complete(t1["id"])
        self.assertEqual(len(self.manager.list(status="completadas")), 1)
        self.assertEqual(len(self.manager.list(status="pendientes")), 1)
        self.assertEqual(len(self.manager.list(priority="alta")), 1)
        self.assertEqual(len(self.manager.list(priority="baja")), 1)

    def test_list_sort(self):
        self.manager.add("A", priority="baja", due_date="2026-08-01")
        self.manager.add("B", priority="alta", due_date="2026-07-01")
        by_priority = self.manager.list(sort_by="prioridad")
        self.assertEqual(by_priority[0]["prioridad"], PRIORIDADES["alta"])
        by_date = self.manager.list(sort_by="fecha")
        self.assertEqual(by_date[0]["fecha_limite"], "2026-07-01")

    def test_export_csv(self):
        self.manager.add("T1")
        self.manager.add("T2", description="desc")
        export_path = Path(self.tempdir.name) / "out.csv"
        count = self.manager.export_csv(str(export_path))
        self.assertEqual(count, 2)
        self.assertTrue(export_path.exists())
        content = export_path.read_text(encoding="utf-8")
        self.assertIn("id,titulo,descripcion,prioridad,fecha_limite,estado,creada", content)
        self.assertIn("T2", content)

    def test_export_csv_sin_tareas(self):
        export_path = Path(self.tempdir.name) / "empty.csv"
        count = self.manager.export_csv(str(export_path))
        self.assertEqual(count, 0)
        self.assertFalse(export_path.exists())

    def test_data_persistence(self):
        task = self.manager.add("Persistente")
        manager2 = TaskManager(str(self.data_file))
        self.assertIsNotNone(manager2.get(task["id"]))


if __name__ == "__main__":
    unittest.main()

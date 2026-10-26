import unittest

from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "Estudio")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertEqual(tarea["categoria"], "Estudio")
        self.assertFalse(tarea["completada"])

    def test_agregar_tarea_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer documentación", "   ")

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar", "Estudio")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_pendientes_filtra_por_categoria_sin_mayusculas(self):
        tareas = []
        agregar_tarea(tareas, "Practicar Python", "Estudio")
        agregar_tarea(tareas, "Comprar cuaderno", "personal")
        completar_tarea(tareas, 2)

        resultado = pendientes(tareas, "eStUdIo")

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["titulo"], "Practicar Python")

    def test_pendientes_categoria_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "Practicar Python", "Estudio")

        resultado = pendientes(tareas, "inexistente")

        self.assertEqual(resultado, [])

    def test_eliminar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar Python", "Estudio")
        tarea_eliminada = agregar_tarea(tareas, "Comprar cuaderno", "Personal")
        agregar_tarea(tareas, "Hacer ejercicio", "Salud")

        resultado = eliminar_tarea(tareas, 2)

        self.assertEqual(resultado, tarea_eliminada)
        self.assertEqual([t["id"] for t in tareas], [1, 3])


    def test_agregar_tarea_no_duplica_id_despues_de_eliminar(self):
        tareas = []
        agregar_tarea(tareas, "A", "x")
        agregar_tarea(tareas, "B", "x")
        agregar_tarea(tareas, "C", "x")

        eliminar_tarea(tareas, 2)
        nueva_tarea = agregar_tarea(tareas, "D", "x")

        self.assertEqual(nueva_tarea["id"], 4)
        self.assertEqual([t["id"] for t in tareas], [1, 3, 4])

    def test_eliminar_tarea_id_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "Practicar Python", "Estudio")

        with self.assertRaisesRegex(ValueError, "Tarea no encontrada"):
            eliminar_tarea(tareas, 999)


if __name__ == "__main__":
    unittest.main()

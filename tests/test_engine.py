"""Tests del motor de respuestas y de la base de conocimiento."""

from __future__ import annotations

import unittest

from bot.engine import ANSWER_THRESHOLD, ChatBot
from bot.knowledge_base import CATEGORIES, ENTRIES, ENTRIES_BY_ID


class KnowledgeBaseTests(unittest.TestCase):
    def test_catalog_is_consistent(self) -> None:
        self.assertGreaterEqual(len(ENTRIES), 30)
        ids = [entry.id for entry in ENTRIES]
        self.assertEqual(len(ids), len(set(ids)), "Hay ids duplicados")

        for entry in ENTRIES:
            with self.subTest(entry=entry.id):
                self.assertIn(entry.category, CATEGORIES)
                self.assertTrue(entry.title.strip())
                self.assertGreater(len(entry.answer), 100)
                self.assertTrue(entry.tags)
                self.assertTrue(entry.patterns)
                for related_id in entry.related:
                    self.assertIn(related_id, ENTRIES_BY_ID)
                    self.assertNotEqual(related_id, entry.id)

    def test_every_category_has_entries(self) -> None:
        for category in CATEGORIES:
            with self.subTest(category=category):
                self.assertTrue(
                    [entry for entry in ENTRIES if entry.category == category]
                )


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bot = ChatBot()

    def test_representative_questions(self) -> None:
        cases = {
            "¿Cómo hago un diagrama de cuerpo libre?": "dcl",
            "¿Cómo calculo el momento de una fuerza?": "momento",
            "Cómo calculo la resultante de dos fuerzas": "vectores",
            "Qué es el equilibrio de una partícula": "equilibrio-particula",
            "Ecuaciones de equilibrio de un cuerpo rígido": "equilibrio-rigido",
            "Tipos de apoyos y reacciones": "apoyos",
            "Cómo saco el centroide de una figura compuesta": "centroide",
            "Qué es la fricción estática": "friccion",
            "Cómo resuelvo una armadura por nodos": "armaduras",
            "Diagrama de cortante y momento": "cortante",
            "Tensión en poleas": "cables-poleas",
            "Qué unidades se usan en estática": "unidades",
            "Pasos para resolver un problema de estática": "metodo-estatica",
            "Reacciones de una viga simplemente apoyada": "viga-reacciones",
            "Qué es la estática": "que-es-estatica",
            "Diferencia entre masa y peso": "peso-masa",
            "Qué es un string": "tipos-datos",
            "Qué es un tipo de dato": "tipos-datos",
            "Qué es una variable": "variables",
            "Cómo uso if else": "condicionales",
            "Cómo funciona el bucle for": "bucles-for",
            "Cómo funciona el while": "bucles-while",
            "Cómo defino una función": "funciones",
            "Cómo usar listas": "listas",
            "Cómo recorrer un diccionario": "diccionarios",
            "Error index out of range": "errores",
            "Qué es la recursividad": "recursividad",
            "Cómo empiezo con numpy": "numpy",
            "Cómo graficar con matplotlib": "matplotlib",
            "Cómo valido la entrada del usuario": "validacion",
            "Cómo depuro mi código": "debug",
            "Cómo crear una clase": "clases",
            "Cómo formatear decimales": "fstrings",
            "Cómo leer un archivo": "archivos",
            "Sistema de ecuaciones con numpy": "numpy-sistemas",
            "Cómo calculo momentos con Python": "python-estatica",
            "Errores de unidades en el código": "unidades-codigo",
            "Quiero aprender a programar": "como-empezar",
            "Qué es programar": "que-es-programar",
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                reply = self.bot.answer(question)
                self.assertEqual(reply.topic_id, expected, reply.text[:120])

    def test_typo_tolerance(self) -> None:
        self.assertEqual(self.bot.answer("mometo de una fuerza").topic_id, "momento")
        self.assertEqual(self.bot.answer("artmadura metodo de nodos").topic_id, "armaduras")

    def test_related_answers_are_returned(self) -> None:
        reply = self.bot.answer("¿Cómo hago un diagrama de cuerpo libre?")
        self.assertGreater(reply.confidence, ANSWER_THRESHOLD)
        self.assertLessEqual(len(reply.suggestions), 3)
        self.assertTrue(reply.suggestions)
        self.assertNotIn("dcl", [s.question for s in reply.suggestions])

    def test_conversational_intents(self) -> None:
        cases = {
            "hola": "EstáticaBot",
            "buenas tardes": "EstáticaBot",
            "¿Qué puedes hacer?": "Puedo ayudarte con estos bloques",
            "¿Quién eres?": "base de conocimiento",
            "gracias": "De nada",
            "adiós": "Hasta luego",
        }
        for question, fragment in cases.items():
            with self.subTest(question=question):
                reply = self.bot.answer(question)
                self.assertIsNone(reply.topic_id)
                self.assertIn(fragment, reply.text)

    def test_help_does_not_intercept_technical_questions(self) -> None:
        reply = self.bot.answer("¿Cómo funciona una polea?")
        self.assertEqual(reply.topic_id, "cables-poleas")

    def test_greetings_do_not_swallow_technical_questions(self) -> None:
        cases = {
            "hola, ¿cómo calculo el momento de una fuerza?": "momento",
            "gracias, ¿cómo funciona el bucle for?": "bucles-for",
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assertEqual(self.bot.answer(question).topic_id, expected)

    def test_unknown_question_falls_back(self) -> None:
        reply = self.bot.answer("asdkjh qwerty zzz")
        self.assertIsNone(reply.topic_id)
        self.assertIn("No encontré", reply.text)
        self.assertTrue(reply.suggestions)

    def test_empty_question(self) -> None:
        reply = self.bot.answer("   ")
        self.assertIsNone(reply.topic_id)
        self.assertTrue(reply.text)
        self.assertTrue(reply.suggestions)

    def test_catalog_navigation(self) -> None:
        self.assertEqual(len(self.bot.entries_by_category("Todas")), len(ENTRIES))
        static_entries = self.bot.entries_by_category("Estática")
        self.assertTrue(static_entries)
        self.assertTrue(all(e.category == "Estática" for e in static_entries))
        self.assertIsNotNone(self.bot.get_entry("dcl"))
        self.assertIsNone(self.bot.get_entry("no-existe"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

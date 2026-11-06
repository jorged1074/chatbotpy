"""Motor de respuestas del chatbot.

No usa servicios externos ni modelos de lenguaje: busca la pregunta del
usuario en la base de conocimiento con TF-IDF + similitud de coseno, corrige
errores de tipeo comunes y devuelve la mejor coincidencia junto con temas
relacionados.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher

from .knowledge_base import CATEGORIES, ENTRIES, ENTRIES_BY_ID, Entry
from .text_utils import expand_query, normalize, tokenize

# Umbral de similitud para responder directamente. Por debajo se ofrece la
# mejor aproximación con un aviso; muy por debajo se muestra ayuda.
ANSWER_THRESHOLD = 0.22
SUGGEST_THRESHOLD = 0.19


@dataclass(frozen=True)
class Suggestion:
    """Pregunta sugerida que la interfaz muestra como botón."""

    label: str
    question: str


@dataclass(frozen=True)
class Reply:
    """Resultado de procesar una pregunta."""

    text: str
    topic_id: str | None = None
    topic_title: str | None = None
    confidence: float = 0.0
    suggestions: tuple[Suggestion, ...] = ()


def _entry_suggestion(entry: Entry) -> Suggestion:
    return Suggestion(label=entry.title, question=entry.title)


class _Index:
    """Índice TF-IDF sobre títulos, tags y preguntas de ejemplo."""

    def __init__(self, entries: tuple[Entry, ...]) -> None:
        self.entries = entries
        documents: list[list[str]] = []
        for entry in entries:
            parts = [entry.title, entry.title, entry.title]
            parts.extend(entry.tags * 2)
            parts.extend(entry.patterns)
            documents.append(tokenize(" ".join(parts)))

        self.total = len(documents)
        document_frequency: Counter[str] = Counter()
        for document in documents:
            document_frequency.update(set(document))

        self.idf: dict[str, float] = {
            term: math.log((self.total + 1) / (frequency + 1)) + 1
            for term, frequency in document_frequency.items()
        }
        self.default_idf = math.log(self.total + 1) + 1
        self.vectors = [self._weigh(document, only_known=False) for document in documents]

    def _weigh(
        self, tokens: list[str], *, only_known: bool
    ) -> dict[str, float]:
        frequencies = Counter(tokens)
        vector: dict[str, float] = {}
        for term, count in frequencies.items():
            if only_known and term not in self.idf:
                continue
            weight = (1 + math.log(count)) * self.idf.get(term, self.default_idf)
            vector[term] = weight
        norm = math.sqrt(sum(value * value for value in vector.values()))
        if norm == 0:
            return {}
        return {term: value / norm for term, value in vector.items()}

    def similarity(self, query: str) -> list[float]:
        query_tokens = self._correct_tokens(expand_query(query))
        if not query_tokens:
            return [0.0] * self.total
        query_vector = self._weigh(query_tokens, only_known=True)
        if not query_vector:
            return [0.0] * self.total
        return [
            sum(weight * document.get(term, 0.0) for term, weight in query_vector.items())
            for document in self.vectors
        ]

    def _correct_tokens(self, tokens: list[str]) -> list[str]:
        """Corrige typos leves contra el vocabulario del índice."""
        corrected: list[str] = []
        vocabulary = tuple(self.idf)
        for token in tokens:
            if token in self.idf:
                corrected.append(token)
                continue
            if len(token) < 5:
                corrected.append(token)
                continue
            best_term = token
            best_ratio = 0.0
            for candidate in vocabulary:
                ratio = SequenceMatcher(None, token, candidate).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_term = candidate
            if best_ratio >= 0.76:
                corrected.append(best_term)
            else:
                corrected.append(token)
        return corrected


_GREETING_RE = re.compile(
    r"^(hola+|buenas|buenos dias|buenas tardes|buenas noches|hey|"
    r"saludos|que tal|hi|hello)"
    r"(\s+(a todos|a todas|amigos|como estas|como andas|que tal))?$"
)
_HELP_RE = re.compile(
    r"^(ayuda|help|opciones|menu|instrucciones|como funcionas|como funciona)$|"
    r"^(que puedes hacer|que sabes hacer|en que me puedes ayudar|"
    r"que temas tienes|temas disponibles)$"
)
_IDENTITY_RE = re.compile(
    r"^(quien eres|como te llamas|que eres|eres un bot|quien te creo|"
    r"quien te hizo)(\s+(exactamente|tu|y que haces))?$"
)
_THANKS_RE = re.compile(
    r"^((muchas|mil|ok|vale|perfecto|genial) )?gracias"
    r"( por (tu|la) ayuda| por todo)?$|^te agradezco( por (tu|la) ayuda)?$"
)
_BYE_RE = re.compile(
    r"^(adios|chao|hasta luego|hasta pronto|nos vemos|bye|goodbye)"
    r"(\s+(amigo|profe|gracias))?$"
)

_IDENTITY_TEXT = (
    "Soy **EstáticaBot** 🧮, un asistente local especializado en **estática** "
    "(mecánica para ingeniería) y **programación básica en Python**.\n\n"
    "No uso internet ni modelos externos: todas mis respuestas salen de una "
    "base de conocimiento incluida en el proyecto, así que funciona sin "
    "conexión y sin claves de API."
)

_HELP_TEXT = """Puedo ayudarte con estos bloques:

**🧱 Estática**
Diagrama de cuerpo libre, vectores y resultantes, momentos, equilibrio de partículas y cuerpos rígidos, tipos de apoyos, centroides, fricción, armaduras, cortante y flector, cables y poleas, vigas y unidades.

**🐍 Programación en Python**
Variables y tipos, condicionales, `for` y `while`, funciones, listas, diccionarios, errores, recursividad, NumPy, Matplotlib, validación, depuración, clases, f-strings y archivos.

**🔗 Estática ↔ Python**
Resolver sistemas de equilibrio con `numpy.linalg.solve`, calcular resultantes y momentos con un script y evitar errores de unidades.

Escribe tu pregunta con tus propias palabras o elige un tema:"""

_THANKS_TEXT = (
    "¡De nada! 😊 Si quieres, seguimos practicando. Puedes preguntarme por "
    "otro tema o pedirme un ejemplo de código."
)

_BYE_TEXT = (
    "¡Hasta luego! 👋 Recuerda: **DCL primero, ecuaciones después**. "
    "Vuelve cuando quieras seguir practicando estática o Python."
)


class ChatBot:
    """Fachada sencilla para consultar la base de conocimiento."""

    def __init__(self) -> None:
        self.entries: tuple[Entry, ...] = ENTRIES
        self.categories: tuple[str, ...] = CATEGORIES
        self._index = _Index(self.entries)

    # ------------------------------------------------------------------
    # Consultas sobre el catálogo
    # ------------------------------------------------------------------
    def entries_by_category(self, category: str | None = None) -> list[Entry]:
        if category in (None, "", "Todas"):
            return list(self.entries)
        return [entry for entry in self.entries if entry.category == category]

    def get_entry(self, entry_id: str) -> Entry | None:
        return ENTRIES_BY_ID.get(entry_id)

    # ------------------------------------------------------------------
    # Respuesta principal
    # ------------------------------------------------------------------
    def answer(self, question: str) -> Reply:
        cleaned = " ".join(str(question or "").split())
        if not cleaned:
            return Reply(
                text="Escribe una pregunta y haré lo posible por ayudarte. 🙂",
                suggestions=self._starter_suggestions(),
            )

        normalized = normalize(cleaned)
        tokens = normalized.split()

        # Intenciones conversacionales (solo si la frase es corta, para no
        # interceptar preguntas técnicas que contengan estas palabras).
        if _IDENTITY_RE.search(normalized) and len(tokens) <= 8:
            return Reply(
                text=_IDENTITY_TEXT,
                suggestions=self._starter_suggestions(),
            )
        if _HELP_RE.search(normalized) and len(tokens) <= 8:
            return Reply(text=_HELP_TEXT, suggestions=self._starter_suggestions())
        if _THANKS_RE.search(normalized) and len(tokens) <= 5:
            return Reply(
                text=_THANKS_TEXT,
                suggestions=self._starter_suggestions(),
            )
        if _BYE_RE.search(normalized) and len(tokens) <= 5:
            return Reply(text=_BYE_TEXT)
        if _GREETING_RE.search(normalized) and len(tokens) <= 5:
            return Reply(
                text=(
                    "¡Hola! 👋 Soy **EstáticaBot**, tu asistente de **estática** "
                    "y **programación básica en Python**.\n\n"
                    "Puedo explicarte teoría, mostrarte fórmulas y darte ejemplos "
                    "de código. Pregúntame lo que necesites o elige un tema para "
                    "empezar:"
                ),
                suggestions=self._starter_suggestions(),
            )

        # Búsqueda en la base de conocimiento.
        scores = self._index.similarity(cleaned)
        ranking = sorted(
            zip(self.entries, scores, strict=True),
            key=lambda pair: pair[1],
            reverse=True,
        )
        best_entry, best_score = ranking[0]

        if best_score < SUGGEST_THRESHOLD:
            candidates = [entry for entry, score in ranking[:3] if score > 0.01]
            if candidates:
                suggestions = tuple(
                    _entry_suggestion(entry) for entry in candidates
                )
            else:
                suggestions = self._starter_suggestions()
            return Reply(
                text=(
                    "No encontré un tema que coincida con tu pregunta. 😅\n\n"
                    "Puedo ayudarte con **estática** (DCL, momentos, equilibrio, "
                    "armaduras, vigas…) y **programación básica en Python** "
                    "(variables, bucles, funciones, NumPy…).\n\n"
                    "Prueba a reformular la pregunta, escribe **ayuda** o elige "
                    "uno de estos temas:"
                ),
                confidence=best_score,
                suggestions=suggestions,
            )

        suggestions = self._related_suggestions(best_entry)

        if best_score < ANSWER_THRESHOLD:
            intro = (
                f"No estoy del todo seguro de haber entendido. Lo más parecido "
                f"que tengo es **{best_entry.title}**; si no es lo que buscabas, "
                f"reformula la pregunta.\n\n---\n\n"
            )
            return Reply(
                text=intro + best_entry.answer,
                topic_id=best_entry.id,
                topic_title=best_entry.title,
                confidence=best_score,
                suggestions=suggestions,
            )

        return Reply(
            text=best_entry.answer,
            topic_id=best_entry.id,
            topic_title=best_entry.title,
            confidence=best_score,
            suggestions=suggestions,
        )

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    def _starter_suggestions(self) -> tuple[Suggestion, ...]:
        starter_ids = ("dcl", "momento", "bucles-for")
        return tuple(
            _entry_suggestion(ENTRIES_BY_ID[entry_id])
            for entry_id in starter_ids
            if entry_id in ENTRIES_BY_ID
        )

    def _related_suggestions(
        self, entry: Entry, limit: int = 3
    ) -> tuple[Suggestion, ...]:
        suggestions: list[Suggestion] = []
        seen = {entry.id}

        for related_id in entry.related:
            related = ENTRIES_BY_ID.get(related_id)
            if related and related.id not in seen:
                suggestions.append(_entry_suggestion(related))
                seen.add(related.id)
            if len(suggestions) >= limit:
                return tuple(suggestions)

        for candidate in self.entries:
            if len(suggestions) >= limit:
                break
            if candidate.id not in seen and candidate.category == entry.category:
                suggestions.append(_entry_suggestion(candidate))
                seen.add(candidate.id)

        return tuple(suggestions)

"""Utilidades de normalización y tokenización de texto en español.

El motor de búsqueda compara la pregunta del usuario con el contenido de la
base de conocimiento. Para que la coincidencia sea robusta frente a tildes,
mayúsculas, signos de puntuación y plurales, todo el texto pasa por aquí.
"""

from __future__ import annotations

import re

# Sustitución simple de caracteres acentuados (no usamos unicodedata para
# mantener el comportamiento predecible con la ñ y los signos de apertura).
_ACCENTS = str.maketrans(
    "áéíóúüñÁÉÍÓÚÜÑ",
    "aeiouunAEIOUUN",
)

_WORD_RE = re.compile(r"[^a-z0-9ñ\s]+")

# Palabras vacías del español: aportan poco a la búsqueda y generan ruido.
STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "al", "algo", "algun", "alguna", "algunas", "alguno", "algunos",
        "ante", "antes", "aquel", "asi", "cada", "como", "con", "contra",
        "cual", "cuales", "cuando", "de", "del", "desde", "donde", "dos",
        "el", "ella", "ellas", "ello", "ellos", "en", "entre", "era", "es",
        "esa", "esas", "ese", "eso", "esos", "esta", "estas", "este", "esto",
        "estos", "fue", "ha", "hacia", "hasta", "hay", "la", "las", "le",
        "les", "lo", "los", "mas", "me", "mi", "mis", "mucho", "muy", "nada",
        "ni", "no", "nos", "o", "otra", "otro", "para", "pero", "poco", "por",
        "porque", "que", "quien", "quienes", "se", "sea", "ser", "si", "sin",
        "sobre", "son", "su", "sus", "te", "tiene", "todo", "todos", "tu",
        "tus", "un", "una", "unas", "uno", "unos", "y", "ya", "yo",
    }
)

# Expansión de sinónimos frecuentes: la clave es el token normalizado que
# escribe el usuario y el valor se añade como tokens extra a la consulta.
SYNONYMS: dict[str, tuple[str, ...]] = {
    "torque": ("momento",),
    "truss": ("armadura", "cercha"),
    "cercha": ("armadura",),
    "dcl": ("diagrama", "cuerpo", "libre"),
    "rozamiento": ("friccion",),
    "graficar": ("grafico", "matplotlib"),
    "grafica": ("grafico", "matplotlib"),
    "plot": ("grafico", "matplotlib"),
    "codigo": ("programacion", "python"),
    "programa": ("programacion", "python"),
    "programar": ("programacion", "python"),
    "script": ("programacion", "python"),
    "depuro": ("depurar", "debug"),
    "depuras": ("depurar", "debug"),
    "depura": ("depurar", "debug"),
    "depurando": ("depurar", "debug"),
    "depuracion": ("depurar", "debug"),
    "promedio": ("media",),
    "raiz": ("sqrt",),
    "potencia": ("exponente",),
    "cadena": ("string", "texto"),
    "string": ("cadena", "texto"),
    "str": ("cadena", "string"),
    "arreglo": ("array", "lista"),
    "vector": ("vector", "fuerza"),
    "matriz": ("matriz", "numpy"),
    "ecuaciones": ("sistema", "ecuacion"),
    "empotrado": ("empotramiento",),
    "articulacion": ("pasador",),
    "soporte": ("apoyo",),
    "peso": ("gravedad", "masa"),
    "empiezo": ("empezar",),
    "empieza": ("empezar",),
    "empiezan": ("empezar",),
    "comienzo": ("empezar",),
}


def strip_accents(text: str) -> str:
    """Devuelve el texto sin tildes ni diéresis."""
    return text.translate(_ACCENTS)


def normalize(text: str) -> str:
    """Minúsculas, sin acentos, sin signos y con espacios colapsados."""
    text = strip_accents(str(text).lower())
    text = _WORD_RE.sub(" ", text)
    return " ".join(text.split())


def stem(word: str) -> str:
    """Stemming muy ligero para español (plurales y terminaciones comunes).

    No pretende ser lingüísticamente perfecto; solo unir variantes como
    ``fuerza/fuerzas``, ``momento/momentos`` o ``reaccion/reacciones``.
    """
    if len(word) <= 4:
        return word
    if word.endswith("mente") and len(word) > 8:
        return word[:-5]
    if word.endswith("es") and len(word) > 5:
        return word[:-2]
    if word.endswith("s") and len(word) > 4:
        return word[:-1]
    return word


def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """Convierte un texto en tokens normalizados y stemizados."""
    tokens = normalize(text).split()
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return [stem(t) for t in tokens]


def expand_query(text: str) -> list[str]:
    """Tokeniza la consulta y agrega sinónimos conocidos."""
    tokens = tokenize(text)
    expanded = list(tokens)
    for token in tokens:
        for synonym in SYNONYMS.get(token, ()):  # noqa: PLC0206
            for piece in synonym.split():
                expanded.append(stem(piece))
    return expanded

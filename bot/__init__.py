"""EstáticaBot: asistente de estática y programación básica con Streamlit."""

from __future__ import annotations

from .calculators import (
    BeamReactions,
    Resultant,
    beam_reactions_point_load,
    resultant_two_forces,
)
from .engine import ChatBot, Reply, Suggestion
from .knowledge_base import CATEGORIES, ENTRIES, Entry

__all__ = [
    "CATEGORIES",
    "ENTRIES",
    "BeamReactions",
    "ChatBot",
    "Entry",
    "Reply",
    "Resultant",
    "Suggestion",
    "beam_reactions_point_load",
    "resultant_two_forces",
]

__version__ = "1.0.0"

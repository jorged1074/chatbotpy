"""Calculadoras rápidas de estática usadas en la barra lateral."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Resultant:
    r: float
    angle: float
    fx: float
    fy: float


@dataclass(frozen=True)
class BeamReactions:
    ra: float
    rb: float
    total: float


def resultant_two_forces(
    f1: float, angle1: float, f2: float, angle2: float
) -> Resultant:
    """Resultante de dos fuerzas concurrentes.

    Los ángulos se expresan en grados medidos desde el eje x positivo y en
    sentido antihorario. Las fuerzas deben ser no negativas.
    """
    f1, f2 = float(f1), float(f2)
    if f1 < 0 or f2 < 0:
        raise ValueError("Los módulos de las fuerzas no pueden ser negativos.")

    a1 = math.radians(float(angle1))
    a2 = math.radians(float(angle2))
    fx = f1 * math.cos(a1) + f2 * math.cos(a2)
    fy = f1 * math.sin(a1) + f2 * math.sin(a2)
    r = math.hypot(fx, fy)
    angle = math.degrees(math.atan2(fy, fx)) % 360 if r > 1e-12 else 0.0
    return Resultant(r=r, angle=angle, fx=fx, fy=fy)


def beam_reactions_point_load(
    span: float, distance: float, load: float
) -> BeamReactions:
    """Reacciones de una viga simplemente apoyada con carga puntual.

    ``span`` es la luz total (m), ``distance`` la posición de la carga medida
    desde el apoyo A (m) y ``load`` la carga vertical hacia abajo (N).
    """
    span, distance, load = float(span), float(distance), float(load)
    if span <= 0:
        raise ValueError("La luz de la viga debe ser mayor que cero.")
    if not 0 <= distance <= span:
        raise ValueError("La carga debe estar entre los dos apoyos.")
    if load < 0:
        raise ValueError("La carga no puede ser negativa.")

    rb = load * distance / span
    ra = load - rb
    return BeamReactions(ra=ra, rb=rb, total=load)

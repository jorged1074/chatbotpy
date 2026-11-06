"""Tests de las calculadoras de estática."""

from __future__ import annotations

import math
import unittest

from bot.calculators import beam_reactions_point_load, resultant_two_forces


class ResultantTests(unittest.TestCase):
    def test_perpendicular_forces(self) -> None:
        result = resultant_two_forces(3, 0, 4, 90)
        self.assertAlmostEqual(result.r, 5.0)
        self.assertAlmostEqual(result.fx, 3.0)
        self.assertAlmostEqual(result.fy, 4.0)
        self.assertAlmostEqual(result.angle, 53.1301, places=4)

    def test_opposite_forces(self) -> None:
        result = resultant_two_forces(100, 0, 40, 180)
        self.assertAlmostEqual(result.r, 60.0)
        self.assertAlmostEqual(result.angle, 0.0)

    def test_zero_forces(self) -> None:
        result = resultant_two_forces(0, 0, 0, 90)
        self.assertAlmostEqual(result.r, 0.0)
        self.assertEqual(result.angle, 0.0)

    def test_angles_are_normalized(self) -> None:
        result = resultant_two_forces(10, 370, 0, 0)
        self.assertAlmostEqual(result.r, 10.0)
        self.assertAlmostEqual(result.angle, 10.0)

    def test_negative_force_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            resultant_two_forces(-1, 0, 10, 0)


class BeamTests(unittest.TestCase):
    def test_point_load_reactions(self) -> None:
        result = beam_reactions_point_load(span=4.0, distance=1.0, load=1000.0)
        self.assertAlmostEqual(result.ra, 750.0)
        self.assertAlmostEqual(result.rb, 250.0)
        self.assertAlmostEqual(result.ra + result.rb, result.total)

    def test_load_in_the_middle(self) -> None:
        result = beam_reactions_point_load(span=6.0, distance=3.0, load=900.0)
        self.assertAlmostEqual(result.ra, 450.0)
        self.assertAlmostEqual(result.rb, 450.0)

    def test_load_at_support(self) -> None:
        result = beam_reactions_point_load(span=5.0, distance=0.0, load=500.0)
        self.assertAlmostEqual(result.ra, 500.0)
        self.assertAlmostEqual(result.rb, 0.0)

    def test_invalid_inputs(self) -> None:
        invalid = [
            (0.0, 0.0, 100.0),
            (-2.0, 1.0, 100.0),
            (4.0, 5.0, 100.0),
            (4.0, -1.0, 100.0),
            (4.0, 1.0, -10.0),
        ]
        for span, distance, load in invalid:
            with self.subTest(span=span, distance=distance, load=load):
                with self.assertRaises(ValueError):
                    beam_reactions_point_load(span, distance, load)

    def test_symmetry(self) -> None:
        left = beam_reactions_point_load(10.0, 2.0, 800.0)
        right = beam_reactions_point_load(10.0, 8.0, 800.0)
        self.assertAlmostEqual(left.ra, right.rb)
        self.assertAlmostEqual(left.rb, right.ra)

    def test_equilibrium_with_angles_consistency(self) -> None:
        # Comprobación numérica: la resultante de dos fuerzas opuestas es nula.
        result = resultant_two_forces(50, 30, 50, 30 + 180)
        self.assertLess(result.r, 1e-9)
        self.assertTrue(math.isclose(result.r, 0.0, abs_tol=1e-9))


if __name__ == "__main__":
    unittest.main(verbosity=2)

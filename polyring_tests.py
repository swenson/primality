import unittest
from polyring import *
from cyclo import *


class PolyRingTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_field10(self):
    k = CyclotomicField(10, 30)
    r = PolynomialRing(k)
    a = k([5])
    self.assertEqual(r([a]) * r([a]), r([a * a]))
    self.assertEqual(r([k(), a]) * r([a]), r([k(), a * a]))
    self.assertEqual(r([k(), a]) * r([k(), a]), r([k(), k(), a * a]))
import unittest
from cyclo import *



class CycloTests(unittest.TestCase):
  def setUp(self):
    pass

  def test_field10(self):
  	k = CyclotomicField(10, 30)
  	self.assertEqual(k([5]) * k([5]), k([25]))
  	self.assertEqual(k([5]) * k([5, 1]), k([25, 5]))
  	self.assertEqual(k([0, 1]) * k([1, 1]), k([0, 1, 1]))
  	self.assertEqual(k([0, 2]) * k([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]), k([2]))
  	self.assertEqual(k([0, 29]) * k([0, 0, 0, 0, 0, 0, 0, 0, 0, 2]), k([28]))

  def test_field1000(self):
		k = CyclotomicField(1000, 30)
		a = k()
		a.value[-1] = 1
		b = k()
		b.value[-2] = 1
		self.assertEqual(a * a, b)

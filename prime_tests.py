import unittest
import miller_rabin
import fast_aks
from math import ceil, sqrt



class PrimeTests(unittest.TestCase):
  def setUp(self):
    self.is_primes = [miller_rabin.is_prime, fast_aks.is_prime]

  def test_known_factorizations(self):
    self.assertEqual(fast_aks.factorization(15),
                     [3, 5])
    self.assertEqual(fast_aks.factorization(2), [2])
    self.assertEqual(fast_aks.factorization(3), [3])
    self.assertEqual(fast_aks.factorization(9), [3, 3])
    self.assertEqual(fast_aks.factorization(96), [2, 2, 2, 2, 2, 3])

  def test_primtiive_root(self):
    self.assertEqual(fast_aks.primitive_root(3), 2)
    self.assertEqual(fast_aks.primitive_root(5), 2)
    self.assertEqual(fast_aks.primitive_root(7), 3)
    self.assertEqual(fast_aks.primitive_root(97), 5)

  def test_fast_aks(self):
    #self.assertEqual(fast_aks.is_prime(101), True)
    pass

  def test_known_primes(self):
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 82104551, 452784427,
              46897875786625702576864112692857487051,
              16924980224899166400812497777709246533,
              2345025074052479518600795136681355950888074907685014583790880397468973914695237139661677440025217429981429253627078303444430132992263268824958968314521]:
      self.assertTrue(miller_rabin.is_prime(p))

  def test_known_composites(self):
    for n in [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 100]:
      self.assertFalse(miller_rabin.is_prime(n))

  def test_first_primes(self):
    primes = [2]
    for q in xrange(3, 10000, 2):
      s = int(ceil(sqrt(q)))
      prime = True
      for p in primes:
        if p > s:
          break
        if q % p == 0:
          prime = False
          break
      if prime:
        primes.append(q)
    for p in primes:
      self.assertTrue(miller_rabin.is_prime(p))



if __name__ == '__main__':
  unittest.main()
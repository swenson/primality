from random import randint
from fast_aks import ctz

known_small_primes = frozenset([2, 3, 5, 7, 11, 13, 17])

def is_prime(p, k=40):
  p = int(p)
  if p in known_small_primes:
    return True
  if p <= 10:
    return False
  n1 = p - 1
  s = ctz(n1)
  d = n1 >> s
  check = list(known_small_primes)
  for i in xrange(k):
    if check:
      a = check.pop()
    else:
      a = randint(17, p - 2)
    x = pow(a, d, p)
    if x == 1 or x == n1:
      continue
    for j in xrange(s - 1):
      x = (x * x) % p
      if x == 1:
        return False
      if x == n1:
        break
    else:
      return False
  return True

from random import randint
from math import ceil, log, exp, floor, factorial, sqrt

# http://www.math.dartmouth.edu/~carlp/PDF/complexity12.pdf
def is_prime(n):
  if has_square(n):
    return False

  pairs, primes = find_pairs(n)
  D = int(ceil(log(n, 2)**2))
  B = int(floor(sqrt(D) * log(n, 2)))
  for p in primes:
    if n == p:
      return True
    if p > B:
      break
    if n % p == 0:
      return False

  poly, prime = find_monic(n, pairs)
  if not prime:
    return False
  for a in xrange(1, B + 1):
    if not a_poly_equals(a, n, poly):
      return False
  return True

def has_square(n):
  if n < 0: n = -n
  k = 2
  root = pow(n, 1.0 / k)
  while int(round(root)) != 1:
    # use root as the first approximation in a newton step
    x = root
    for i in xrange(10):
      if x == 0: x = 0.000001
      x = x - k * (x**(k - 1)) / (x**k)

    x = int(round(x))
    if x**k == n:
      return True

    k += 1
    root = pow(n, 1.0 / k)
  return False

def compute_factorizations(upper):
  factorizations = [list() for i in xrange(upper + 1)]
  primes = []
  p = 2
  while p <= upper:
    if not factorizations[p]:
      primes.append(p)
      for q in xrange(p, upper + 1, p):
        factorizations[q].append(p)
    p += 1
  return factorizations, primes

def is_squarefree(n):
  return not has_square(n)

def factors_for(num, factors):
  if num < 0:
    num = -num
  if num == 1:
    return True
  for f in factors:
    while num % f == 0:
      num //= f
    if num == 1:
      return True
  return num == 1

def find_pairs(n, D = None):
  if D is None:
    D = int(ceil(log(n, 2) ** 2))

  factorizations, primes = compute_factorizations(4 * D)
  D611 = int(ceil(pow(D, 6/11.0)))
  D311 = pow(D, 3/11.0)
  qlower = exp(log(D) / (log(log(2 * D))**2))
  pairs = set()
  qs = set()
  qmap = {}
  for r in primes:
    if r >= D611: break
    for q in primes:
      if (r - 1) % q != 0:
        continue
      if not (qlower < q < D311):
        continue
      nr = pow(n, (r - 1) / q, r)
      if nr != 1:
        pairs.add((r, q))
        qs.add(q)
        qmap[q] = r
  for d in xrange(D, 4 * D + 1):
    if is_squarefree(d) and factors_for(d, qs):
      break
  else:
    return find_pairs(n, 4 * D)
  return [(qmap[q], q) for q in factorizations[d]], primes

def choose(n, k):
  return factorial(n) / (factorial(k) * factorial(n - k))

def a_poly_equals(a, n, poly):
  for i in xrange(1, n + 1):
    b = choose(n, i)
    if b * (a ** i) != 0:
      return False
  return True

def totient(n):
  prod = n
  for p in set(factorization(n)):
    prod = prod * (p - 1) / p
  return prod

def factorization(n):
  if n <= 1: return []
  twos = ctz(n)
  n >>= twos
  factors = [2] * twos
  primes = [2]
  s = int(ceil(sqrt(n)))
  for q in xrange(3, s + 2, 2):
    if n == 1:
      break
    while n % q == 0:
      factors.append(q)
      n /= q
  if n != 1:
    factors.append(n)
  return factors

def primitive_root(r):
  phi = totient(r)
  factors = set(factorization(phi))
  for m in xrange(2, r):
    for p in factors:
      if pow(m, phi / p, r) == 1:
        break
    else:
      return m

def find_monic(n, pairs):
  # TODO
  # stage 1
  for r, q in pairs:
    z = primitive_root(r)
    Sj = find_sj(z, pairs)
  # stage 2
  # stage 3

def ctz(n):
  if n == 0:
    return 0
  elif n & 1 == 1:
    return 0
  z = 0
  while n & 1 == 0:
    z += 1
    n >>= 1
  return z
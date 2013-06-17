from random import randint
from math import ceil, log, exp, floor, factorial, sqrt

# http://www.math.dartmouth.edu/~carlp/PDF/complexity12.pdf
def is_prime(n):
  if is_power(n):
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

def is_power(n):
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

def factors_for_and_squarefree(num, factors):
  if num < 0:
    num = -num
  if num == 1:
    return True
  for f in factors:
    i = 0
    while num % f == 0:
      num //= f
      i += 1
    if i > 1:
      return False
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
    if factors_for_and_squarefree(d, qs):
      break
  else:
    return find_pairs(n, 4 * D)
  print "d =", d
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

def find_sj(z, pairs, n):

  def add(p, q):
    if len(q) > len(p):
      p.extend([0] * (len(q) - len(p)))
    for i, qi in enumerate(q):
      p[i] = (p[i] + qi) % n

  def sub(p, q):
    if len(q) > len(p):
      p.extend([0] * (len(q) - len(p)))
    for i, qi in enumerate(q):
      p[i] = (p[i] - qi) % n

  def add3(p, q):
    r = p[:]
    add(r, q)
    return r

  def school_mult(p, q, r):
    pq = [0] * r
    qis = [(i, qi) for i, qi in enumerate(q) if qi != 0]
    for i, pi in enumerate(p):
      if pi == 0: continue
      for j, qj in qis:
        pq[(i + j) % r] += (pi * qj) % n
    return pq

  def mult(p, q, r):
    if len(p) <= 16 or len(q) <= 16:
      return school_mult(p, q, r)
    # karatsuba in da house
    x0 = p[:len(p)/2]
    x1 = p[len(p)/2:]
    y0 = q[:len(q)/2]
    y1 = q[len(q)/2:]
    z2 = mult(x1, y1, r)
    z0 = mult(x0, y0, r)
    z1 = mult(add3(x0, x1), add3(y0, y1), r)
    sub(z1, z2)
    sub(z1, z0)
    z0.extend(z1)
    z0.extend(z2)
    return z0

  def school_multiply(p, q, r):
    # lazy schoolbook multiplication
    pq = [list() for i in xrange(len(p) + len(q))]

    for i, pi in enumerate(p):
      for j, qj in enumerate(q):
        add(pq[i + j], mult(pi, qj, r))
    return pq

  def bigadd(p, q):
    if len(q) > len(p):
      p.extend([list() for i in xrange(len(q) - len(p))])
    for i, qi in enumerate(q):
      add(p[i], q[i])

  def bigsub(p, q):
    if len(q) > len(p):
      p.extend([list() for i in xrange(len(q) - len(p))])
    for i, qi in enumerate(q):
      sub(p[i], q[i])

  def bigadd3(p, q):
    r = p[:]
    bigadd(r, q)
    return r

  def multiply(p, q, r):
    print "Multiplying %d x %d" % (len(p), len(q))
    if len(p) <= 1 or len(q) <= 1:
      return school_multiply(p, q, r)

    # karatsuba in da house
    x0 = p[:len(p)/2]
    x1 = p[len(p)/2:]
    y0 = q[:len(q)/2]
    y1 = q[len(q)/2:]
    z2 = multiply(x1, y1, r)
    z0 = multiply(x0, y0, r)
    z1 = multiply(bigadd3(x0, x1), bigadd3(y0, y1), r)
    bigsub(z1, z2)
    bigsub(z1, z0)
    z0.extend(z1)
    z0.extend(z2)
    return z0


  def multiply_down(polys, r):
    print "Mutiplying down %d" % len(polys)
    if len(polys) == 1:
      return polys[0]
    if len(polys) == 2:
      return multiply(polys[0], polys[1], r)
    mid = len(polys) / 2
    return multiply(multiply_down(polys[0:mid], r), multiply_down(polys[mid:], r), r)

  print z
  print pairs

  gs = []

  for r, q in pairs:
    polys = []
    for j in xrange(q):
      Sj = set()
      zj = pow(z, j, r)
      zq = pow(z, q, r)
      zjlq = zj
      Sj.add(zjlq)
      for l in xrange((r - 1) / q):
        zjlq += zq
        Sj.add(zjlq)
      poly = [0] * (max(Sj) + 1)
      for m in Sj:
        poly[m] = -1
      polys.append([[1], poly])
    print Sj
    g = multiply_down(polys, r)
    print len(g)
    gs.append(g)











def find_monic(n, pairs):
  # TODO
  # stage 1
  for r, q in pairs:
    z = primitive_root(r)
    Sj = find_sj(z, pairs, n)
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


if __name__ == '__main__':
  print is_prime(31)
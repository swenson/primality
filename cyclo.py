K_THRESH = 128

class CyclotomicField(object):
	def __init__(self, n, m):
		self.n = n
		self.m = m

	def __call__(self, value=None):
		return CyclotomicFieldElement(self, value)
	def __eq__(self, other):
		return self.n == other.n and self.m == other.m

class CyclotomicFieldElement(object):
	def __init__(self, field, value=None):
		self.n = field.n
		self.m = field.m
		self.field = field
		if value:
			self.value = list(value) + [0] * (self.n - len(value))
		else:
			self.value = [0] * (self.n)

	def copy(self):
		return self.field(self.value[:])

	def __eq__(self, other):
		return self.field == other.field and self.value == other.value

	def __sub__(self, other):
		result = [0] * self.n
		m = self.m
		a = self.value
		b = other.value
		for i in xrange(self.n):
			result[i] = (a[i] - b[i]) % m
		return self.field(result)

	def __add__(self, other):
		result = [0] * self.n
		m = self.m
		a = self.value
		b = other.value
		for i in xrange(self.n):
			result[i] = (a[i] + b[i]) % m
		return self.field(result)

	def __mul__(self, other):
		return self.field(mult(self.value, other.value, self.n, self.m))
		# result = [0] * self.n
		# m = self.m
		# a = self.value
		# b = other.value

		# for i in xrange(self.n):
		# 	r = 0
		# 	for j in xrange(0, i + 1):
		# 		r += (a[i + j] * b[i - j]) % m
		# 	for j in xrange(i, self.n):
		# 		r += (a[i + j]) * b[i - j + n]) % m
		#   result[i] = r
	def __str__(self):
	  return "<%s>" % self.value

	def __repr__(self):
	  return "<%s>" % self.value

	def square(self):
		return self * self

def add(p, q, m):
  if len(q) > len(p):
    p.extend([0] * (len(q) - len(p)))
  for i, qi in enumerate(q):
    p[i] = (p[i] + qi) % m

def sub(p, q, m):
  if len(q) > len(p):
    p.extend([0] * (len(q) - len(p)))
  for i, qi in enumerate(q):
    p[i] = (p[i] - qi) % m

def add3(p, q, m):
  r = p[:]
  add(r, q, m)
  return r

def school_mult(p, q, n, m):
	pq = [0] * n
	qis = [(i, qi) for i, qi in enumerate(q) if qi != 0]
	for i, pi in enumerate(p):
	  if pi == 0: continue
	  for j, qj in qis:
	    ijr = (i + j) % n
	    pq[ijr] = (pq[ijr] + pi * qj) % m
	return pq

def mult(p, q, n, m, offset=0):
	if len(p) <= K_THRESH or len(q) <= K_THRESH:
	  return fold([0] * offset + school_mult(p, q, n, m), n, m)
	# karatsuba in da house
	x0 = p[:len(p)/2]
	x1 = p[len(p)/2:]
	y0 = q[:len(q)/2]
	y1 = q[len(q)/2:]
	z2 = mult(x1, y1, n, m, offset=len(p)/2)
	z0 = mult(x0, y0, n, m, offset=len(p)/2)
	z1 = mult(add3(x0, x1, m), add3(y0, y1, m), n, m, offset=len(p)/2)
	sub(z1, z2, m)
	sub(z1, z0, m)
	z1 = [0] * (len(p) / 2) + z1
	z0.extend(z1)
	z0.extend(z2)
	return fold([0] * offset + z0, n, m)

def fold(z0, n, m):
	if len(z0) > n:
		j = 0
		for i in xrange(n, len(z0)):
			z0[j] = (z0[j] + z0[i]) % m
			j += 1
			if j >= n:
				j -= n
		z0 = z0[:n]

	return z0


if __name__ == '__main__':
	import random
	r = 12389183912
	n = 8192
	k = CyclotomicField(n, r)
	a = k([random.randint(0, r - 1) for i in xrange(n)])
	import timeit
	for t in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]:
		print t
		print timeit.timeit("a * a", setup="import cyclo; cyclo.K_THRESH = %d; a = cyclo.CyclotomicField(%d, %d)(%s)" % (t, n, r, a.value), number=1)


K_THRESH = 1

class PolynomialRing(object):
	def __init__(self, field):
		self.field = field

	def __call__(self, value=None):
		return PolynomialRingElement(self, self.field, value)

	def __eq__(self, other):
		return self.field == other.field

class PolynomialRingElement(object):
	def __init__(self, ring, field, value=None):
		self.ring = ring
		self.field = field
		if value:
			self.value = value
		else:
			self.value = [field()]

	def __eq__(self, other):
		return self.ring == other.ring and self.field == other.field and self.value == other.value

	def __add__(self, other):
		l = max(len(self.value), len(other.value))
		result = list(self.value) + [self.field() for i in xrange(l - len(self.value))]
		for i, v in enumerate(other.value):
			result[i] += v
		return result

	def __mul__(self, other):
		return self.ring(mult(self.value, other.value))

	def __str__(self):
	  return "<%s>" % self.value

	def __repr__(self):
	  return "<%s>" % self.value

def add(p, q):
  for i, qi in enumerate(q):
    p[i] += qi

def sub(p, q):
  for i, qi in enumerate(q):
    p[i] -= qi

def add3(p, q):
  r = [x.copy() for x in p]
  add(r, q)
  return r

def school_mult(p, q):
	pq = [pi * q[0] for pi in p]
	for i, pi in enumerate(p):
	  for j, qj in enumerate(q):
	  	if j == 0: continue
	  	pq[i + j] += pi * qj
	return pq

def mult(p, q):
	if len(p) <= K_THRESH or len(q) <= K_THRESH:
	  return school_mult(p, q)
	# karatsuba in da house
	x0 = p[:len(p)/2]
	x1 = p[len(p)/2:]
	y0 = q[:len(q)/2]
	y1 = q[len(q)/2:]
	z2 = mult(x1, y1)
	z0 = mult(x0, y0)
	z1 = mult(add3(x0, x1), add3(y0, y1))
	sub(z1, z2)
	sub(z1, z0)
	z0.extend(z1)
	z0.extend(z2)
	return z0

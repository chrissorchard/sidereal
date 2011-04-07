"""Who loves quaternions!?"""

class Quaternion(tuple):
    def __str__(self):
        """Construct a concise string representation.

        """
        return "Quaternion((%.2f, %.2f, %.2f, %.2f))" % self

    def __repr__(self):
        """Construct a precise string representation.

        """
        return "Quaternion((%r, %r, %r, %r))" % self

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @property
    def w(self):
        return self[3]

    def __add__(self,other):
        a1,b1,c1,d1 = self
        a2,b2,c2,d2 = other

        return Quaternion((a1+a2,b1+b2,c1+c2,d1+d2))

    def __mul__(self,other):
        try:
            other = float(other)
            return Quaternion((self[0] * other, self[1] * other, self[2] * other, self[3] * other))
        except TypeError:
            a1,b1,c1,d1 = self
            a2,b2,c2,d2 = other

            q1 = a1*a2 - b1*b2 - c1*c2 - d1*d2
            q2 = a1*b2 + b1*a2 + c1*d2 - d1*c2
            q3 = a1*c2 - b1*d2 + c1*a2 + d1*b2
            q4 = a1*d2 + b1*c2 - c1*b2 + d1*a2

            return Quaternion((q1,q2,q3,q4))

    def conjugate(self):
        return self + q_i*self*q_i + q_j*self*q_j + q_k*self*q_k * -0.5

def q(*args):
    """Construct a quaternion from an iterable or from multiple arguments.

    """
    if len(args) == 1:
        return Quaternion(args[0])
    return Quaternion(args)

q_1 = Quaternion((1,0,0,0))
q_i = Quaternion((0,1,0,0))
q_j = Quaternion((0,0,1,0))
q_k = Quaternion((0,0,0,1))

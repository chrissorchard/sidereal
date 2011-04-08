"""Who loves quaternions!?"""

from __future__ import division

import math

# This is from sidereal.vector
# I would import it, but that would mean this class no longer stands alone.
def cached(func):
    """Decorate a function as a caching property.

    :Parameters:
        `func` : function
            The getter function to decorate.

    """
    cached_name = "_cached_%s" % func.func_name

    # The keywords 'getattr' and 'cached_name' are used to optimise the common
    # case (return cached value) by bringing the used names to local scope.
    def fget(self, getattr=getattr, cached_name=cached_name):
        try:
            return getattr(self, cached_name)
        except AttributeError:
            value = func(self)
            setattr(self, cached_name, value)
            return value

    def fset(self, value):
        assert not hasattr(self, cached_name)
        setattr(self, cached_name, value)

    fget.func_name = "get_" + func.func_name
    fset.func_name = "set_" + func.func_name

    return property(fget, fset, doc=func.func_doc)

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

    @cached
    def norm(self):
        return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2 + self[3]**2)

    @cached
    def axisangle(self):
        q1,q2,q3,q4 = self
        halftheta = math.acos(q4)
        x = q1 / math.sin(halftheta)
        y = q2 / math.sin(halftheta)
        z = q3 / math.sin(halftheta)
        return (x,y,z),halftheta*2


    def versor(self):
        qx,qy,qz,qw = self
        n = self.norm
        return Quaternion((qx / n, qy / n, qz / n, qw / n))

    def __add__(self,other):
        a1,b1,c1,d1 = self
        a2,b2,c2,d2 = other

        return Quaternion((a1+a2,b1+b2,c1+c2,d1+d2))

    def __sub__(self,other):
        a1,b1,c1,d1 = self
        a2,b2,c2,d2 = other

        return Quaternion((a1-a2,b1-b2,c1-c2,d1-d2))

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
        return Quaternion((self[0],-self[1],-self[2],-self[3]))

    @classmethod
    def from_axisangle(cls,axis,angle):
        halfangle = angle / 2
        x,y,z = axis
        q1 = x * math.sin(halfangle)
        q2 = y * math.sin(halfangle)
        q3 = z * math.sin(halfangle)
        q4 = math.cos(halfangle)
        return Quaternion((q1,q2,q3,q4))

    @classmethod
    def from_euler(cls,angles):
        pitch,yaw,roll = angles
        # or x,y,z
        # or pitcx,yaw,rolz
        i = (1,0,0)
        j = (0,1,0)
        k = (0,0,1)

        iq = cls.from_axisangle(i,pitch)
        jq = cls.from_axisangle(j,yaw)
        kq = cls.from_axisangle(k,roll)

        return iq * jq * kq

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

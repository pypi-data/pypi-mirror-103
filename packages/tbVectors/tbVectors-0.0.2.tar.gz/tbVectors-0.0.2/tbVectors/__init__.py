import math
import random


class Vector:
    def __init__(self, *args):
        if args == ():
            args = (0, 0)
        args = args[0] if len(args) == 1 else args
        self.x = args[0]
        self.y = args[1]

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def set_vecs(self, *args):
        self.__init__(args)

    def normalize(self):
        try:
            self.x /= magnitude
            self.y /= magnitude
        except ZeroDivisionError:
            self.x = 0
            self.y = 0

    def cap_mag(self, cap):
	if self.get_mag() > cap:
	    self.setMag(cap)

    def get_mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def setMag(self, mag):
        try:
            cur_mag = self.get_mag()
            self.x *= mag / cur_mag
            self.y *= mag / cur_mag
        except ZeroDivisionError:
            self.x = 0
            self.y = 0
    
    def add(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int):
            self.x += other
            self.y += other

    def sub(self, other):
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int):
            self.x -= other
            self.y -= other

    def mult(self, other):
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int):
            self.x *= other
            self.y *= other

    def div(self, other):
        if isinstance(other, Vector):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, int):
            self.x /= other
            self.y /= other

    def get_pos(self):
        return self.x, self.y

    def heading(self):
        return math.atan2(self.y, self.x)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif isinstance(other, int):
            return Vector(self.x / other, self.y / other)

    def __gt__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() > other.get_mag()
        elif other is None:
            return True
        
    def __ge__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() >= other.get_mag()
        elif other is None:
            return True

    def __lt__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() < other.get_mag()
        elif other is None:
            return True
        
    def __le__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() <= other.get_mag()
        elif other is None:
            return True
        
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() == other.get_mag()
        elif other is None:
            return True
        
    def __ne__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() != other.get_mag()
        elif other is None:
            return True
        
    def __bool__(self, other):
        if isinstance(other, Vector):
            return self.get_mag() != 0
        elif other is None:
            return True
        
    def __reversed__(self):
        a = self.x
        self.x = self.y
        self.y = a

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y

    @classmethod
    def from_angle(cls, angle):
        return cls(math.cos(angle), math.sin(angle))

    @classmethod
    def random_vector(cls, min, max):
        return cls(random.randint(min, max), random.randint(min, max))

    @staticmethod
    def angle_from_vecs(v1, v2):
        return math.asin((v2.y - v1.y) / Vector.distance(v1, v2))

    @staticmethod
    def distance(p1, p2):
        if p1 is None or p2 is None:
            return math.inf

        if not isinstance(p1, Vector):
            p1 = Vector(p1)
        if not isinstance(p2, Vector):
            p2 = Vector(p2)

        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

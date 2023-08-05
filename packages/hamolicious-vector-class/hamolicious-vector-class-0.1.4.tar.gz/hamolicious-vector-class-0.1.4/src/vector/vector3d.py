from math import sin, cos, atan2, sqrt
from random import randint

def get_unit():
	return randint(-10000, 10000) / 10000
def get_normal():
	return randint(0, 10000) / 10000

class Vec3d:
	def __get_xyz(self, *args) -> list[float]:
		args = args[0]
		number_of_args = len(args)

		if number_of_args == 0:
			return 0, 0, 0  # no arguments
		elif number_of_args == 3:
	   		return args  # x, y and z passed in
		elif number_of_args == 1:  # one argument
			arg_type = type(args[0])

			if arg_type is float or arg_type is int:  # single int or float argument
				return args[0], args[0], args[0]
			if arg_type is list or arg_type is tuple:
				if len(args[0]) == 1:
					return args[0][0], args[0][0], args[0][0]
				return args[0][0], args[0][1], args[0][2]  # single list argument
			if arg_type is Vec3d:
				return args[0].x, args[0].y, args[0].z

		raise TypeError(f'Invalid Input: {args}')

	def __init__(self, *args) -> None:
		self.__elements = self.__get_xyz(args)


	#region Properties

	#---------------------- X
	@property
	def x(self):
		return self.__elements[0]
	@x.setter
	def x(self, val):
		self.__elements[0] = val

	#---------------------- Y
	@property
	def y(self):
		return self.__elements[1]
	@y.setter
	def y(self, val):
		self.__elements[1] = val

	#---------------------- Z
	@property
	def z(self):
		return self.__elements[2]
	@z.setter
	def z(self, val):
		self.__elements[2] = val

	#---------------------- W
	@property
	def w(self):
		return self.__elements[0]
	@w.setter
	def w(self, val):
		self.__elements[0] = val

	#---------------------- H
	@property
	def h(self):
		return self.__elements[1]
	@h.setter
	def h(self, val):
		self.__elements[1] = val

	#---------------------- D
	@property
	def d(self):
		return self.__elements[2]
	@d.setter
	def d(self, val):
		self.__elements[2] = val

	#---------------------- Magnitude
	@property
	def length(self):
		return self.get_magnitude()


	#endregion


	#region Creation methods

	@staticmethod
	def random_unit():
		return Vec3d(get_unit(), get_unit(), get_unit())

	@staticmethod
	def random_pos():
		return Vec3d(get_normal(), get_normal(), get_normal())

	@staticmethod
	def zero():
		return Vec3d()

	#endregion


	#region General manipulation methods

	def get(self):
		return list(self.__elements)

	def get_int(self):
		return [int(self.x), int(self.y), int(self.z)]

	def set(self, *args):
		x, y, z = self.__get_xyz()
		self.__elements = x, y, z

	def copy(self):
		return Vec3d(self.x, self.y, self.z)

	def clear(self):
		self.x = self.y = self.z = 0

	#endregion


	#region Mathematical manipulation methods

	def dist_sqrt(self, *args):
		x, y, z = self.__get_xyz(args)
		return sqrt((self.x - x)**2 + (self.y - y)**2 + (self.z - z)**2)

	def dist(self, *args):
		x, y, z = self.__get_xyz(args)
		return (self.x - x)**2 + (self.y - y)**2 + (self.z - z)**2

	def get_magnitude(self):
		return sqrt(self.x**2 + self.y**2 + self.z**2)

	def normalise(self):
		mag = self.length
		if mag == 0 : return
		self.div(mag)

	def clamp(self, *args):
		max_x, max_y, max_z = self.__get_xyz(args)

		if self.x > max_x : self.x = max_x
		if self.y > max_y : self.y = max_y
		if self.z > max_z : self.z = max_z

		if self.x < -max_x : self.x = -max_x
		if self.y < -max_y : self.y = -max_y
		if self.z < -max_z : self.z = -max_z

	def add(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x += x
		self.y += y
		self.z += z

	def sub(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x -= x
		self.y -= y
		self.z -= z

	def mult(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x *= x
		self.y *= y
		self.z *= z

	def div(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x /= x
		self.y /= y
		self.z /= z

	def linear_interpolate(self, *args, t=0.5):
		x, y, z = self.__get_xyz(args)

		x = self.x + t * (x - self.x)
		y = self.y + t * (y - self.y)
		z = self.z + t * (y - self.z)

		self.set(x, y, z)

	def dot_product(self, *args):
		x, y, z = self.__get_xyz(args)
		return sum([self.x * x, self.y * y, self.z * z])

	#endregion


	#region Dunder methods

	def __iadd__(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x += x ; self.y += y ; self.z += z
		return self

	def __isub__(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x -= x ; self.y -= y ; self.z -= z
		return self

	def __imul__(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x *= x ; self.y *= y ; self.z *= z
		return self

	def __idiv__(self, *args):
		x, y, z = self.__get_xyz(args)
		self.x /= x ; self.y /= y ; self.z /= z
		return self

	def __add__(self, *args):
		x, y, z = self.__get_xyz(args)
		return Vec3d(self.x + x, self.y + y, self.z + z)

	def __sub__(self, *args):
		x, y, z = self.__get_xyz(args)
		return Vec3d(self.x - x, self.y - y, self.z - z)

	def __mul__(self, *args):
		x, y, z = self.__get_xyz(args)
		return Vec3d(self.x * x, self.y * y, self.z * z)

	def __div__(self, *args):
		x, y, z = self.__get_xyz(args)
		return Vec3d(self.x / x, self.y / y, self.z / z)

	def __getitem__(self, index):
		return self.__elements[index]

	def __repr__(self):
		return f'vector X: {self.x}, Y: {self.y}, Z: {self.z}'

	#endregion




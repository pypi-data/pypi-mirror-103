from random import randint
from math import sin, cos, sqrt

class Vec3d:
    #region INIT
    def _get_xyz(self, args):
        """Generates a x, y and z from any input
        Returns:
            [tuple]: x, y, z
        """
        number_of_args = len(args)

        if   number_of_args == 0 : return 0, 0, 0 # no arguments
        elif number_of_args == 3 : x, y, z = args ; return x, y, z # both x and y passed in

        if number_of_args == 1: # one argument
            arg_type = type(args[0])

            if arg_type is float or arg_type is int: # single int or float argument
                return args[0], args[0], args[0]
            if arg_type is list or arg_type is tuple:
                return args[0][0], args[0][1], args[0][2] # single list argument
            if arg_type is Vec3d:
                return args[0].x, args[0].y, args[0].z

    def __init__(self, *args):
        self.x, self.y, self.z = self._get_xyz(args)
        self.data = {}
    #endregion

    #region AUTO CREATE METHODS

    def random_pos():
        """Returns a vector in normalised 0-1 space
        Returns:
            Vector2D: a vector in normal space
        """
        return Vec3d(randint(0, 1000)/1000, randint(0, 1000)/1000, randint(0, 1000)/1000)

    def random_unit():
        """Generates a unit vector with a random heading
        Returns:
            Vector2D: unit vector
        """
        pos = Vec3d(randint(-1000, 1000), randint(-1000, 1000), randint(-1000, 1000))
        pos.normalise()
        return pos

    #endregion

    #region CUSTOM METHODS

    def get(self):
        """Gets the x, y and z components as an integer tuple
        Returns:
            tuple: contains x, y and z as integers
        """
        return (int(self.x), int(self.y), int(self.z))

    def set(self,  *args):
        """Sets the x, y and z components
        """
        x, y, z = self._get_xyz(args)
        self.x = x ; self.y = y ; self.z = z

    def copy(self):
        """Gets a copy of this vector
        Returns:
            Vector2D: a copy of this vector
        """
        return Vec3d(self.x, self.y, self.z)

    def clear(self):
        """Sets both components to 0
        """
        self.x = self.y = self.z = 0

    #endregion

    #region CUSTOM MATHEMATICAL METHODS
    def dist_sqrt(self, *args):
        """Gets the distance between this point and another (uses square root)
        Returns:
            float: distance
        """
        x, y, z = self._get_xyz(args)
        return sqrt((self.x - x)**2 + (self.y - y)**2 + (self.z - z)**2)

    def dist(self, *args):
        """Gets the distance between this point and another (does not use square root)
        Returns:
            float: distance
        """
        x, y, z = self._get_xyz(args)
        return (self.x - x)**2 + (self.y - y)**2 + (self.z - z)**2

    def get_magnitude(self):
        """Gets the magnitude/length of the vector
        Returns:
            float: magnitude
        """
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalise(self):
        """Normalises this vector making it a unit vector
        """
        mag = self.get_magnitude()
        if mag == 0 : return
        self.div(mag)
    def normalize(self):
        """Normalises this vector making it a unit vector
        """
        self.normalise()

    def truncate(self, max_val):
        """Clamps the x, y and z components to be in range -max_val to max_val
        Args:
            max_val (float): max and min for each component
        """
        if self.x > max_val : self.x = max_val
        if self.y > max_val : self.y = max_val
        if self.z > max_val : self.z = max_val

        if self.x < -max_val : self.x = -max_val
        if self.y < -max_val : self.y = -max_val
        if self.z < -max_val : self.z = -max_val

    def add(self, *args):
        x, y, z = self._get_xyz(args)
        self.x += x ; self.y += y ; self.z += z

    def sub(self, *args):
        x, y, z = self._get_xyz(args)
        self.x -= x ; self.y -= y ; self.z -= z

    def mult(self, *args):
        x, y, z = self._get_xyz(args)
        self.x *= x ; self.y *= y ; self.z *= z

    def div(self, *args):
        x, y, z = self._get_xyz(args)
        self.x /= x ; self.y /= y ; self.z /= z

    def linear_interpolate(self, *args, t=0.5):
        """Linearly interpolates between current position and passed in position
        Args:
            t (float, optional): speed. Defaults to 0.5.
        """
        x, y, z = self._get_xyz(args)

        x = self.x + t * (x - self.x)
        y = self.y + t * (y - self.y)
        z = self.z + t * (y - self.z)

        self.set(x, y, z)

    #endregion

    #region MAGIC METHODS
    def __iadd__(self, *args):
        x, y, z = self._get_xyz(args)
        self.x += x ; self.y += y ; self.z += z
        return self
    def __isub__(self, *args):
        x, y, z = self._get_xyz(args)
        self.x -= x ; self.y -= y ; self.z -= z
        return self
    def __imul__(self, *args):
        x, y, z = self._get_xyz(args)
        self.x *= x ; self.y *= y ; self.z *= z
        return self
    def __idiv__(self, *args):
        x, y, z = self._get_xyz(args)
        self.x /= x ; self.y /= y ; self.z /= z
        return self

    def __add__(self, *args):
        x, y, z = self._get_xyz(args)

        return Vec3d(self.x + x, self.y + y, self.z + z)
    def __sub__(self, *args):
        x, y, z = self._get_xyz(args)

        return Vec3d(self.x - x, self.y - y, self.z - z)
    def __mul__(self, *args):
        x, y, z = self._get_xyz(args)

        return Vec3d(self.x * x, self.y * y, self.z * z)
    def __div__(self, *args):
        x, y, z = self._get_xyz(args)

        return Vec3d(self.x / x, self.y / y, self.z / z)
    #endregion

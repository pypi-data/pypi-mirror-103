
from vector2d import Vec2d
from vector3d import Vec3d
import click

click.clear()

v = Vec2d(0.5, 0.5)
print(v.x, v.y)

v = Vec2d.random_unit()
print(v.x, v.y)

v = Vec2d.random_pos()
print(v.x, v.y)

v = Vec2d.random_pos()
print(v.get())

v = Vec2d.random_pos()
print(v.get_int())

v = Vec2d.random_pos()
print(v.copy())

v = Vec2d.random_pos()
print(v[0], v[1])

v = Vec2d.random_pos() * [10, 10]
print(v.get())

#---------------------

v = Vec3d(0.5, 0.5, 0.5)
print(v.x, v.y, v.z)

v = Vec3d.random_unit()
print(v.x, v.y, v.z)

v = Vec3d.random_pos()
print(v.x, v.y, v.z)

v = Vec3d.random_pos()
print(v.get())

v = Vec3d.random_pos()
print(v.get_int())

v = Vec3d.random_pos()
print(v.copy())

v = Vec3d.random_pos()
print(v[0], v[1], v[2])

v = Vec3d.random_pos() * [10, 10, 10]
print(v.get())

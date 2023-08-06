# pyvectors

This is a simple Mathematical Module which is extremely user-friendly.  The module deals with 3-dimensional real position **Vectors** centered at the Origin (0, 0, 0). Using this module, the algebra of **Vectors** can be easily performed in python. \
**Vector(x, y, z) -> xi + yj + zk** \
A lot of help text is included in the class, and in the error messages, hence making the module easy to use.

## Attributes of class Vector
Four Vector instances have been already defined in the module. These are:
- Vector.i -> **1i + 0j + 0k**
- Vector.j -> **0i + 1j + 0k**
- Vector.k -> **0i + 0j + 1k**
- Vector.null -> **0i + 0j + 0k**

These Vectors cannot be created through the Vector() constructor. Functions evaluating to these Vectors will return the predefined objects only. If these Vectors are changed by the user, the class may misbehave. Hence, user is advised to treat these objects as "read-only".

## Attributes of Vector objects
Vectors have attributes like x, y, z, magnitude, tuple, ... \
Attributes of Vectors are read-only. Manually editing any of them results in unexpected behavior, which renders the object useless and prone to errors.

## Methods

- add two Vectors:
    > returns resultant of the two Vectors \
    > can be achieved through v1 + v2
- subtract two Vectors:
    > returns the difference of the Vectors \
    > can be achieved through v1 - v2
- Vector.dot(v1, v2)
    > returns dot product of the two Vectors
- Vector.cross(v1, v2)
    > returns cross product of the two Vectors
- Vector.scale(v, k)
    > returns the Vector obtained by scaling the components of v by k \
    > can also be achieved through v * k
- Vector.angle(v1, v2)
    > returns the angle between the two Vectors
- Vector.scalar_triple(v1, v2, v3)
    > returns the scalar triple product of the Vectors taken in order
- Vector.vector_triple(v1, v2, v3)
    > returns the vector triple product of the Vectors taken in order
- Vector.unit(v)
    > returns the Unit Vector along the direction of v
- Vector.mod(v)
    > returns the magnitude or absolute value of the Vector v \
    > can also be achieved through abs(v)
 And many more... Each function contains help text that can be accessed through help() in python to know more about it. Users are advised to read help() on methods they want to use to ensure required results.

## Plotting a Vector
Two methods allow you to plot the Vector on a 3-dimensional mathematical plot:
- Vector.plot(v) -> plots single Vector
- Vector.plot_vectors(v1, v2, v3, ..., vn) -> plots multiple Vectors on the same grid

## Updates (0.2.2)
Minor bug fixes:
- Fixed all math domain errors
- Fixed issues with plotting multiple Vectors

## Updates (0.2.3)
Added methods which allow you to rotate Vectors using the Right-Hand Rule and Matrix Rotation:
- Vector.rotate(v, yaw=x, pitch=y, roll=z)
    > rotates the Vector by the given yaw, pitch and roll angles \
    > formally, this corresponds to an intrinsic rotation whose Tait-Bryan angles are x, y and z about the axes Z, Y and X respectively
- Vector.rotate_vector(v1, v2, phi=value)
    > rotates Vector v1 phi degrees about Vector v2 \
    > when phi > 0, the rotation will be counter-clockwise when v2 points towards the observer
- Vector.rotate_axis(v, axis="A", phi=value)
    > rotates the Vector phi degrees about the positive direction of the given axis \
    > when phi > 0, the rotation will be counter-clockwise when the positive direction of axis of rotation points towards the observer

## Updates (0.2.4)
You can now compare Vectors using in-build operators < and >. These operators are used to compare the magnitude / absolute value of two Vector objects. For example:
- v1 > v2 returns True if Vector.mod(v1) > Vector.mod(v2) and False in all other cases
- v1 < v2 returns True if Vector.mod(v1) < Vector.mod(v2) and False in all other cases
Note that relational operators <= and >= will still not be defined for Vector Objects as they lead to ambiguity. (Whether to compare magnitudes or compare for actual equality)

## Reach out to me
Feel free to reach out to me if you notice any bugs or if you need any kind of
help from me in understanding the usage of the module or the source code.
My email: knightt1821@gmail.com
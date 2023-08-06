"""pyvectors
Provides functions to perform operations on ℝ³ Vectors centered at the
Origin (0, 0, 0)"""

__name__ = "__main__"


class Vector():
    """Vector(x, y, z) = (x)î + (y)ĵ + (z)k̂
    represents a Vector centred at the Origin in 3D space

    see help(__init__) for help on Vector creation
    Truth Value of Vectors:
        bool(Vector.null) == False

    Predefined Vectors cannot be created through the Vector() constructor
    They can only be pointed-to with help of variables
    There is only one instance each of the predefined Vectors
    Overriding these may result in unusual behaviour"""


    def __init__(self, x, y, z, /):
        """initializes Vector instance
        x, y, z are Real Numbers which represent co-ordinates of the required
        position Vector
        attrs of Vector Object:
            • self.x == self.i = x
            • self.y == self.j = y
            • self.z == self.k = z
            • self.magnitude = mod(self)
            • self.tuple = components(self)"""

        vec = [x, y, z]

        for i in range(3):
            if not isinstance(vec[i], (int, float)):
                raise TypeError(" ".join((
                    "invalid component type for 'Vector':",
                    "must be 'int' / 'float'"
                )))
            if str(abs(vec[i])) in {"inf", "nan"}:
                raise ValueError(f"invalid component for 'Vector': '{vec[i]}'")

            if float(vec[i]).is_integer():
                vec[i] = int(vec[i])

        if __name__ != "__main__":
            if set(vec) == {0}:
                raise AttributeError("cannot create Vector 'null'")
            if (vec.count(1), vec.count(0)) == (1, 2):
                raise AttributeError("cannot create Vectors 'î', 'ĵ', 'k̂'")

        from math import hypot

        self.tuple = tuple(vec)
        self.x, self.y, self.z = self.i, self.j, self.k = self.tuple
        self.magnitude = hypot(*self.tuple)

        self.dict = {
            "x": self.x, "y": self.y, "z": self.z,
            "i": self.i, "j": self.j, "k": self.k,
            "tuple": self.tuple, "magnitude": self.magnitude
        }


    def __str__(self, /):
        """defines the str() method for Vector"""

        vec = list(Vector.components(self))
        sign, plus, minus = ["", "", ""], "", "- "

        for i in range(3):
            sign[i] = plus if vec[i] >= 0 else minus
            vec[i], plus = abs(vec[i]), "+ "

        return f"{sign[0]}{vec[0]}î {sign[1]}{vec[1]}ĵ {sign[2]}{vec[2]}k̂"


    def __repr__(self, /):
        """defines the repr() method for Vector"""

        vec = Vector.components(self)
        return f"Vector({vec[0]}, {vec[1]}, {vec[2]})"


    def __bool__(self, /):
        """defines the truth value of a Vector
        bool(Vector.null) == False"""

        return set(Vector.components(self)) != {0}


    def __hash__(self, /):
        """defines the hash value of a Vector"""

        Vector.ExceptionVector(self)
        return hash(repr(self))


    def __len__(self, /):
        """defines the len() method for Vector
        returns the number of dimensions spanned by the Vector"""

        return 3 - Vector.components(self).count(0)


    def __iter__(self, /):
        """implements iter(self)
        iterating over a Vector returns its component - vectors"""

        return iter(Vector.componentvectors(self))


    def __getitem__(self, axis):
        """defines indexing property for Vector
        indices defined here:
          'x' == 'i' = X-component
          'y' == 'j' = Y-component
          'z' == 'k' = Z-component"""

        Vector.ExceptionVector(self)

        if not isinstance(axis, str):
            raise TypeError("'Vector' indices must be 'str'")

        if axis not in {"x", "y", "z", "i", "j", "k"}:
            raise IndexError(" ".join((
                "invalid index for 'Vector':",
                "see help(__getitem__) for help on valid indices"
            )))

        if axis in {"x", "y", "z"}:
            return {"x": self.x, "y": self.y, "z": self.z}[axis]
        else:
            return {"i": self.x, "j": self.y, "k": self.z}[axis]


    def __delattr__(self, name):
        """prevents deletion of Vector attrs"""

        if not hasattr(self, name):
            raise AttributeError(f"'Vector' object has no attr {name !r}")
        else:
            raise AttributeError(f"cannot delete 'Vector' attribute {name !r}")


    def __contains__(self, item, /):
        """defines membership property for Vector
        returns True if item is a component-vector of self, False otherwise"""

        if not isinstance(item, Vector):
            raise TypeError(" ".join((
                "'in <Vector>' requires left operand as 'Vector'",
                f"not {item.__class__.__name__ !r}"
            )))

        Vector.ExceptionVector(self, item)
        return item in self.componentvectors()


    def __round__(self, digits=0):
        """defines the round() method for Vector
        round each component of the point to given number of digits"""

        result = [round(Vector.components(self)[i], digits) for i in range(3)]
        return Vector.FromSequence(result)


    def __neg__(self, /):
        """defines the negative of a Vector using unary '-' operator
        -Vector(x, y, z) == Vector(-x, -y, -z)"""

        return Vector.scale(self, -1)


    def __abs__(self, /):
        """defines the abs() method for Vector
        returns the magnitude of the Vector"""

        return Vector.mod(self)


    def __eq__(self, other, /):
        """defines the equality of Vector Objects using '==' operator"""

        if type(self) is not type(other):
            return False
        else:
            return Vector.components(self) == Vector.components(other)


    def __lt__(self, other, /):
        """compares magnitudes of Vector Objects using '<' operator
        returns True if magnitude of self is less than magnitude of other"""

        return Vector.mod(self) < Vector.mod(other)


    def __gt__(self, other, /):
        """compares magnitudes of Vector Objects using '>' operator
        returns True if magnitude of self is greater than magnitude of other"""

        return Vector.mod(self) > Vector.mod(other)


    def __add__(self, other, /):
        """add Vector Objects using '+' operator
        returns the result for (self + other)"""

        v1, v2 = Vector.components(self), Vector.components(other)
        return Vector.FromSequence([v1[i] + v2[i] for i in range(3)])


    def __sub__(self, other, /):
        """subtract Vector Objects using '-' operator
        returns the result for (self - other)"""

        Vector.ExceptionVector(self, other)
        return self + (-other)


    def __mul__(self, k, /):
        """scale the components of the Vector by k using '*' operator
        equivalent to scale(Vector(x, y, z), k)"""

        return Vector.scale(self, k)

    __rmul__ = __mul__


    @classmethod
    def ExceptionVector(cls, *vectors):
        """raise Exception when objects passed to functions are not Vectors
        or when attrs of Vector Object are altered"""

        for vec in vectors:
            if not isinstance(vec, cls):
                raise TypeError(" ".join((
                    "invalid operand(s) for Vector Calculus:",
                    f"expected 'Vector' recieved {vec.__class__.__name__ !r}"
                )))
            copy = {i: vec.__dict__[i] for i in vec.__dict__ if i != "dict"}
            if vec.dict != copy:
                raise AttributeError("attrs of Vector Object have been altered")


    @classmethod
    def ExceptionNull(cls, *vectors):
        """raise Exception when Vector.null is passed to functions in which
        Vector.null is unsuported as an argument"""

        for vector in vectors:
            if not vector:
                raise ValueError("invalid Vector: 'null' for chosen operation")


    @classmethod
    def FromAngles(cls, alpha, beta, gamma, /, *, mod=1):
        """creates a Vector along the given angles with given magnitude
        (angles are in degrees taken counter-clockwise)
        may return pre-defined Vector instances if required
        𝜶, 𝜷, 𝜸 = angles subtended by Vector at the axes 'X', 'Y', 'Z'
        direction cosines: cos²𝜶 + cos²𝜷 + cos²𝜸 == 1"""

        for angle in alpha, beta, gamma:
            if not isinstance(angle, (int, float)):
                raise TypeError(" ".join((
                    "'FromAngles' expects all positional",
                    "arguments as 'int' / 'float'"
                )))
        if not isinstance(mod, (int, float)):
            raise TypeError(
                "invalid operand type for 'mod': must be 'int' / 'float'"
            )
        if mod <= 0:
            raise ValueError(
                "invalid operand for 'mod': must be positive 'int' / 'float'"
            )

        from math import cos, radians

        cosines = [cos(radians(angle)) for angle in (alpha, beta, gamma)]
        total = sum(dc**2 for dc in cosines)

        if round(total, 10) != 1:
            raise ValueError(" ".join((
                "given angles do not form direction cosines:",
                "see help(FromAngles) for help on valid angles"
            )))

        return cls.FromSequence([round(dc, 15) for dc in cosines]).scale(mod)


    @classmethod
    def FromSequence(cls, sequence, /):
        """creates a Vector from the given sequence
        the sequence must have len(sequence) == 3
        valid sequences defined here:
            • (x, y, z)
            • [x, y, z]
            • {'x': x, 'y': y, 'z': z}
            • {'i': x, 'j': y, 'k': z}"""

        if not isinstance(sequence, (dict, list, tuple)):
            raise TypeError(" ".join((
                "invalid sequence type for 'Vector':",
                "see help(FromSequence) for help on valid sequences"
            )))
        if len(sequence) != 3:
            raise ValueError(" ".join((
                "len of sequence must be 3:",
                "see help(FromSequence) for help on valid sequences"
            )))

        if isinstance(sequence, dict):
            if set(sequence.keys()) not in ({"x", "y", "z"}, {"i", "j", "k"}):
                raise KeyError(" ".join((
                    "invalid keys for 'Vector':",
                    "see help(FromSequence) for help on valid keys"
                )))

            p, q, r = sorted(sequence.keys())
            sequence = sequence[p], sequence[q], sequence[r]

        if set(sequence) == {0}:
            return cls.null

        if (sequence.count(1), sequence.count(0)) == (1, 2):
            if sequence[0] == 1:
                return cls.i
            if sequence[1] == 1:
                return cls.j
            else:
                return cls.k
        else:
            return cls(*sequence)


    @staticmethod
    def zeroresultant(*vectors):
        """returns True if the resultant of the given Vectors is Vector.null,
        False otherwise
        all Vectors add upto Vector.null ⇒ they form a closed polygon"""

        return not sum(vectors, Vector.null)


    @staticmethod
    def plot_vectors(*vectors, show_legend=True):
        """plots all given Vectors in the same plot
        show_legend is a boolean which displays legend on the plot if True"""

        if not vectors:
            return
        else:
            import matplotlib.pyplot as plt

        Vector.ExceptionVector(*vectors)

        ax = plt.axes(projection="3d")
        colors = ["red", "orange", "green", "blue", "purple"] * len(vectors)

        X = abs(max(vectors, key=lambda vec: abs(vec.x)))
        Y = abs(max(vectors, key=lambda vec: abs(vec.y)))
        Z = abs(max(vectors, key=lambda vec: abs(vec.z)))

        ax.plot3D([-X-10, X+10], [0, 0], [0, 0], color="black", linewidth=3)
        ax.plot3D([0, 0], [-Y-10, Y+10], [0, 0], color="black", linewidth=3)
        ax.plot3D([0, 0], [0, 0], [-Z-10, Z+10], color="black", linewidth=3)
        ax.plot3D(0, 0, 0, color="black", marker="o")

        for i, vector in enumerate(vectors):
            if vectors.index(vector) == i:
                ax.quiver(
                    0, 0, 0, *vector.tuple, linewidth=3, label=vector,
                    color=(colors[i] if vector else "black")
                )

        ax.set_xlabel("î")
        ax.set_ylabel("ĵ")
        ax.set_zlabel("k̂")

        if show_legend:
            ax.legend()

        plt.show()


    def plot(self, /):
        """plots the Vector on a 3D plot and displays it"""

        Vector.plot_vectors(self)


    def mod(self, /):
        """returns the magnitude (absolute value) of the Vector
        mod(Vector(x, y, z)) == √(|x|² + |y|² + |z|²)"""

        Vector.ExceptionVector(self)
        return self.magnitude


    def components(self, /):
        """returns a tuple containing rectangular components of the Vector
        components(Vector(x, y, z)) == (x, y, z)"""

        Vector.ExceptionVector(self)
        return self.tuple


    def tosequence(self, sequence, *, keys=None):
        """returns the given Vector as a dict, list or tuple of components
        if the required sequence type is 'dict', keys must be given as
        a list, set, str or tuple
        valid keys defined here:
            • ['x', 'y', 'z'] or ['i', 'j', 'k']
            • {'x', 'y', 'z'} or {'i', 'j', 'k'}
            • ('x', 'y', 'z') or ('i', 'j', 'k')
            • 'xyz' or 'ijk'"""

        vec = Vector.components(self)

        if sequence not in {dict, list, tuple}:
            raise TypeError(" ".join((
                "invalid operand type for 'sequence':",
                "must be 'type' ('dict', 'list' or 'tuple'}"
            )))

        if sequence is dict:
            if keys is None:
                raise TypeError(
                    "argument 'keys' must be given for sequence type 'dict'"
                )
            if not isinstance(keys, (list, set, str, tuple)):
                raise TypeError(" ".join((
                    "invalid operand type for 'keys':",
                    "must be 'list', 'set', 'tuple' or 'str'"
                )))
            if set(keys) not in ({"x", "y", "z"}, {"i", "j", "k"}):
                raise ValueError(" ".join((
                    "invalid keys for sequence type 'dict':",
                    "see help(tosequence) for help on valid keys"
                )))
            if set(keys) == {"x", "y", "z"}:
                return {"x": vec[0], "y": vec[1], "z": vec[2]}
            else:
                return {"i": vec[0], "j": vec[1], "k": vec[2]}
        else:
            return sequence(vec)


    def componentvectors(self, /):
        """returns a tuple containing the component Vectors of the given Vector
        componentvectors(Vector(x, y, z)) == (
            Vector(x, 0, 0), Vector(0, y, 0), Vector(0, 0, z)
        )"""

        vec = x, y, z = list(Vector.components(self))
        for i in range(3):
            vec[i] = Vector.FromSequence([0]*i + [vec[i]] + [0]*(2-i))
        return tuple(vec)


    def resolve(self, /):
        """returns a dict of rectangularly resolved components of the Vector
        resolve(Vector(x, y, z)) == {î: x, ĵ: y, k̂: z}"""

        x, y, z = Vector.components(self)
        return {Vector.i: x, Vector.j: y, Vector.k: z}


    def octant(self, /):
        """returns the octant in which the given Vector lies as 'int'
        returns NotImplemented if any component of the Point is zero
        i.e., Vector(x, y, z), where x, y, z ≠ 0
        octants are numbered as per convention:
            1. (+, +, +)      5.  (+, +, -)
            2. (-, +, +)      6.  (-, +, -)
            3. (-, -, +)      7.  (-, -, -)
            4. (+, -, +)      8.  (+, -, -)"""

        Vector.ExceptionVector(self)

        if len(self) != 3:
            return NotImplemented

        if self.z > 0:
            if self.y > 0:
                if self.x > 0:
                    return 1
                return 2

            if self.x < 0:
                return 3
            return 4

        if self.y > 0:
            if self.x > 0:
                return 5
            return 6

        if self.x < 0:
            return 7
        return 8


    def axis(self, /):
        """returns the axis on which the given Vector lies as 'int'
        returns NotImplemented if two components of the Point are not zero
        i.e., Vector(x, 0, 0), Vector(0, y, 0), Vector(0, 0, z),
        where x, y, z ≠ 0
        axes are numbered as per convention:
            1, 2, 3 = 'X', 'Y', 'Z'"""

        Vector.ExceptionVector(self)

        if len(self) != 1:
            return NotImplemented

        if not self.z:
            if not self.y:
                return 1
            return 2
        return 3


    def directioncos(self, /):
        """returns a tuple containing direction cosines of the Vector
        directioncos(FromAngles(𝜶, 𝜷, 𝜸, mod=n)) == (cos𝜶, cos𝜷, cos𝜸)
        see help(FromAngles) for help on angles & direction cosines"""

        return Vector.unit(self).tuple


    def axis_angles(self, /):
        """returns a tuple of angles (in degrees) that the Vector makes with
        the co-ordinate axes
        axis_angles(FromAngles(𝜶, 𝜷, 𝜸, mod=n)) == (𝜶, 𝜷, 𝜸)
        see help(FromAngles) for help on angles"""

        from math import acos, degrees
        return tuple(
            [round(degrees(acos(i)), 10) for i in Vector.directioncos(self)]
        )


    def dot(self, other, /):
        """performs dot product / scalar product on two Vectors and
        returns the result (scalar)
        dot(Vector(a, b, c), Vector(d, e, f)) is equivalent to
        a*d + b*e + c*f"""

        v1, v2 = Vector.components(self), Vector.components(other)
        return sum([v1[i] * v2[i] for i in range(3)])


    def cross(self, other, /):
        """performs cross product / vector product on two Vectors and
        returns the result (Vector)
        cross(Vector(a, b, c), Vector(d, e, f)) is equivalent to
        Vector((b*f - c*e), (c*d - a*f), (a*e - b*d))"""

        Vector.ExceptionVector(self, other)

        result1 = (self.y*other.z - self.z*other.y)
        result2 = (self.z*other.x - self.x*other.z)
        result3 = (self.x*other.y - self.y*other.x)

        return Vector.FromSequence([result1, result2, result3])


    def scalar_triple(self, value1, value3, /):
        """returns the result (scalar) of scalar triple product of the Vectors
        taken in order
        scalar_triple(v1, v2, v3) == dot(v1, cross(v2, v3))"""

        return Vector.dot(self, Vector.cross(value1, value3))


    def vector_triple(self, value1, value3, /):
        """returns the result (Vector) of vector triple product of the Vectors
        taken in order
        vector_triple(v1, v2, v3) == cross(v1, cross(v2, v3))"""

        return Vector.cross(self, Vector.cross(value1, value3))


    def scale(self, /, k):
        """scales the Vector by scalar k and returns the result
        scale(Vector(x, y, z), 𝝀) == Vector(𝝀x, 𝝀y, 𝝀z)"""

        Vector.ExceptionVector(self)

        if k == 1:
            return self
        if not isinstance(k, (int, float)):
            raise TypeError(" ".join((
                "invalid operand type for 'k':",
                "must be 'int' / 'float'"
            )))
        return Vector.FromSequence([comp * k for comp in self.tuple])


    def angle(self, other, /):
        """returns the angle (in degrees) between the given Vectors
        for any two Vectors v1 and v2:
            angle(v1, v2) == cos⁻¹(dot(v1, v2) / (mod(v1) * mod(v2)))
        Note: using Vector.null as either of the operands raises Exception"""

        Vector.ExceptionNull(self, other)
        from math import acos, degrees
        result = self.dot(other) / (self.magnitude * other.magnitude)
        return round(degrees(acos(round(result, 10))), 10)


    def isscaledof(self, other, /):
        """returns True if the given Vectors are scaled versions of each other,
        False otherwise
        Note: using Vector.null as either of the operands raises Exception"""

        return Vector.isparallel(self, other)


    def scalefactor(self, other, /):
        """returns the scale factor by which self is scaled to get other if the
        Vectors are scaled versions of each other, else NotImplemented"""

        if Vector.isscaledof(self, other):
            for i in range(3):
                if self.tuple[i]:
                    return other.tuple[i] / self.tuple[i]
        return NotImplemented


    def unit(self, /):
        """returns the unit Vector along the direction of the given Vector
        for a Vector: v = Vector(x, y, z)
        unit(v) == scale(v, 1/mod(v))
        Note: there is no unit Vector along Vector.null"""

        Vector.ExceptionNull(self)
        return self.scale(1 / self.magnitude)


    def inverse(self, /):
        """returns the inverse of a Vector
        for a Vector: v = Vector(x, y, z)
        inverse(v) == scale(unit(v), 1/mod(v)) == scale(v, 1/mod(v)²)
        Note: there is no inverse Vector corresponding to Vector.null"""

        return Vector.unit(self).scale(1 / self.magnitude)


    def section_internal(self, other, /, m, n):
        """returns the Vector which sections the line joining self and
        other in the ratio m : n internally
        Note: m and n must be positive Real numbers"""

        for num in m, n:
            if not isinstance(num, (int, float)):
                raise TypeError("'m' and 'n' must be positive 'int' / 'float'")
            if num <= 0:
                raise ValueError("'m' and 'n' must be positive 'int' / 'float'")

        return (Vector.scale(other, m) + Vector.scale(self, n)).scale(1 / (m+n))


    def section_external(self, other, /, m, n):
        """returns the Vector which sections the line joining self and
        other in the ratio m : n externally
        Note: m and n must be positive Real numbers
        returns NotImplemented if no such Vector exists, i.e. when m = n"""

        Vector.section_internal(self, other, m=m, n=n)
        if not (m - n):
            return NotImplemented
        else:
            return (other.scale(m) - self.scale(n)).scale(1 / (m-n))


    def isunit(self, /):
        """returns True if the given Vector is a unit Vector, False otherwise"""

        return Vector.mod(self) == 1


    def isinverse(self, other, /):
        """returns True if the given Vectors are inverses of each other,
        False otherwise"""

        Vector.ExceptionVector(self, other)
        return (self == other.inverse()) or (other == self.inverse())


    def equalmod(self, other, /):
        """returns True if the given Vectors are equal in magnitude,
        False otherwise"""

        return Vector.mod(self) == Vector.mod(other)


    def iscoplanar(self, value2, value3, /):
        """returns True if the given Vectors are co-planar, False otherwise
        Note: using Vector.null as any of the operands returns True"""

        return not Vector.scalar_triple(self, value2, value3)


    def isparallel(self, other, /):
        """returns True if the given Vectors are parallel, False otherwise
        Note: using Vector.null as either of the operands raises Exception"""

        Vector.ExceptionNull(self, other)
        return not self.cross(other)


    def isperpendicular(self, other, /):
        """returns True if the given Vectors are perpendicular, False otherwise
        Note: using Vector.null as either of the operands raises Exception"""

        Vector.ExceptionNull(self, other)
        return not self.dot(other)


    def random(*, mod=1):
        """returns a Vector with the given magnitude in a random direction
        passing argument mod as 0 returns Vector.null"""

        if not isinstance(mod, (int, float)):
            raise TypeError(
                "invalid operand type for 'mod': must be 'int' / 'float'"
            )
        if mod < 0:
            raise ValueError(
                "invalid operand for 'mod': must be positive 'int' / 'float'"
            )
        if not mod:
            return Vector.null

        from random import uniform
        result = uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)

        return Vector.FromSequence(result).unit().scale(mod)


    def transform(self, /, i, j, k):
        """returns the Linearly Transformed version of the given Vector when
        new Vectors i, j, k are chosen as the Basis Vectors
        i, j, k = Vector for new Vector.i, Vector.j, Vector.k
        Vector(x, y, z) == scale(î, x) + scale(ĵ, y) + scale(k̂, z)
        transform(Vector(x, y, z), i, j, k) is equivalent to
        scale(i, x) + scale(j, y) + scale(k, z)
        Note: using Vector.null as i, j or k raises Exception"""

        Vector.ExceptionNull(i, j, k)
        x, y, z = Vector.components(self)
        return i.scale(x) + j.scale(y) + k.scale(z)


    def shear2D(self, /):
        """performs 2-dimensional Shear Linear Transformation on the given
        Vector and returns the result
        for a Vector: v = Vector(x, y, z)
        shear2D(v) = transform(v, Vector.i, Vector(1, 1, 0), Vector.k)"""

        i, j, k = Vector.i, Vector(1, 1, 0), Vector.k
        return Vector.transform(self, i, j, k)


    def shear3D(self, /):
        """performs 3-dimensional Shear Linear Transformation on the given
        Vector and returns the result
        for a Vector: v = Vector(x, y, z)
        shear3D(v) = transform(v, Vector.i, Vector(1, 1, 1), Vector.k)"""

        i, j, k = Vector.i, Vector(1, 1, 1), Vector.k
        return Vector.transform(self, i, j, k)


    def isindependent(self, value2, value3, /):
        """returns True if the given Vectors are Linearly Independent,
        False otherwise
        isindependent(v1, v2, v3) == (scalar_triple(v1, v2, v3) != 0)"""

        return not Vector.iscoplanar(self, value1, value2)


    def rank(self, value2, value3, /):
        """returns the rank of (dimensions spanned by) three Vectors
        Note: using Vector.null as either of the operands raises Exception"""

        if Vector.isindependent(self, value2, value3):
            return 3

        p1 = self.isparallel(value2)
        p2 = value2.isparallel(value3)
        p3 = value3.isparallel(self)

        if not all({p1, p2, p3}):
            return 2
        else:
            return 1


    def rotate(self, /, *, yaw, pitch, roll):
        """rotates the Vector by the given yaw, pitch and roll angles using
        the Right-Hand Rule (angles are in degrees taken counter-clockwise)
        formally, this corresponds to an intrinsic rotation whose Tait-Bryan
        angles are yaw, pitch and roll about the Z, Y and X axes respectively"""

        x, y, z = Vector.components(self)

        for angle in yaw, pitch, roll:
            if not isinstance(angle, (int, float)):
                raise TypeError(" ".join((
                    "inalid operand type(s) for 'yaw', 'pitch' or 'roll':",
                    "must be 'int' / 'float'"
                )))

        from math import sin, cos, radians

        cA, sA = cos(radians(yaw)), sin(radians(yaw))
        cB, sB = cos(radians(pitch)), sin(radians(pitch))
        cC, sC = cos(radians(roll)), sin(radians(roll))

        X = x*cA*cB + y*(cA*sB*sC - sA*cC) + z*(cA*sB*cC + sA*sC)
        Y = x*sA*cB + y*(sA*sB*sC + cA*cC) + z*(sA*sB*cC - cA*sC)
        Z = -x*sB + y*cB*sC + z*cB*cC

        return round(Vector.FromSequence([X, Y, Z]), 10)


    def rotate_vector(self, other, /, *, phi=90):
        """rotates the Vector self phi degrees about the Vector other using
        the Right-Hand Rule. phi can be any Real Number.
        when phi > 0, the rotation will be counter-clockwise when 'other' points
        towards the observer.
        a Vector rotated about its own axis returns itself
        Note: other cannot be Vector.null"""

        Vector.ExceptionVector(self, other)

        if not isinstance(phi, (int, float)):
            raise TypeError(
                "invalid operand type 'phi': must be 'int' / 'float'"
            )

        from math import sin, cos, radians
        phi = radians(phi)

        other = other.unit()
        result1 = other.scale(self.dot(other))
        result2 = other.vector_triple(other, self).scale(-cos(phi))
        result3 = other.cross(self).scale(sin(phi))

        return round(sum([result1, result2, result3], Vector.null), 10)


    def rotate_axis(self, /, axis, *, phi=90):
        """rotates the Vector by phi degrees about positive direction of the
        given axis using the Right-Hand Rule. phi can be any Real Number.
        when phi > 0, the rotation will be counter-clockwise when the positive
        direction of axis of rotation points towards the observer.
        a Vector rotated about its own axis returns itself
        axes defined here:
          'x' == 'i' = X-axis
          'y' == 'j' = Y-axis
          'z' == 'k' = Z-axis"""

        Vector.ExceptionVector(self)

        if not isinstance(axis, str):
            raise TypeError("invalid operand type for 'axis': must be 'str'")

        if axis not in {"x", "y", "z", "i", "j", "k"}:
            raise ValueError(" ".join((
                "invalid operand for 'axis':",
                "see help(rotate_axis) for help on valid axes"
            )))

        X, Y = {"x", "i"}, {"y", "j"}

        return self.rotate_vector(
            Vector.i if axis in X else Vector.j if axis in Y else Vector.k,
            phi=phi
        )


Vector.i = Vector(1, 0, 0)
Vector.j = Vector(0, 1, 0)
Vector.k = Vector(0, 0, 1)
Vector.null = Vector(0, 0, 0)

__name__ = "pyvectors"
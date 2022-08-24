from math import ceil, floor


class Vector2D:
    def __init__(self, x: int | float, y: int | float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(self.x + value, self.y + value)

        return Vector2D(self.x + value.x, self.y + value.y)

    def __radd__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(value + self.x, value + self.y)

        return Vector2D(value.x + self.x, value.y + self.y)

    def __iadd__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            self.x += value
            self.y += value
            return self

        self.x += value.x
        self.y += value.y
        return self

    def __sub__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(self.x - value, self.y - value)

        return Vector2D(self.x - value.x, self.y - value.y)

    def __rsub__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(value - self.x, value - self.y)

        return Vector2D(value.x - self.x, value.y - self.y)

    def __isub__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            self.x -= value
            self.y -= value
            return self

        self.x -= value.x
        self.y -= value.y
        return self

    def __mul__(self, value: "Vector2D | int | float"):
        if isinstance(value, (int, float)):
            return Vector2D(self.x * value, self.y * value)

        return Vector2D(self.x * value.x, self.y * value.y)

    def __rmul__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(value * self.x, value * self.y)

        return Vector2D(value.x * self.x, value.y * self.y)

    def __imul__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            self.x *= value
            self.y *= value
            return self

        self.x *= value.x
        self.y *= value.y
        return self

    def __truediv__(self, value: "Vector2D | int | float"):
        if isinstance(value, (int, float)):
            return Vector2D(self.x / value, self.y / value)

        return Vector2D(self.x / value.x, self.y / value.y)

    def __rtruediv__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            return Vector2D(value / self.x, value / self.y)

        return Vector2D(value.x / self.x, value.y / self.y)

    def __itruediv__(self, value: "Vector2D | int | float") -> "Vector2D":
        if isinstance(value, (int, float)):
            self.x /= value
            self.y /= value
            return self

        self.x /= value.x
        self.y /= value.y
        return self

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Vector2D):
            return False

        if self.x == value.x and self.y == value.y:
            return True

        return False

    def __round__(self) -> "Vector2D":
        return Vector2D(round(self.x), round(self.y))

    def __floor__(self) -> "Vector2D":
        return Vector2D(floor(self.x), floor(self.y))

    def __ceil__(self) -> "Vector2D":
        return Vector2D(ceil(self.x), ceil(self.y))

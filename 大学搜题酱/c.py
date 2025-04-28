import math
from _decimal import ROUND_HALF_EVEN
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_UP, ROUND_DOWN, ROUND_CEILING, ROUND_FLOOR

class ToDoubleRounder:
    def __init__(self):
        pass

    def minus(self, x, x2):
        raise NotImplementedError("minus method must be implemented in subclass")

    def roundToDoubleArbitrarily(self, x):
        raise NotImplementedError("roundToDoubleArbitrarily method must be implemented in subclass")

    def sign(self, x):
        raise NotImplementedError("sign method must be implemented in subclass")

    def toX(self, d, roundingMode):
        raise NotImplementedError("toX method must be implemented in subclass")

    def roundToDouble(self, x, roundingMode):
        if x is None:
            raise ValueError("x must not be None")
        if roundingMode is None:
            raise ValueError("mode must not be None")

        roundToDoubleArbitrarily = self.roundToDoubleArbitrarily(x)
        if math.isinf(roundToDoubleArbitrarily):
            switch_map = {
                ROUND_DOWN: 1,
                ROUND_HALF_UP: 2,
                ROUND_HALF_DOWN: 3,
                ROUND_UP: 4,
                ROUND_FLOOR: 5,
                ROUND_CEILING: 6,
                ROUND_HALF_EVEN: 7,
            }
            mode_value = switch_map.get(roundingMode, 0)

            if mode_value in [1, 2, 3, 4]:
                return math.copysign(math.inf, roundToDoubleArbitrarily)
            elif mode_value == 5:
                return math.inf if roundToDoubleArbitrarily == float('inf') else -float('inf')
            elif mode_value == 6:
                return float('inf') if roundToDoubleArbitrarily == float('inf') else -1.7976931348623157e308
            elif mode_value == 7:
                return roundToDoubleArbitrarily
            else:
                raise ArithmeticError(f"{x} cannot be represented precisely as a double")
        else:
            x3 = self.toX(roundToDoubleArbitrarily, ROUND_DOWN)
            compare = self._compare(x, x3)

            switch_map = {
                ROUND_DOWN: 1,
                ROUND_HALF_UP: 2,
                ROUND_HALF_DOWN: 3,
                ROUND_UP: 4,
                ROUND_FLOOR: 5,
                ROUND_CEILING: 6,
                ROUND_HALF_EVEN: 7,
            }
            mode_value = switch_map.get(roundingMode, 0)

            if mode_value == 1:
                return roundToDoubleArbitrarily if (self.sign(x) >= 0 and compare >= 0) or (self.sign(x) < 0 and compare <= 0) else math.nextafter(roundToDoubleArbitrarily, -math.inf) if self.sign(x) >= 0 else math.nextafter(roundToDoubleArbitrarily, math.inf)
            elif mode_value in [2, 3, 4]:
                if compare >= 0:
                    d = math.nextafter(roundToDoubleArbitrarily, math.inf)
                    if math.isinf(d):
                        return roundToDoubleArbitrarily
                    x2 = self.toX(d, ROUND_UP)
                else:
                    next_down = math.nextafter(roundToDoubleArbitrarily, -math.inf)
                    if math.isinf(next_down):
                        return roundToDoubleArbitrarily
                    x4 = self.toX(next_down, ROUND_DOWN)
                    x2 = x3
                    x3 = x4
                    d = roundToDoubleArbitrarily
                    roundToDoubleArbitrarily = next_down

                compare_diff = self._compare(self.minus(x, x3), self.minus(x2, x))
                if compare_diff < 0:
                    return roundToDoubleArbitrarily
                elif compare_diff > 0:
                    return d
                else:
                    if mode_value == 2:
                        return roundToDoubleArbitrarily if (math.frexp(roundToDoubleArbitrarily)[0] & 1) == 0 else d
                    elif mode_value == 3:
                        return roundToDoubleArbitrarily if self.sign(x) >= 0 else d
                    elif mode_value == 4:
                        return d if self.sign(x) >= 0 else roundToDoubleArbitrarily
                    else:
                        raise AssertionError("impossible")
            elif mode_value == 5:
                return roundToDoubleArbitrarily if compare >= 0 else math.nextafter(roundToDoubleArbitrarily, -math.inf)
            elif mode_value == 6:
                return roundToDoubleArbitrarily if compare <= 0 else math.nextafter(roundToDoubleArbitrarily, math.inf)
            elif mode_value == 7:
                return roundToDoubleArbitrarily if (self.sign(x) >= 0 and compare <= 0) or (self.sign(x) < 0 and compare >= 0) else math.nextafter(roundToDoubleArbitrarily, math.inf) if self.sign(x) >= 0 else math.nextafter(roundToDoubleArbitrarily, -math.inf)
            else:
                raise AssertionError("impossible")

    def _compare(self, x, y):
        if x == y:
            return 0
        elif x > y:
            return 1
        else:
            return -1

    def minus(self, x, x2):
        raise NotImplementedError

    def roundToDoubleArbitrarily(self, x):
        raise NotImplementedError

    def sign(self, x):
        raise NotImplementedError

    def toX(self, d, roundingMode):
        raise NotImplementedError


class ConcreteToDoubleRounder(ToDoubleRounder):
    def minus(self, x, x2):
        return x - x2

    def roundToDoubleArbitrarily(self, x):
        return round(x)

    def sign(self, x):
        return 1 if x > 0 else -1 if x < 0 else 0

    def toX(self, d, roundingMode):
        return d


# 示例使用
rounder = ConcreteToDoubleRounder()
result = rounder.roundToDouble(3.14159, ROUND_HALF_UP)
print(result)
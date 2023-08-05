import cx_autopos

class Position:
    def __init__(self, x, y, z):
        self.__position = cx_autopos.Position(x, y, z)

    @property
    def x(self):
        return self.__position.x

    @property
    def y(self):
        return self.__position.y

    @property
    def z(self):
        return self.__position.z

    def __repr__(self):
        return self.__position.__repr__()

class AutoPos:
    def __init__(self, anchor_cnt):
        self.__autopos = cx_autopos.AutoPos(anchor_cnt)

    def get_position_estimates(self):
        return self.__autopos.get_position_estimates()

    def compute(self, measurements):
        self.__autopos.compute(measurements)

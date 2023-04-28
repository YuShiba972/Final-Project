"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""


class Point:
    def __init__(self, battery=0, charge=0.5, consume=0, color=None, name='', location=None):
        if location is None:
            location = []
        if color is None:
            color = [0, 0, 0]
        self.name = name
        self.location = location
        self.battery = battery
        self.charge = charge
        self.consume = consume
        self.color = color


if __name__ == "__main__":
    A = Point(name='A', location=[0, 0], color=[255, 0, 0], charge=0.3)
    B = Point(name='B', location=[4, 9], color=[0, 255, 0], charge=0.3)
    C = Point(name='C', location=[16, 10], color=[0, 0, 255], charge=0.3)
    D = Point(name='D', location=[10, 11], color=[255, 255, 0], charge=0.3)
    points_list = [A, B, C, D]
    points = list(map(lambda x: x.location, points_list))
    print(points)

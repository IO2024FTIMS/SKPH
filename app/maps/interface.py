from dataClasses import (
    DistPoint,
    PickupPoint,
    ReliefArea,
    Coordinates,
    DangerArea,
)

from datetime import datetime

dist_point = DistPoint(
    51.747186, 19.453107, "Super punkt", ["mądrość, wiedza"]
)
pickup_point = PickupPoint(
    51.744591, 19.452547, "Punkt odbioru", "dzieci", datetime.now(), 90
)

naszaStrefa: list[Coordinates] = [
    Coordinates(51.747241, 19.452640),
    Coordinates(51.747041, 19.452761),
    Coordinates(51.747195, 19.454950),
    Coordinates(51.747424, 19.454926),
]

nienaszaStrefa: list[Coordinates] = [
    Coordinates(51.752518, 19.452965),
    Coordinates(51.752720, 19.454963),
    Coordinates(51.753832, 19.454722),
    Coordinates(51.753684, 19.452624),
]

relief_area = ReliefArea(
    "Strefa pomocy", naszaStrefa, "Aktywna", ["kable", "ekrany"]
)
danger_area = ReliefArea(
    "Strefa krzywdy", naszaStrefa, "Aktywna", ["kable", "ekrany", "dante"]
)


def squareQuery(p1: Coordinates, p2: Coordinates, test=False) -> list[
    list[DistPoint],
    list[PickupPoint],
    list[ReliefArea],
    list[DangerArea],
]:
    if test:
        return [[dist_point], [pickup_point], [relief_area], [danger_area]]

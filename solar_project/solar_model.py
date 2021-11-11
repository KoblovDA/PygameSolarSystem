# coding: utf-8
# license: GPLv3
import math
import time
import numpy as np
import matplotlib.pyplot as plt

from solar_project.solar_main import time_scale

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""
counter = 0


class DataController:
    def __init__(self):
        self.distance, self.speed, self.t = np.array([]), np.array([]), np.array([])

    def update(self, upd_distance, upd_speed, upd_t):
        self.distance = np.append(self.distance, upd_distance)
        self.speed = np.append(self.speed, upd_speed)
        self.t = np.append(self.t, upd_t)

    def plots(self):
        plt.plot(self.t, self.speed)
        plt.legend("Зависимость скорости от времени")
        plt.savefig("task1.png")
        plt.clf()
        plt.plot(self.t, self.distance)
        plt.legend("Зависимость расстояния от времени")
        plt.savefig("task2.png")
        plt.clf()
        plt.plot(self.distance, self.speed)
        plt.legend("Зависимость скорости от расстояния")
        plt.savefig("task3.png")


new_data = DataController()


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        r = max(r, body.R + obj.R)  # обработка аномалий при прохождении одного тела сквозь другое
        body.Fx += -gravitational_constant * obj.m * body.m * (body.x - obj.x) / r ** 3
        body.Fy += -gravitational_constant * obj.m * body.m * (body.y - obj.y) / r ** 3


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    ax = body.Fx / body.m
    body.x += body.Vx * dt
    body.Vx += ax * dt
    ay = body.Fy / body.m
    body.y += body.Vy * dt
    body.Vy += ay * dt


def data_function(body):
    global counter
    distance = math.sqrt(body.x ** 2 + body.y ** 2)
    speed = math.sqrt(body.Vx ** 2 + body.Vy ** 2)
    t = time.perf_counter() / time_scale
    new_data.update(distance, speed, t)
    counter += 1
    if (counter % 1000 == 1):
        new_data.plots()


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)
    if len(space_objects) != 0:
        data_function(space_objects[0])


if __name__ == "__main__":
    print("This module is not for direct call!")

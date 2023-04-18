from typing import Final
import pygame as pg
import Constants

# Lets define some constants for move speeds, we can define all of these in MM per second
PLANE_SPEED_MAX: Final[int] = 100
PLANE_SPEED_MIN: Final[int] = 80
VERTICAL_SPEED_MAX: Final[int] = 20
VERTICAL_SPEED_MIN: Final[int] = 10

PLANE_ACCELERATION: Final[int] = 10


def calculateSpeed(target: int, currentStep: int, startingStep: int,
                   maxSpeed: int, minSpeed: int):
    velocity = 0
    distance_to_go = abs(target - currentStep)
    toal_distance = abs(target - startingStep)
    percentage = distance_to_go / toal_distance
    # Now we can calculate the speed we need to travel at
    if percentage < .25:
        velocity = (maxSpeed - minSpeed) * (percentage / .25) + minSpeed
    elif percentage > .75:
        velocity = (maxSpeed - minSpeed) * ((1 - percentage) / .25) + minSpeed
    else:
        velocity = maxSpeed

    if target < currentStep:
        velocity = -velocity
    return velocity


class Grabber:

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.target_x = None
        self.target_y = None

        self.starting_x = None
        self.starting_y = None

        self.target_z = None
        self.starting_z = None

        self.ticks = 0

    def set_target(self, x: int, y: int):
        self.target_x = x
        self.target_y = y
        self.starting_x = self.x
        self.starting_y = self.y

    def set_vertical_target(self, z: int):
        self.target_z = z
        self.starting_z = self.z

    def update(self):
        self.ticks += 1
        self.x += self.vx / 60
        self.y += self.vy / 60
        self.z += self.vz / 60

        if self.target_x is not None:
            if abs(self.x - self.target_x) < 2:
                self.vx = 0
                self.x = self.target_x
                self.target_x = None
            else:
                self.vx = calculateSpeed(self.target_x, self.x,
                                         self.starting_x, PLANE_SPEED_MAX,
                                         PLANE_SPEED_MIN)

        if self.target_y is not None:
            if abs(self.y - self.target_y) < 2:
                self.vy = 0
                self.y = self.target_y
                self.target_y = None
            else:
                self.vy = calculateSpeed(self.target_y, self.y,
                                         self.starting_y, PLANE_SPEED_MAX,
                                         PLANE_SPEED_MIN)

        if self.target_z is not None:
            if abs(self.z - self.target_z) < 2:
                self.vz = 0
                self.z = self.target_z
                self.target_z = None
                print("Done with Z")
            else:
                self.vz = calculateSpeed(self.target_z, self.z,
                                         self.starting_z, VERTICAL_SPEED_MAX,
                                         VERTICAL_SPEED_MIN)

    def in_motion(self):
        return not (self.vz == 0 and self.vx == 0 and self.vy == 0)
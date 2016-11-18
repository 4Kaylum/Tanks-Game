# Import the main library to use for the game
import pygame
import math

class Controller:

    def __init__(self, number):
        if pygame.joystick.get_count() < number:
            raise Exception('There are not enough controllers connected.')

        self.joystick = pygame.joystick.Joystick(number - 1)
        self.joystick.init()

    def giveAxies(self):
        deadzoneTrig = 1
        deadzoneAxis = 0
        a = int(self.joystick.get_axis(0) * 100)
        a = a if abs(a) > deadzoneAxis else 0
        b = int(self.joystick.get_axis(1) * 100)
        b = b if abs(b) > deadzoneAxis else 0
        c = int(self.joystick.get_axis(2) * 100)
        c = c if abs(c) > deadzoneTrig else 0
        return [a, b], c

    def giveRotation(self):
        deadzone = 0
        a = int(self.joystick.get_axis(0) * 100)
        xAx = a if abs(a) > deadzone else 0
        b = int(self.joystick.get_axis(1) * 100)
        yAx = b if abs(b) > deadzone else 0

        try:
            r = abs(int(math.degrees(math.atan(xAx/yAx))))
            print (r)
        except ZeroDivisionError:
            r = -1
        print(yAx)

        if xAx < 0 and yAx < 0: # top left
            r = r 
        elif xAx < 0 and yAx > 0: # bottom left
            r = 180 - r 
        elif xAx > 0 and yAx > 0: # bottom right
            r = 180 + r 
        elif xAx > 0 and yAx < 0: # top right
            r = 360 - r

        if r == -1:
            r = 90 if xAx < 0 else r
            r = 180 if yAx < 0 else r
            r = 270 if xAx > 0 else r
            r = 180 if yAx > 0 else r
            r = 0 if [xAx, yAx] == [0, 0] else r

        if r == 0:
            return 180 if yAx > 0 else 0

        return r

    def giveRotationalMovement(self):
        pass



if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    i = Controller(1)
    while True:
        pygame.event.pump()
        i.giveAxies()
        clock.tick(30)
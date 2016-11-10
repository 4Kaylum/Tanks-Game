# Import the main library to use for the game
import pygame

class Controller:

    def __init__(self, number):
        if pygame.joystick.get_count() < number:
            raise Exception('There are not enough controllers connected.')

        self.joystick = pygame.joystick.Joystick(number - 1)
        self.joystick.init()

    def giveAxies(self):
        deadzone = 10
        a = int(self.joystick.get_axis(0) * 100)
        a = a if abs(a) > deadzone else 0
        b = int(self.joystick.get_axis(1) * -100)
        b = b if abs(b) > deadzone else 0
        c = int(self.joystick.get_axis(2) * 100)
        c = c if abs(c) > deadzone else 0
        return [a, b], c

    def giveRotation(self):
        deadzone = 10
        a = int(self.joystick.get_axis(0) * 100)
        xAx = a if abs(a) > deadzone else 0
        b = int(self.joystick.get_axis(1) * -100)
        yAx = b if abs(b) > deadzone else 0

        try:
            a = int(math.degrees(math.atan(xAx/yAx)))
            # print(xAx, yAx)
        except:
            a = 0

        if xAx >= 0 and yAx < 0:
            a = 90 - (90 + a)
        elif xAx >= 0 and yAx > 0:
            a = 90 + (90 - a)
        elif xAx <= 0 and yAx > 0:
            a = 180 - a
        elif xAx <= 0 and yAx < 0:
            a = 270 + (90 - a)

        if xAx == 0 and yAx < 0:
            a = 0
        elif xAx == 0 and yAx > 0:
            a = 180
        elif xAx > 0 and yAx == 0:
            a = 90
        elif xAx < 0 and yAx == 0:
            a = 270

        return -a


if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    i = Controller(1)
    while True:
        pygame.event.pump()
        i.giveAxies()
        clock.tick(30)
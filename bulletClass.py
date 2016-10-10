import pygame
from wallClass import *

class Bullet(pygame.sprite.Sprite):

	def __init__(self, parent):
		super().__init__()

		self.direction = parent.direction
		self.image = Wall(
			topLeft=[parent.rect.x, parent.rect.y],
			dimensions=[10, 10],
			colour=[0, 0, 0])
		self.rect = self.image.get_rect()

		self.transform = [0, 0]
		if parent.direction ==  0:
			self.transform = [0, -5]
		elif parent.direction == 1:
			self.transform = [-5, 0]
		elif parent.direction == 2:
			self.transform = [0, 5]
		elif parent.direction == 3:
			self.transform = [5, 0]

	def tick(self):
		self.rect.x += self.transform[0]
		self.rect.y += self.transform[1]
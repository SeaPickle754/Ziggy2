import pyglet
import random

import math
def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

images = {
	"slimeMain":"enemies\\slime1.png",
	"zombieDown":"enemies\\zombie1.png",
	"zombieRight":"enemies\\zombie2.png",
	"zombieLeft":"enemies\\zombie3.png",
	"zombieUp":"enemies\\zombie4.png",
	"dzombieDown":"enemies\\zombie1damage.png",
	"dzombieRight":"enemies\\zombie2damage.png",
	"dzombieLeft":"enemies\\zombie3damage.png",
	"dzombieUp":"enemies\\zombie4damage.png",
	"slimeDamage":"enemies\\slime2.png",
}
tracking_distance = 300

class Slime(pyglet.sprite.Sprite):
	def __init__(self, player, batch):
		self.textures = {
		"main":pyglet.image.load(images["slimeMain"]),
		"damage":pyglet.image.load(images["slimeDamage"]),
		}
		super().__init__(list(self.textures.values())[0], batch = batch)
		self.player = player
		self.x = random.randint(0, 380)
		self.y = random.randint(0, 380)
		self.type = 0
		self.health = 2
		self.hurt = 0
	
	def update(self):
		if not self.hurt:
			if distance((self.player.x, self.player.y), (self.x, self.y)) <= tracking_distance and\
				distance((self.player.x, self.player.y), (self.x, self.y)) >= 42.5:
				if self.player.x < self.x:
					self.x -= 30
					
				if self.player.x > self.x:
					self.x += 30
					
				if self.player.y < self.y:
					self.y -= 30
					
				if self.player.y > self.y:
					self.y += 30
				
			else:
				self.x = self.player.x
				self.y = self.player.y
		
		else:
			self.image = self.textures["damage"]

			
class Zombie(pyglet.sprite.Sprite):
	def __init__(self, player, batch):
		self.textures = {
			
			"up":pyglet.image.load(images["zombieUp"]),
			"dup":pyglet.image.load(images["dzombieUp"]),
		}
		super().__init__(self.textures["up"], batch = batch)
		self.player = player
		self.x = random.randint(0, 380)
		self.y = random.randint(0, 380)
		self.type = 1
		self.health = 5
		self.hurt = 0
	
	def update(self):
		if not self.hurt:
			if distance((self.player.x, self.player.y), (self.x, self.y)) <= tracking_distance:
				if self.player.x < self.x:
					self.x -= 1
				if self.player.x > self.x:
					self.x += 1
				if self.player.y < self.y:
					self.y -= 1
				if self.player.y > self.y:
					self.y += 1
		else:
			self.image = self.textures["dup"]


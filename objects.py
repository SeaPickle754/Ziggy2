import pyglet
import dialogLoader
import random

class Tile(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 0
class nonPassableTile(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	# Cannot be passed through by the player
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 1

class slowDownTile(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	# Cannot be passed through by the player
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 4

class RoomChange(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 2

class Item(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	#=========================
	def __init__(self, texture, x, y, ID, batch):
		super().__init__(pyglet.image.load(texture), x = x, y = y, batch=batch)
		self.id = ID
	
	def on_player_pickup(self, player):
		if self.id == 1:
			player.coins += 1

class Store(pyglet.sprite.Sprite):
	#=========================
	#gets dialog when e pressed.
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 3
		self.storeType = random.randint(1,2)
	
	def get_dialog(self):
		return dialogLoader.load_dialog(self.storeType)
	
	def doTransaction(self, player):
		if self.storeType == 1:
			if player.coins <= 0:
				return
			player.coins -= 1
			player.health = 5
		if self.storeType == 2:
			return
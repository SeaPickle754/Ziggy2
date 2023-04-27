import pyglet
import dialogLoader
import dialog
import random

class Tile(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(pyglet.image.load(texture), x = x*40, y = y*40, batch=batch)
		self.type = 0
class nonPassableTile(Tile):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	# Cannot be passed through by the player
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(texture, x, y, batch=batch)
		self.type = 1

class slowDownTile(Tile):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	# Cannot be passed through by the player
	# See Tile class
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(texture, x, y, batch=batch)
		self.type = 4

class RoomChange(Tile):
	#=========================
	# Rigid basis of the world. Are placed
	# on a ten by ten grid, 40 pixels apart from each other
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(texture, x, y, batch=batch)
		self.type = 2

class Item(pyglet.sprite.Sprite):
	#=========================
	# Rigid basis of the world. Are placed as
	# An item. Can be placed anywhere.
	# Params: texture: file path
	# x: x, y: y,
	# ID: number for the type of item
	# batch: batch
	#=========================
	def __init__(self, texture, x, y, ID, batch):
		super().__init__(pyglet.image.load(texture), x, y, batch=batch)
		self.id = ID
	
	def on_player_pickup(self, player):
		if self.id == 1:
			player.coins += 1

class Store(Tile):
	#=========================
	#gets dialog when e pressed.
	#=========================
	def __init__(self, texture, x, y, batch):
		super().__init__(texture, x, y, batch=batch)
		self.type = 3
		self.storeType = random.randint(0,1)
	
	def get_dialog(self):
		return dialogLoader.load_dialog(self.storeType)
	
	def doTransaction(self, player):
		if self.storeType == 1:
			if player.coins <= 0:
				return dialog.DialogBox(dialogLoader.load_dialog(3))
			player.coins -= 1
			player.health = 5
			return 0
		if self.storeType == 0:
			return 0


class Sign(Tile):
	#=========================
	#gets dialog when e pressed.
	#=========================
	def __init__(self, texture, x, y, batch, room):
		super().__init__(texture, x, y, batch=batch)
		self.type = 3
		self.room = room
	
	def get_dialog(self):
		return dialogLoader.load_dialog(self.room)
	
	def doTransaction(self, player):
		return

class MessageHandler:
	def __init__(self):
		self.type = -1
	def doTransaction(self, player):
		return
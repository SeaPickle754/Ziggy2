import pyglet
import random
# sound
import pygame.mixer as pm
from math import sqrt
import objects
import player
import dialogLoader
import room_loader
import enemy
from dialog import DialogBox
from dialogLoader import load_dialog

tilePaths={
	"grass":"tiles\\grass.png",
	"tree":"tiles\\tree.png",
	"sand":"tiles\\sand.png",
	"stone":"tiles\\stone.png",
	"wall":"tiles\\stonewall.png",
	"vineTree":"tiles\\vtree.png",
	"water":"tiles\\water.png",
	"background":"misc\\play.mp3",
	"store":"tiles\\store.png",
	"stairs":"tiles\\stairs.png",
	"start":"misc\\start.png",
	"mud":"tiles\\dirt.png",
	"sign":"tiles\\sign.png",
}

MUD_SLOW = 100


class Game(pyglet.window.Window):
	def __init__(self, height, width, caption):
		super().__init__(height, width, caption = caption)
		self.tileArray = room_loader.load(1)
		
		self.batch, self.group = pyglet.graphics.Batch(), pyglet.graphics.OrderedGroup(0)
		self.start = pyglet.image.load(tilePaths["start"])
		self.tiles, self.enemies, self.pastFps = [],[], 0
		self.messageHandler = objects.MessageHandler()
		self.dialogOpen, self.nextRoom, self.muted = False, 2, True
		pm.init()
		pyglet.gl.glClearColor(0.2431, 0.2117, 0.2235, 1)
		pm.music.load(tilePaths["background"])
		if(not self.muted):
			pm.music.play(-1)
		self.entityBatch = pyglet.graphics.Batch()
		self.player = player.Player(0, 0, self.batch)
		self.player.group = self.group
		room_loader.batch = self.entityBatch
		self.storeInteract = False
		self.items = []
		self.run_room()
		for i in range(0, 3):
			self.items.append(objects.Item("misc\\coin.png", random.randint(0, 368), random.randint(0, 368), 1, batch = self.entityBatch))
			self.items[-1].group = self.group
		self.dialog = DialogBox(load_dialog(1))
		for i in range(0, 3):
			if random.randint(0, 1):
				self.enemies.append(enemy.Slime(self.player, self.entityBatch))
				self.enemies[-1].group = self.group
				# while it is too close to the player regenerate it
				while self.distance(self.player, self.enemies[-1]) < 240:
					del self.enemies[-1]
					self.enemies.append(enemy.Slime(self.player, self.entityBatch))
					self.enemies[-1].group = self.group
			else:
				self.enemies.append(enemy.Zombie(self.player, self.entityBatch))
				self.enemies[-1].group = self.group
				# while it is too close to the player regenerate it
				while self.distance(self.player, self.enemies[-1]) < 240:
					del self.enemies[-1]
					self.enemies.append(enemy.Zombie(self.player, self.entityBatch))
					self.enemies[-1].group = self.group
		self.game_active = False
	def toggle_game_active(self):
		self.game_active = not self.game_active
	def run_room(self):
		self.init_tiles()
	def init_tiles(self):
		self.tiles=list()
		self.tileArray.reverse()
		for y in range(len(self.tileArray)):
			self.tiles.append([])
			for x in range(len(self.tileArray[y])):
				j = self.tileArray[y][x]
				if j == 0:
					self.tiles[y].append(objects.Tile(tilePaths["grass"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 1:
					self.tiles[y].append(objects.nonPassableTile(tilePaths["tree"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 2:
					self.tiles[y].append(objects.RoomChange(tilePaths["tree"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 3:
					self.tiles[y].append(objects.Tile(tilePaths["sand"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 4:
					self.tiles[y].append(objects.Tile(tilePaths["stone"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 5:
					self.tiles[y].append(objects.nonPassableTile(tilePaths["wall"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 6:
					self.tiles[y].append(objects.nonPassableTile(tilePaths["vineTree"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 7:
					self.tiles[y].append(objects.RoomChange(tilePaths["sand"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 8:
					self.tiles[y].append(objects.nonPassableTile(tilePaths["water"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 9:
					self.tiles[y].append(objects.Store(tilePaths["store"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 10:
					self.tiles[y].append(objects.Store(tilePaths["stairs"], x, y, self.batch))
					self.tiles[y][-1].group = self.group
				elif j == 11:
					self.tiles[y].append((objects.slowDownTile(tilePaths["mud"], x, y, self.batch)))
					self.tiles[y][-1].group=self.group
				
				elif j == 12:
					self.tiles[y].append(objects.Sign(tilePaths["sign"], x, y, self.batch, self.nextRoom))
					self.tiles[y][-1].group = self.group

		#self.tiles[9].append(objects.MessageHandler())
		del self.tileArray
		return self.tiles
				
	def draw_text(self):

		self.label = pyglet.text.Label(f"Coins: {self.player.coins}",
							font_name='Ariel',
							font_size=12,
							x=20, y = 430,
							anchor_x='left') 
		self.label.draw()
		self.label.text = f"Health: {self.player.health}"
		self.label.y = 410
		self.label.draw()
		self.label.text = f"FPS {int(pyglet.clock.get_fps())}"
		self.label.y = 430
		self.label.x = 100
		self.label.draw()
	def on_key_press(self,symbol, modifiers):
		if self.game_active:
			if symbol == pyglet.window.key.UP:
				self.player.change_direction("up")
				self.player.movement["up"] = True
				
			if symbol == pyglet.window.key.DOWN:
				self.player.change_direction("down")
				self.player.movement["down"] = True
			if symbol == pyglet.window.key.RIGHT:
				self.player.change_direction("right")
				self.player.movement["right"] = True
			if symbol == pyglet.window.key.LEFT:
				self.player.change_direction("left")
				self.player.movement["left"] = True
			if symbol == pyglet.window.key.SPACE:
				self.player.damage = round(pyglet.clock.get_fps()) // 2
			if symbol == pyglet.window.key.R:
				self.dialogOpen = False
			if symbol == pyglet.window.key.E:
				if self.dialogOpen:
					dialog = self.storeInteract.doTransaction(self.player) 
					if dialog == 0:
						self.dialogOpen = False
						self.dialog = -1
					else:
						self.dialog = dialog
		else:
			if symbol == pyglet.window.key.P:
				self.toggle_game_active()
	def on_key_release(self, symbol, modifiers):
		if symbol == pyglet.window.key.UP:
			self.player.movement["up"] = False
		if symbol == pyglet.window.key.DOWN:
			self.player.movement["down"] = False
		if symbol == pyglet.window.key.RIGHT:
			self.player.movement["right"] = False
		if symbol == pyglet.window.key.LEFT:
			self.player.movement["left"] = False
			
		

	def on_draw(self):
		if self.game_active:
			self.clear()
			self.batch.draw()
			self.player.draw()
			self.entityBatch.draw()
			if self.dialogOpen:
				self.dialog.draw()
		self.draw_text()
		if not self.game_active:
			self.start.blit(0, 0)


	def collide(self, a, b):
		if a.y + a.height < b.y:
			return False
		elif a.y > b.y + b.height:
			return False
		elif a.x + a.width < b.x:
			return False
		elif a.x > b.x + b.width:
			return False
		return True

	def restart(self):
		self.tileArray = room_loader.load(1)
		self.tiles = []
		self.items = []
		self.enemies = list()
		self.player = player.Player(0, 0, self.batch)
		self.init_tiles()
		self.objects = set()
		for i in range(0, 3):
			if random.randint(0, 1):
				self.enemies.append(enemy.Slime(self.player, self.entityBatch))
			else:
				self.enemies.append(enemy.Zombie(self.player, self.entityBatch))
		self.nextRoom = 2
		for i in range(0, 3):
			self.items.append(objects.Item("misc\\coin.png", random.randint(0, 368), random.randint(0, 368), 1, self.entityBatch))
	def distance(self, a, b):
		return sqrt((a.x-b.x)**2+(a.y-b.y)**2)
	def update(self, dt):
		# dont update if not active
		if not self.game_active:
			return
		if self.dialogOpen:
			return
		# before player coords
		preX = self.player.x
		preY = self.player.y
		self.player.update(dt)
		# loop through enemies
		# if continuously moving, update it
		# then deincrement timer if its hurt
		# if the timer runs out restore old image and continue in the loop
		# If player is attacking, deal damage 
		# If touching player, deal damage
		for i in self.enemies:
			if i.type == 1:
				i.update()
			if i.hurt:
				i.hurt -= 1
				if i.hurt == 0:
					i.image = list(i.textures.values())[0]
					continue
			if self.distance(self.player, i) < 100:
				if self.player.damage:
					if self.collide(self.player, i):
						i.health -= self.player.strength
						i.hurt = 20
						i.x = random.randint(0, 255)
						i.y = random.randint(0, 255)
						if i.health <= 0:
							self.enemies.remove(i)
						continue
				if(self.collide(self.player, i)):
						self.player.health -= 1
						self.enemies.remove(i)
						self.player.taking_damage = 20
						if self.player.health <= 0:
							print("game over!!")
							self.storeInteract = self.messageHandler
							self.dialogOpen = True
							self.dialog = DialogBox(dialogLoader.load_dialog(-1))
							
							self.restart()
		for i in self.items:
			if self.distance(i, self.player) < 100:
				if self.collide(self.player, i):
					i.on_player_pickup(self.player)
					self.items.remove(i)
					return
		if self.player.damage:
			self.player.damage -= 1
			if self.player.damage == 0:
				self.player.change_image(self.player.get_current_dir())
		if self.player.taking_damage:
			self.player.taking_damage -= 1
			if self.player.taking_damage == 0:
				self.player.change_image(self.player.get_current_dir())
		if self.player.x != preX or self.player.y != preY:
				for y in self.tiles:
					if not (y[0].y < self.player.y - 80 or y[0].y > self.player.y + 80):
						for x in y:
							#if not (x.x < self.player.y - 80 or x.x > self.player.x + 80):
								if self.player.slowed and self.collide(self.player, x) and x.type != 4:
									self.player.slowed = False
									self.player.speed += MUD_SLOW
								if self.collide(self.player, x) and x.type == 1:
									self.player.x = preX
									self.player.y = preY
									continue
								elif self.collide(self.player, x) and x.type == 3:
									self.dialog = DialogBox(x.get_dialog())
									self.dialogOpen = True
									self.storeInteract = x
									self.player.x = preX
									self.player.y = preY
									continue
								elif self.collide(self.player, x) and x.type == 4 and self.player.slowed == False:
									self.player.slowed = True
									self.player.speed -= MUD_SLOW
								elif self.collide(self.player, x) and x.type == 2:
									self.tileArray = room_loader.load(self.nextRoom)
									self.init_tiles()
									self.nextRoom += 1
									self.storeInteract = False
									self.items = []
									for i in range(0, 3):
										self.items.append(objects.Item("misc\\coin.png", random.randint(0, 368), random.randint(0, 368), 1, batch = self.entityBatch))
									self.player.x, self.player.y = 40, 40
									self.enemies = []
									for i in range(0, 3):
										if random.randint(0,1):
											self.enemies.append(enemy.Slime(self.player, self.entityBatch))
										else:
											self.enemies.append(enemy.Zombie(self.player, self.entityBatch))
									continue


	def update_enemies(self, dt):
		if self.game_active and not self.dialogOpen:
			for i in self.enemies:
				if i.type == 0:
					i.update()
#amogus

game = Game(400, 450, "Legend of Ziggy (BETA)")
pyglet.clock.schedule_interval(game.update, 1.0 / 120)
pyglet.clock.schedule_interval(game.update_enemies, 1)
pyglet.app.run()
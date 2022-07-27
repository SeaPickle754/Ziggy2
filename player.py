import pyglet

images = {
	"right":"player/right.png",
	"left":"player/left.png",
	"up":"player/up.png",
	"down":"player/down.png",
	"aright":"player/right_attack.png",
	"aleft":"player/left_attack.png",
	"aup":"player/up_attack.png",
	"adown":"player/down_attack.png",
	"dright":"player/right_damage.png",
	"dleft":"player/left_damage.png",
	"dup":"player/up_damage.png",
	"ddown":"player/down_damage.png",

}

class Player(pyglet.sprite.Sprite):
	def __init__(self, x, y, batch):
		self.textures = {
			"up":pyglet.image.load(images["up"]),
			"down":pyglet.image.load(images["down"]),
			"left":pyglet.image.load(images["left"]),
			"right":pyglet.image.load(images["right"]),
			"aup":pyglet.image.load(images["aup"]),
			"adown":pyglet.image.load(images["adown"]),
			"aleft":pyglet.image.load(images["aleft"]),
			"aright":pyglet.image.load(images["aright"]),
			"dup":pyglet.image.load(images["dup"]),
			"ddown":pyglet.image.load(images["ddown"]),
			"dleft":pyglet.image.load(images["dleft"]),
			"dright":pyglet.image.load(images["dright"])
		}
		self.movement = {
			"up": False,
			"down":False,
			"right":False,
			"left":False,
		}
		self.health = 5
		self.current_direction = "right"
		self.damage = 0
		self.speed = 130
		self.isAttacking = 0
		self.taking_damage = 0
		self.slowed = False
		self.coins = 0
		self.strength = 3

		super().__init__(self.textures["right"], x = x, y = y, batch=self.batch)
	
	def change_direction(self, new_direction):
		if self.current_direction != new_direction:
			self.image = self.textures[new_direction]
			self.current_direction = new_direction
		else:
			return -1
	
	def change_image(self, newImage):
		self.image = self.textures[newImage]

	def get_current_dir(self):
		return self.current_direction
	
	def update(self, dt):
		if self.damage == 0 and self.taking_damage == 0:
			if self.movement["right"]:
				# do this to do more stable movement
				self.x = (self.x + dt * self.speed)
			if self.movement["left"]:
				self.x = (self.x - dt * self.speed)
			if self.movement["up"]:
				self.y = (self.y + dt * self.speed)
			if self.movement["down"]:
				self.y = (self.y - dt * self.speed)
		elif self.damage:
			self.image = self.textures["a"+self.current_direction]
		elif self.taking_damage:
			self.image = self.textures["d"+self.current_direction]
		if self.x < 0:
			self.x = 0
		if self.x > 385:
			self.x = 385
		if self.y < 0:
			self.y = 0
		if self.y > 385:
			self.y = 385

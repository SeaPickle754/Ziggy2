import pyglet

class DialogBox:
	def __init__(self, message):
		self.box = pyglet.shapes.Rectangle(10, 10, 380, 200, color=(0, 0, 0))
		self.label = pyglet.text.Label(message,
							font_name='Ariel',
							font_size=12,
							width=1000,
							x=20, y = 180,
							anchor_x='left', multiline=True)
		
	def draw(self):
		self.box.draw()
		self.label.draw()
from PIL import Image

from drawable_element import DrawableElement

class GenericRectangle(DrawableElement):
	# constants
	IMG_MODE = "RGBA"
	
	def __init__(self, size, fill_color, border_size, border_color):
		self.size = size
		self.fill_color = fill_color
		self.border_size = border_size
		self.border_color = border_color
		self.im = Image.new(self.IMG_MODE, size)

	def draw(self):
		self.fill()
		if self.border_size: self.draw_border()

	def fill(self):
		self.im.putdata((self.fill_color,) * self.size[0] * self.size[1])

	def draw_border(self):
		px = self.im.load()
		w, h = self.size
		for r in range(h):
			for c in range(w):
				if r < self.border_size or c < self.border_size or \
				   r >= h - self.border_size or c >= w - self.border_size:
					p = px[c, r]
					if len(p) < 4 or p[3] != 0: px[c, r] = self.border_color

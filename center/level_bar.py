from rounded_rectangle import RoundedRectangle

class LevelBar(RoundedRectangle):
	#constants
	SIZE = (535, 65)
	CORNER_RADIUS = 10
	BORDER_SIZE = 4

	# COLORS
	BORDER_COLOR = (0, 0, 0) # black
	EMPTY_COLOR = (255, 255, 255) # white
	EMPTY_1CH = 255 # white (1 channel)
	START = (255, 0, 0) # red
	MIDDLE = (255, 255, 0) # yellow
	END = (0, 255, 0) # green

	def __init__(self, percentage):
		super().__init__(self.SIZE, self.EMPTY_COLOR,
						 self.BORDER_SIZE, self.BORDER_COLOR, self.CORNER_RADIUS)
		self.level = int(self.SIZE[0] * percentage)
		self.gradient = [self.get_color_tuple(i) for i in range(self.SIZE[0])]

	def fill(self):
		self.im.putdata(self.gradient * self.SIZE[1])

	def draw_corners(self):
		super().draw_corners()
		w, h = self.SIZE
		# upper left corner
		self.apply_gradient_to_corner(self.gradient, self.corners[0], False)
		self.im.paste(self.corners[0], (0, 0))
		# lower left corner
		self.apply_gradient_to_corner(self.gradient, self.corners[1], False)
		self.im.paste(self.corners[1], (0, h - self.CORNER_RADIUS))
		# lower right corner
		reversed_gradient = self.gradient[::-1]
		self.apply_gradient_to_corner(reversed_gradient, self.corners[2], True)
		self.im.paste(self.corners[2], (w - self.CORNER_RADIUS, h - self.CORNER_RADIUS))
		should_round_corners_of_level = w != self.level and self.level > self.CORNER_RADIUS
		if should_round_corners_of_level:
			level_gradient = self.gradient[:self.level][::-1]
			self.apply_gradient_to_corner(level_gradient, self.corners[2], True, True)
			self.im.paste(self.corners[2], (self.level - self.CORNER_RADIUS, h - self.CORNER_RADIUS))
		# upper right corner
		self.apply_gradient_to_corner(reversed_gradient, self.corners[3], True)
		self.im.paste(self.corners[3], (w - self.CORNER_RADIUS, 0))
		if should_round_corners_of_level:
			self.apply_gradient_to_corner(level_gradient, self.corners[3], True, True)
			self.im.paste(self.corners[3], (self.level - self.CORNER_RADIUS, 0))

	def get_color_tuple(self, i):
		return tuple([self.get_channel_value(i, c) for c in range(3)])

	def get_channel_value(self, i, c):
		if i >= self.level: return self.EMPTY_1CH
		half_size = self.SIZE[0] // 2
		if i < half_size:
			return self.START[c] + int(i / half_size * (self.MIDDLE[c] - self.START[c]))
		return self.MIDDLE[c] + int((i - half_size) / half_size * (self.END[c] - self.MIDDLE[c]))

	def apply_gradient_to_corner(self, gradient, corner, backwards, alpha_to_white=False):
		px = corner.load()
		w, h = corner.size
		range_w = range(w)[::-1] if backwards else range(w)
		for r in range(h):
			i = 0
			for c in range_w:
				if i == len(gradient): break
				elif px[c, r][3] != 0: px[c, r] = gradient[i]
				elif alpha_to_white: px[c, r] = self.EMPTY_COLOR
				i += 1

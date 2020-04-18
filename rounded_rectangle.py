from PIL import Image, ImageDraw

from generic_rectangle import GenericRectangle

class RoundedRectangle(GenericRectangle):
	def __init__(self, size, fill_color, border_size, border_color, corner_radius):
		super().__init__(size, fill_color, border_size, border_color)
		self.corner_radius = corner_radius

	def draw(self):
		self.fill()
		if self.corner_radius: self.draw_corners()
		if self.border_size: self.draw_border()

	def draw_corners(self):
		w, h = self.size
		self.corners = []
		# upper left corner
		corner = self.get_rounded_corner()
		self.im.paste(corner, (0, 0))
		self.corners.append(corner)
		# lower left corner
		corner = corner.rotate(90)
		self.im.paste(corner, (0, h - self.corner_radius))
		self.corners.append(corner)
		# lower right corner
		corner = corner.rotate(90)
		self.im.paste(corner, (w - self.corner_radius, h - self.corner_radius))
		self.corners.append(corner)
		# upper right corner
		corner = corner.rotate(90)
		self.im.paste(corner, (w - self.corner_radius, 0))
		self.corners.append(corner)

	def get_rounded_corner(self):
		corner = Image.new(self.IMG_MODE, (self.corner_radius, self.corner_radius), (0, 0, 0, 0))
		draw = ImageDraw.Draw(corner)
		draw.pieslice((0, 0, self.corner_radius * 2, self.corner_radius * 2),
					  180, 270, fill=self.fill_color)
		return corner

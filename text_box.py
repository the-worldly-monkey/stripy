from PIL import ImageDraw, ImageFont

from rounded_rectangle import RoundedRectangle

class TextBox(RoundedRectangle):
	def __init__(self, size, fill_color, border_size, border_color, corner_radius,
				 text, text_color, font_size, y_offset, cv):
		super().__init__(size, fill_color, border_size, border_color, corner_radius)
		self.cv = cv
		self.text = text
		self.text_color = text_color
		self.font_size = font_size
		self.y_offset = y_offset

	def draw(self):
		super().draw()
		self.im_draw = ImageDraw.Draw(self.im)

		font = ImageFont.truetype(self.cv.fonts["regular"], self.font_size)
		text_size = self.im_draw.textsize(self.text, font=font)
		text_coords = ((self.size[0] - text_size[0]) // 2,
					   (self.size[1] - text_size[1]) // 2 - self.y_offset)

		self.im_draw.text(text_coords, self.text, self.text_color, font=font)

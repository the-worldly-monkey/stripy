from PIL import Image, ImageDraw, ImageFont

from drawable_element import DrawableElement
from generic_rectangle import GenericRectangle

class LanguageCaptionItem(DrawableElement):
	# constants
	BOX_SIZE = (60, 60)
	BORDER_SIZE = 4
	BOX_TEXT_SPACING = 30
	FONT_SIZE = 50 # must be smaller than box height
	FIXED_Y_OFFSET = 5

	# COLORS
	BORDER_COLOR = (255, 255, 255) # white

	def __init__(self, box_color, text, cv):
		super().__init__(cv)
		self.box_color = box_color
		self.text = text
		self.box = GenericRectangle(self.BOX_SIZE, box_color, self.BORDER_SIZE, self.BORDER_COLOR)

	def draw(self):
		self.box.draw()

		font = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		text_size = self.cv.im_draw.textsize(self.text, font=font)
		text_y_offset = (self.box.im.size[1] - text_size[1]) // 2
		text_coords = (self.box.im.size[0] + self.BOX_TEXT_SPACING,
					   text_y_offset - self.FIXED_Y_OFFSET)

		self.im = Image.new(self.cv.IMG_MODE, (text_coords[0] + text_size[0], self.box.im.size[1]),
							self.cv.main_color_rgb)
		self.im.paste(self.box.im, (0, 0))

		self.im_draw = ImageDraw.Draw(self.im)

		self.im_draw.text(text_coords, self.text, self.cv.WHITE_3CH, font=font)

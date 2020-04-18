from PIL import Image, ImageDraw, ImageFont

from drawable_element import DrawableElement

class ColumnLeftItem(DrawableElement):
	# constants
	IMG_TEXT_SPACING = 50
	FONT_SIZE = 50
	FIXED_Y_OFFSET = 5

	def __init__(self, data, cv):
		super().__init__(cv)
		self.img_path = self.get_absolute_path(data["img_path"])
		self.text = data["text"]

	def draw(self):
		img = Image.open(self.img_path)
		img = img.convert(self.cv.IMG_MODE)
		self.hsv_based_color_conversion(img, self.cv.main_color_rgb)
		self.transparency_to_color_conversion(img, self.cv.WHITE_3CH)

		font = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		text_size = self.cv.im_draw.textsize(self.text, font=font)
		text_coords = (img.size[0] + self.IMG_TEXT_SPACING,
					   (img.size[1] - text_size[1]) // 2 - self.FIXED_Y_OFFSET)

		im_size = (text_coords[0] + text_size[0], img.size[1])
		self.im = Image.new(self.cv.IMG_MODE, im_size, self.cv.WHITE_4CH)
		self.im.paste(img, (0, 0))
		self.im_draw = ImageDraw.Draw(self.im)
		self.im_draw.text(text_coords, self.text, self.cv.main_color_rgb, font=font)

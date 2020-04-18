from PIL import Image, ImageDraw, ImageFont

from drawable_element import DrawableElement
from level_bar import LevelBar
from tags import Tags

class ColumnCenterItem(DrawableElement):
	# constants
	IMG_TARGET_SIZE = (150, 150)
	NAME_FONT_SIZE = 50
	TAG_FONT_SIZE = 45
	BAR_NAME_SPACING = 10
	HEAD_TAGS_SPACING = 10

	def __init__(self, data, cv):
		super().__init__(cv)
		self.img_path = self.get_absolute_path(data["img_path"])
		self.allowed_width = data["allowed_width"]
		self.name = data["name"]
		self.level = data["level"]
		self.tags = data["tags"]

	def draw(self):
		img = Image.open(self.img_path)
		img = img.convert(self.cv.IMG_MODE)
		self.transparency_to_color_conversion(img, self.cv.WHITE_3CH)
		img = self.resize_keeping_aspect_ratio(img, self.IMG_TARGET_SIZE, False)
		bar = LevelBar(self.level)
		bar.draw()

		name_font = ImageFont.truetype(self.cv.fonts["regular"], self.NAME_FONT_SIZE)
		name_size = self.cv.im_draw.textsize(self.name, font=name_font)

		bar_name_height = bar.im.size[1] + name_size[1] + self.BAR_NAME_SPACING
		
		tags = Tags(self.allowed_width, self.tags, self.cv)
		tags.draw()

		head_height = max(self.IMG_TARGET_SIZE[1], bar_name_height)
		im_size = (self.allowed_width, head_height + self.HEAD_TAGS_SPACING + tags.im.size[1])
		self.im = Image.new(self.cv.IMG_MODE, im_size, self.cv.WHITE_4CH)

		img_y_offset = 0 if head_height == self.IMG_TARGET_SIZE[1] \
						 else (head_height - self.IMG_TARGET_SIZE[1]) // 2
		img_coords = ((self.IMG_TARGET_SIZE[0] - img.size[0]) // 2,
					  (self.IMG_TARGET_SIZE[1] - img.size[1]) // 2 + img_y_offset)
		self.im.paste(img, img_coords)

		bar_y_offset = 0 if head_height == bar_name_height \
						 else (head_height - bar_name_height) // 2
		bar_coords = (self.allowed_width - bar.im.size[0], bar_y_offset)
		self.im.paste(bar.im, bar_coords)

		name_coords = (bar_coords[0], bar_coords[1] + bar.im.size[1] + self.BAR_NAME_SPACING)
		self.im_draw = ImageDraw.Draw(self.im)
		self.im_draw.text(name_coords, self.name, self.cv.main_color_rgb, font=name_font)

		tags_coords = ((self.allowed_width - tags.im.size[0]) // 2,
					   head_height + self.HEAD_TAGS_SPACING)
		self.im.paste(tags.im, tags_coords)

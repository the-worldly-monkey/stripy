from PIL import Image, ImageFont

from drawable_element import DrawableElement
from text_box import TextBox

class Tags(DrawableElement):
	# constants
	HEIGHT = 70
	FONT_SIZE = 35
	FIXED_Y_OFFSET = 2.5
	BORDER_SIZE = 0 # no border
	CORNER_RADIUS = 35
	SPACING = 10
	MAX_ROWS = 2

	# COLORS
	BG_COLOR = (200, 200, 255)
	TEXT_COLOR = (49, 51, 125) #31337d

	def __init__(self, allowed_width, tags, cv):
		super().__init__(cv)
		self.allowed_width = allowed_width
		self.tags = tags

	def draw(self):
		font = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		tag_boxes = []
		row_widths = []
		coords_list = []
		max_x = 0
		coords = (0, 0)
		for i, tag in enumerate(self.tags):
			tag_size = self.cv.im_draw.textsize(tag, font=font)
			if coords[0] == 0 and tag_size[0] > self.allowed_width: continue
			if coords[0] + tag_size[0] + self.CORNER_RADIUS * 2 > self.allowed_width:
				row_widths.append(coords[0] - self.SPACING)
				if len(row_widths) == self.MAX_ROWS: break
				coords = (0, coords[1] + self.HEIGHT + self.SPACING)
			# if we reach here, the tag box can be drawn at the current coords
			tag_boxes.append(TextBox((tag_size[0] + self.CORNER_RADIUS, self.HEIGHT), self.BG_COLOR,
							 self.BORDER_SIZE, self.cv.WHITE_1CH, self.CORNER_RADIUS, tag,
							 self.TEXT_COLOR, self.FONT_SIZE, self.FIXED_Y_OFFSET, self.cv))
			coords_list.append(coords)
			current_row_width = coords[0] + tag_boxes[-1].size[0]
			if current_row_width > max_x: max_x = current_row_width
			if i == len(self.tags) - 1: row_widths.append(current_row_width)
			else: coords = (current_row_width + self.SPACING, coords[1])
		im_size = (max_x, coords[1] + self.HEIGHT)
		self.im = Image.new(self.cv.IMG_MODE, im_size, self.cv.WHITE_4CH)
		curr_row = 0
		for i, tag_box in enumerate(tag_boxes):
			if i > 0 and coords_list[i][1] != coords_list[i-1][1]: curr_row += 1
			x_offset = (max_x - row_widths[curr_row]) // 2
			tag_box.draw()
			self.im.paste(tag_box.im, (coords_list[i][0] + x_offset, coords_list[i][1]))

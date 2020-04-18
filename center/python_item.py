from PIL import Image, ImageDraw, ImageFont

from column_center_item import ColumnCenterItem
from rounded_rectangle import RoundedRectangle

class PythonItem(ColumnCenterItem):
	# constants
	BUBBLE_BORDER_SIZE = 5
	BUBBLE_CORNER_RADIUS = 10
	BUBBLE_X_OFFSET = 80
	TAIL_X_OFFSET = 50
	TAIL_INCLINATION = 15
	TAIL_HEIGHT = 50
	TAIL_BASE = 35
	FIXED_Y_OFFSET = 7.5
	UNDERLINE_OFFSET = 10
	FONT_SIZE = 35
	MARGIN = 50

	# TEXT
	LINE_1 = "This CV was built with Python!"
	LINE_2 = "Check the source code "
	LINK_TEXT = "here"
	LINK_URL = "https://github.com/the-worldly-monkey/stripy"

	def __init__(self, offsets, data, cv):
		super().__init__(data, cv)
		self.offsets = offsets

	def draw(self):
		super().draw()

		font = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		line_1_size = self.cv.im_draw.textsize(self.LINE_1, font=font)
		line_2_size = self.cv.im_draw.textsize(self.LINE_2, font=font)
		link_text_size = self.cv.im_draw.textsize(self.LINK_TEXT, font=font)

		total_height = line_1_size[1] + max(line_2_size[1], link_text_size[1])
		line_2_total_width = line_2_size[0] + link_text_size[0]
		max_line_width = max(line_1_size[0], line_2_total_width)
		bubble_size = (max_line_width + self.MARGIN * 2, total_height + self.MARGIN * 2)
		bubble = RoundedRectangle(bubble_size, self.cv.WHITE_3CH, self.BUBBLE_BORDER_SIZE,
								  self.cv.main_color_rgb, self.BUBBLE_CORNER_RADIUS)
		bubble.draw()
		line_1_coords = ((bubble_size[0] - line_1_size[0]) // 2,
						 (bubble_size[1] - total_height) // 2 - self.FIXED_Y_OFFSET)
		line_2_coords = ((bubble_size[0] - line_2_total_width) // 2,
						 line_1_coords[1] + line_1_size[1])
		link_text_coords = (line_2_coords[0] + line_2_size[0], line_2_coords[1])
		self.bubble_draw = ImageDraw.Draw(bubble.im)
		self.bubble_draw.text(line_1_coords, self.LINE_1, self.cv.main_color_rgb, font=font)
		self.bubble_draw.text(line_2_coords, self.LINE_2, self.cv.main_color_rgb, font=font)
		self.draw_underlined_text(self.bubble_draw, link_text_coords, self.LINK_TEXT, font,
								  self.UNDERLINE_OFFSET // 2, fill=self.cv.main_color_rgb, width=2)
		
		speech_bubble_height = bubble_size[1] - self.BUBBLE_BORDER_SIZE + self.TAIL_HEIGHT
		self.im_new = Image.new(self.cv.IMG_MODE, (self.im.size[0],
												   self.im.size[1] + speech_bubble_height),
								self.cv.WHITE_4CH)
		
		tail_start_y = bubble_size[1] - self.BUBBLE_BORDER_SIZE
		tail_start_x = self.BUBBLE_X_OFFSET + self.TAIL_X_OFFSET
		tail_sides = [(tail_start_x, tail_start_y),
					  (tail_start_x - self.TAIL_INCLINATION, tail_start_y + self.TAIL_HEIGHT),
					  (tail_start_x + self.TAIL_BASE + self.BUBBLE_BORDER_SIZE, tail_start_y)]
		
		tail_in_start_x = tail_start_x + self.BUBBLE_BORDER_SIZE
		tail_in_sides = [(tail_in_start_x, tail_start_y),
						 (tail_in_start_x - self.TAIL_INCLINATION - self.BUBBLE_BORDER_SIZE // 2,
						  tail_sides[1][1] - self.BUBBLE_BORDER_SIZE),
						 (tail_sides[2][0] - self.BUBBLE_BORDER_SIZE, tail_start_y)]
		
		self.im_new.paste(bubble.im, (self.BUBBLE_X_OFFSET, 0))
		self.im_new.paste(self.im, (0, speech_bubble_height))
		self.im_draw = ImageDraw.Draw(self.im_new)
		self.im_draw.polygon(tail_sides, fill=self.cv.main_color_rgb)
		self.im_draw.polygon(tail_in_sides, fill=self.cv.WHITE_3CH)
		self.im = self.im_new

		# finally, add link URL, size and coords
		self.cv.links.append(self.LINK_URL)
		self.cv.links_coords.append((self.offsets[0] + self.BUBBLE_X_OFFSET + link_text_coords[0],
									 self.offsets[1] + link_text_coords[1]))
		self.cv.links_sizes.append((link_text_size[0], link_text_size[1] + self.UNDERLINE_OFFSET))

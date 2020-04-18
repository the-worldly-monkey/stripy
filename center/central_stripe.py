from PIL import Image

from drawable_element import DrawableElement
from column_left import ColumnLeft
from column_center import ColumnCenter
from column_right import ColumnRight

class CentralStripe(DrawableElement):
	# constants
	DASHED_LINES_X_OFFSETS = [790, 1690]
	DASHED_LINES_Y_OFFSETS = [105, 860]
	MAX_Y_OFFSETS = [2480, 3250]
	Y_OFFSET = 15
	X_SIDE = 20
	Y_SIDE = 35
	
	def __init__(self, data, cv):
		super().__init__(cv)

		if "more_img_path" in data:
			more_im = Image.open(self.get_absolute_path(data["more_img_path"]))
			more_im = more_im.convert(self.cv.IMG_MODE)
			self.hsv_based_color_conversion(more_im, cv.main_color_rgb)
			self.transparency_to_color_conversion(more_im, self.cv.WHITE_3CH)
		else: more_im = None
		shared = {
			"more_im": more_im,
			"column_offsets": self.DASHED_LINES_X_OFFSETS + [self.X_SIDE]
		}
		
		self.elements = [
			ColumnLeft(dict(data["column_left"], **shared), cv),
			ColumnCenter(dict(data["column_center"], **shared), cv),
			ColumnRight(dict(data["column_right"], **shared), cv)
		]

	def draw(self):
		self.draw_dashed_lines()
		for elem in self.elements: elem.draw()

	def draw_dashed_lines(self):
		for i, x_offset in enumerate(self.DASHED_LINES_X_OFFSETS):
			y = self.DASHED_LINES_Y_OFFSETS[i]
			while y < self.MAX_Y_OFFSETS[i]:
				self.cv.im_draw.polygon([(x_offset, y),
										 (x_offset, y + self.Y_SIDE),
										 (x_offset + self.X_SIDE, y + self.Y_SIDE + self.Y_OFFSET),
										 (x_offset + self.X_SIDE, y + self.Y_OFFSET)],
										fill=self.cv.main_color_rgb)
				y += (self.Y_SIDE * 2)

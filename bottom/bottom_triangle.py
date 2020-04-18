from drawable_element import DrawableElement
from languages import Languages
from education import Education

class BottomTriangle(DrawableElement):
	# constants
	BOTTOM_TRIANGLE_SIDES = [(0, 1790), (0, 3508), (2025, 3508)]
	
	def __init__(self, data, cv):
		super().__init__(cv)
		self.elements = [
			Languages(data["languages"], cv),
			Education(data["education"], cv)
		]

	def draw(self):
		self.cv.im_draw.polygon(self.BOTTOM_TRIANGLE_SIDES, fill=self.cv.main_color_rgb)
		for elem in self.elements: elem.draw()
		self.cv.im_draw.polygon([(0, 0)] + self.BOTTOM_TRIANGLE_SIDES[::2] + [self.cv.IMG_SIZE] + 
								[(self.cv.IMG_SIZE[0], 0)], fill=self.cv.WHITE_4CH)

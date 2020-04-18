from drawable_element import DrawableElement
from name_title import NameTitle
from photo import Photo
from contact_info import ContactInfo

class TopTriangle(DrawableElement):
	# constants
	TOP_TRIANGLE_SIDES = [(685, 0), (2480, 1490), (2480, 0)]
	
	def __init__(self, data, cv):
		super().__init__(cv)
		self.elements = [
			NameTitle(data["name_title"], cv),
			Photo(data["photo"], cv),
			ContactInfo(data["contact_info"], cv)
		]

	def draw(self):
		self.cv.im_draw.polygon(self.TOP_TRIANGLE_SIDES, fill=self.cv.main_color_rgb)
		for elem in self.elements: elem.draw()

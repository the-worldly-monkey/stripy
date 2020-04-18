from drawable_element import DrawableElement
from education_item import EducationItem

class Education(DrawableElement):
	# constants
	BASE_Y_OFFSET = 3090
	MAX_WIDTH = 1660
	MIN_X_SPACING = 35
	CONTENT_Y_SPACING = 70

	def __init__(self, data, cv):
		super().__init__(cv)
		self.edu_header = data["edu_header"]
		self.items = data["items"][:2]

	def draw(self):
		if not self.items: return
		header_coords = (self.cv.MARGIN + self.cv.HEADER_INDENT, self.BASE_Y_OFFSET)
		self.cv.im_draw.text(header_coords, self.edu_header, self.cv.WHITE_3CH, font=self.cv.h_font)

		header_size = self.cv.im_draw.textsize(self.edu_header, font=self.cv.h_font)
		edu1_coords = (self.cv.MARGIN, self.BASE_Y_OFFSET + header_size[1] + self.CONTENT_Y_SPACING)

		edu1 = EducationItem(self.items[0], self.cv)
		edu1.draw()
		self.cv.im.paste(edu1.im, edu1_coords)
		if len(self.items) < 2: return
		
		edu2 = EducationItem(self.items[1], self.cv)
		edu2.draw()
		x_margin = max((self.MAX_WIDTH - edu1.im.size[0] - edu2.im.size[0]) // 2, self.MIN_X_SPACING)
		self.cv.im.paste(edu2.im, (edu1_coords[0] + edu1.im.size[0] + x_margin, edu1_coords[1]))

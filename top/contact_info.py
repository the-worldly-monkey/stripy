from PIL import ImageFont
from os import name, linesep

from drawable_element import DrawableElement

class ContactInfo(DrawableElement):
	# constants
	BASE_COORDS = (1680, 630)
	FONT_SIZE = 45
	SPACING = 50
	IS_WINDOWS = name == "nt"
	FIXED_X_OFFSET = 15 if IS_WINDOWS else 0

	def __init__(self, data, cv):
		super().__init__(cv)
		self.align = data["align"]
		self.info = data["info"][:4]
		self.links = data["links"][:4]

	def draw(self):
		coords = self.BASE_COORDS
		font = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		text = linesep.join(self.info) + (" " if self.IS_WINDOWS else "")
		text_size = self.cv.im_draw.textsize(text, font=font)
		self.cv.im_draw.multiline_text(coords, text, self.cv.WHITE_3CH,
									   spacing=self.SPACING, font=font, align=self.align)
		for i, el in enumerate(self.info): # for contact info, each element has a link
			w, h = self.cv.im_draw.textsize(el, font=font)
			if i > 0: coords = (coords[0] + self.cv.links_sizes[-1][0] - w,
								coords[1] + self.cv.links_sizes[-1][1] + self.FONT_SIZE)
			elif w < text_size[0]: coords = (coords[0] + text_size[0] - w - self.FIXED_X_OFFSET,
											 coords[1])
			self.cv.links.append(self.links[i])
			self.cv.links_coords.append(coords)
			self.cv.links_sizes.append((w, h))

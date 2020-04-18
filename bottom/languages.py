from drawable_element import DrawableElement
from language_box import LanguageBox
from language_caption_item import LanguageCaptionItem

class Languages(DrawableElement):
	# constants
	BASE_Y_OFFSET = 2255
	CONTENT_SPACING = 70
	CAPTION_X_SPACING = 35
	CAPTION_Y_SPACING = 45
	ELEM_FIRST_ROW = 2
	ELEM_SECOND_ROW = 3

	def __init__(self, data, cv):
		super().__init__(cv)
		self.lang_header = data["lang_header"]
		self.lang_colors = [self.hex_to_rgb(hex) for hex in data["lang_colors_hex"][:4]]
		self.lang_captions = data["lang_captions"][:4]
		self.lang_levels = data["lang_levels"][:5]
		self.base_coords = (self.cv.MARGIN, self.BASE_Y_OFFSET)

	def draw(self):
		if not self.lang_levels or not self.lang_colors or not self.lang_captions: return
		lang_n = len(self.lang_levels)
		if lang_n < 3:
			self.base_coords = (self.base_coords[0],
								self.base_coords[1] + LanguageBox.SIZE[1] + self.CAPTION_Y_SPACING)
		header_coords = (self.base_coords[0] + self.cv.HEADER_INDENT, self.base_coords[1])
		self.cv.im_draw.text(header_coords, self.lang_header, self.cv.WHITE_3CH, font=self.cv.h_font)

		header_size = self.cv.im_draw.textsize(self.lang_header, font=self.cv.h_font)
		boxes_base_coords = (self.base_coords[0],
							 self.base_coords[1] + header_size[1] + self.CONTENT_SPACING)
		
		elem_row_1 = self.ELEM_FIRST_ROW if lang_n == self.ELEM_FIRST_ROW \
										 else max(1, lang_n - self.ELEM_SECOND_ROW)
		c = 0
		for i in range(elem_row_1): # first row
			if c == lang_n: break
			box_coords = (boxes_base_coords[0] + i * (LanguageBox.SIZE[0] + self.CONTENT_SPACING),
						  boxes_base_coords[1])
			self.cv.im.paste(self.generate_language_box(self.lang_levels[c]), box_coords)
			c += 1
			
		for i in range(self.ELEM_SECOND_ROW): # second row
			if c == lang_n: break
			box_coords = (boxes_base_coords[0] + i * (LanguageBox.SIZE[0] + self.CONTENT_SPACING),
						  boxes_base_coords[1] + LanguageBox.SIZE[1] + self.CONTENT_SPACING)
			self.cv.im.paste(self.generate_language_box(self.lang_levels[c]), box_coords)
			c += 1
		
		captions_coords = (boxes_base_coords[0],
						   boxes_base_coords[1] + LanguageBox.SIZE[1] * (1 if lang_n < 3 else 2) +
												  self.CONTENT_SPACING +
												  (self.CAPTION_Y_SPACING if lang_n > 2 else 0))
		
		for i, lang_caption in enumerate(self.lang_captions):
			caption = LanguageCaptionItem(self.lang_colors[i], lang_caption, self.cv)
			caption.draw()
			self.cv.im.paste(caption.im, captions_coords)
			captions_coords = (captions_coords[0] + caption.im.size[0] +
							   self.CAPTION_X_SPACING, captions_coords[1])

	def generate_language_box(self, language):
		box = LanguageBox(self.lang_colors[language["level"]], language["iso639_1"], self.cv)
		box.draw()
		return box.im

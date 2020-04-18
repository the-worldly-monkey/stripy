from text_box import TextBox

class LanguageBox(TextBox):
	# constants
	SIZE = (235, 235)
	FONT_SIZE = 80
	FIXED_Y_OFFSET = 10
	BORDER_SIZE = 4
	CORNER_RADIUS = 0 # no rounded corners

	# COLORS
	BORDER_COLOR = (255, 255, 255) # white

	def __init__(self, fill_color, text, cv):
		super().__init__(self.SIZE, fill_color, self.BORDER_SIZE, self.BORDER_COLOR,
						 self.CORNER_RADIUS, text[:2].upper(), cv.WHITE_3CH, self.FONT_SIZE,
						 self.FIXED_Y_OFFSET, cv)

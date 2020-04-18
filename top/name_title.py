from PIL import ImageFont
from os import linesep

from drawable_element import DrawableElement

class NameTitle(DrawableElement):
	# constants
	NAME_X_OFFSET = 1200
	NAME_BASE_Y_OFFSET = 195
	NAME_PULL_UP_FACTOR = 25
	NAME_FONT_SIZE = 75
	NAME_TITLE_Y_OFFSET = 120
	TITLE_FONT_SIZE = 60
	TITLE_ROW_MAX_LEN = 20
	TITLE_MAX_ROWS = 3
	TITLE_SPACING = 10

	def __init__(self, data, cv):
		super().__init__(cv)
		self.name = data["name"]
		self.title = data["title"]
		self.title_align = data["title_align"]

	def draw(self):
		# preprocess title
		self.title = self.title.split()
		title_row_len = 0
		rows = 1
		diff = 0
		i = 0
		num_of_words = len(self.title)
		while i < num_of_words:
			curr_word = self.title[i]
			title_row_len += len(curr_word)
			if (i+1) < len(self.title):
				next_word = self.title[i+1]
				if (title_row_len + len(next_word) + 1) > self.TITLE_ROW_MAX_LEN:
					rows += 1
					if rows > self.TITLE_MAX_ROWS:
						if title_row_len > (self.TITLE_ROW_MAX_LEN - 3):
							diff = self.TITLE_ROW_MAX_LEN - (title_row_len + 3)
						self.title = self.title[:i+1]
						break
					else:
						self.title.insert(i+1, linesep)
						title_row_len = 0
						num_of_words += 1
						i += 1
				else:
					self.title[i] = curr_word + " "
					title_row_len += 1
			i += 1
		self.title = ''.join(self.title)
		if rows > self.TITLE_MAX_ROWS:
			self.title = (self.title[:diff] if diff else self.title) + "..."

		name_pull_up_value = self.title.count(linesep) * self.NAME_PULL_UP_FACTOR
		name_coords = (self.NAME_X_OFFSET, self.NAME_BASE_Y_OFFSET - name_pull_up_value)

		name_font = ImageFont.truetype(self.cv.fonts["regular"], self.NAME_FONT_SIZE)
		title_font = ImageFont.truetype(self.cv.fonts["italic"], self.TITLE_FONT_SIZE)
		
		name_size = self.cv.im_draw.textsize(self.name, font=name_font)
		title_longest_row_size = self.cv.im_draw.textsize(max(self.title.split(linesep),
															  key=len), font=title_font)
		name_title_x_offset = (name_size[0] - title_longest_row_size[0]) // 2
		title_coords = (name_coords[0] + name_title_x_offset,
						name_coords[1] + self.NAME_TITLE_Y_OFFSET)

		self.cv.im_draw.text(name_coords, self.name, self.cv.WHITE_3CH, font=name_font)
		self.cv.im_draw.multiline_text(title_coords, self.title, self.cv.WHITE_3CH,
									   spacing=self.TITLE_SPACING, font=title_font,
									   align=self.title_align)

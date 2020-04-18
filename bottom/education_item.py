from PIL import Image, ImageDraw, ImageFont

from drawable_element import DrawableElement

class EducationItem(DrawableElement):
	# constants
	LOGO_TARGET_SIZE = (200, 200)
	FONT_SIZE = 45
	LOGO_TEXT_SPACING = 20
	FIXED_Y_OFFSET = 5

	def __init__(self, data, cv):
		super().__init__(cv)
		self.logo_path = self.get_absolute_path(data["logo_path"])
		self.row1 = data["school_name"]
		self.row2 = data["course_name"]
		self.row3 = data["final_score"]
		self.row4 = data["period_span"]

	def draw(self):
		font_m = ImageFont.truetype(self.cv.fonts["medium"], self.FONT_SIZE)
		font_r = ImageFont.truetype(self.cv.fonts["regular"], self.FONT_SIZE)
		font_i = ImageFont.truetype(self.cv.fonts["italic"], self.FONT_SIZE)

		row1_size = self.cv.im_draw.textsize(self.row1, font=font_m)
		row2_size = self.cv.im_draw.textsize(self.row2, font=font_r)
		row3_size = self.cv.im_draw.textsize(self.row3, font=font_i)
		row4_size = self.cv.im_draw.textsize(self.row4, font=font_r)

		total_text_size = (max(size[0] for size in [row1_size, row2_size, row3_size, row4_size]),
						   row1_size[1] + row2_size[1] + row3_size[1] + row4_size[1])
		
		logo = Image.open(self.logo_path)
		logo = logo.convert(self.cv.IMG_MODE)
		self.transparency_to_color_conversion(logo, self.cv.main_color_rgb)
		logo = self.resize_keeping_aspect_ratio(logo, self.LOGO_TARGET_SIZE, False)
		text_x_offset = logo.size[0] + self.LOGO_TEXT_SPACING
		im_size = (text_x_offset + total_text_size[0], max(total_text_size[1], logo.size[1]))
		self.im = Image.new(self.cv.IMG_MODE, im_size, self.cv.main_color_rgb)

		logo_coords = (0, 0) if logo.size[1] == im_size[1] else \
					  (0, (im_size[1] - logo.size[1]) // 2 - self.FIXED_Y_OFFSET)
		
		text_coords = (text_x_offset, 0) if total_text_size[1] == im_size[1] else \
					  (text_x_offset, (im_size[1] - total_text_size[1]) // 2 - self.FIXED_Y_OFFSET)

		self.im.paste(logo, logo_coords)
		self.im_draw = ImageDraw.Draw(self.im)
		self.im_draw.text(text_coords, self.row1, self.cv.WHITE_3CH, font=font_m)
		row2_coords = (text_coords[0], text_coords[1] + row1_size[1])
		self.im_draw.text(row2_coords, self.row2, self.cv.WHITE_3CH, font=font_r)
		row3_coords = (text_coords[0], row2_coords[1] + row2_size[1])
		self.im_draw.text(row3_coords, self.row3, self.cv.WHITE_3CH, font=font_i)
		row4_coords = (text_coords[0], row3_coords[1] + row3_size[1])
		self.im_draw.text(row4_coords, self.row4, self.cv.WHITE_3CH, font=font_r)

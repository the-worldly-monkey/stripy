from PIL import Image, ImageDraw, ImageFont

from rounded_rectangle import RoundedRectangle

class ColumnRightItem(RoundedRectangle):
	# constants
	SIZE = (580, 350)
	FLAG_SIZE = (65, 65)
	CORNER_RADIUS = 10
	BORDER_SIZE = 4
	MARGIN = 30
	FIXED_Y_OFFSET = 5
	NAME_FONT_SIZE = 60
	NAME_PERIOD_SPAN_SPACING = 15
	PERIOD_SPAN_FONT_SIZE = 50
	IMG_SPACING = 5
	ELLIPSIS = "..."

	# COLORS
	BORDER_COLOR = (73, 73, 73)

	def __init__(self, data, cv):
		super().__init__(self.SIZE, self.hex_to_rgb(data["bg_color_hex"]),
						 self.BORDER_SIZE, self.BORDER_COLOR, self.CORNER_RADIUS)
		self.cv = cv
		self.name = data["name"]
		self.period_span = data["period_span"]
		self.flag_paths = [self.get_absolute_path(path) for path in data["flag_paths"][:2][::-1]]
		self.logo_paths = [self.get_absolute_path(path) for path in data["logo_paths"][:4]]

	def draw(self):
		super().draw()
		
		flag_coords = (self.SIZE[0] - self.MARGIN - self.FLAG_SIZE[0], self.MARGIN)
		for flag_path in self.flag_paths:
			flag_im = Image.open(flag_path).convert(self.cv.IMG_MODE)
			flag_im = flag_im.convert(self.cv.IMG_MODE)
			self.transparency_to_color_conversion(flag_im, self.fill_color)
			self.im.paste(self.resize_keeping_aspect_ratio(flag_im, self.FLAG_SIZE, False),
						  flag_coords)
			flag_coords = (flag_coords[0] - self.IMG_SPACING - self.FLAG_SIZE[0], self.MARGIN)
		
		name_max_width = flag_coords[0] + self.FLAG_SIZE[0] - self.IMG_SPACING - self.MARGIN
		
		self.im_draw = ImageDraw.Draw(self.im)
		name_font = ImageFont.truetype(self.cv.fonts["medium"], self.NAME_FONT_SIZE)
		period_span_font = ImageFont.truetype(self.cv.fonts["regular"],
											  self.PERIOD_SPAN_FONT_SIZE)

		name_size = self.im_draw.textsize(self.name, font=name_font)
		while name_size[0] > name_max_width:
			self.name = self.name[:-4 if self.name.endswith(self.ELLIPSIS) else -1] + self.ELLIPSIS
			name_size = self.im_draw.textsize(self.name, font=name_font)

		name_coords = (self.MARGIN, self.MARGIN - self.FIXED_Y_OFFSET)
		self.im_draw.text(name_coords, self.name, self.cv.WHITE_3CH, font=name_font)
		
		period_span_coords = (self.MARGIN,
							  name_coords[1] + name_size[1] + self.NAME_PERIOD_SPAN_SPACING)
		self.im_draw.text(period_span_coords, self.period_span, self.cv.WHITE_3CH,
						  font=period_span_font)
		
		period_span_size = self.im_draw.textsize(self.period_span, font=period_span_font)
		logo_size = ((self.SIZE[0] - self.MARGIN * 2 - self.IMG_SPACING * 3) // 4,
					 self.SIZE[1] - self.MARGIN * 2 - period_span_size[1] - period_span_coords[1])
		min_size = min(logo_size)
		
		logo_base_y = period_span_coords[1] + period_span_size[1] + self.MARGIN
		for i, logo_path in enumerate(self.logo_paths):
			logo_im = Image.open(logo_path).convert(self.cv.IMG_MODE)
			logo_im = logo_im.convert(self.cv.IMG_MODE)
			self.transparency_to_color_conversion(logo_im, self.fill_color)
			logo_im = self.resize_keeping_aspect_ratio(logo_im, (min_size, min_size), False)
			x_offset = (logo_size[0] + self.IMG_SPACING) * i + self.MARGIN
			x = x_offset + (logo_size[0] - min_size) // 2 + (min_size - logo_im.size[0]) // 2
			y = logo_base_y + (logo_size[1] - min_size) // 2 + (min_size - logo_im.size[1]) // 2
			self.im.paste(logo_im, (x, y))

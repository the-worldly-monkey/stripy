from PIL import Image, ImageDraw

from drawable_element import DrawableElement

class Photo(DrawableElement):
	# constants
	BG_X_OFFSET = 1950
	BG_OFFSET = 10
	TARGET_SIZE = (435, 435)

	def __init__(self, data, cv):
		super().__init__(cv)
		self.path = self.get_absolute_path(data["path"])
		self.bg_coords = (self.BG_X_OFFSET, self.cv.MARGIN)

	def draw(self):
		photo = self.resize_and_crop_center(Image.open(self.path), self.TARGET_SIZE)
		photo = photo.convert(self.cv.IMG_MODE)
		bg_size = (photo.size[0] + self.BG_OFFSET, photo.size[1] + self.BG_OFFSET)
		bg = Image.new(self.cv.IMG_MODE, bg_size, self.cv.WHITE_3CH)
		mask_im = Image.new(str(1), photo.size, 0)
		mask_bg = Image.new(str(1), bg.size, 0)
		draw = ImageDraw.Draw(mask_bg)
		draw.ellipse([(0, 0), bg.size], fill=self.cv.WHITE_1CH)
		draw = ImageDraw.Draw(mask_im)
		draw.ellipse([(0, 0), photo.size], fill=self.cv.WHITE_1CH)
		actual_photo_coords = (self.bg_coords[0] + self.BG_OFFSET // 2,
							   self.bg_coords[1] + self.BG_OFFSET // 2)
		self.cv.im.paste(bg, self.bg_coords, mask=mask_bg)
		self.cv.im.paste(photo, actual_photo_coords, mask=mask_im)

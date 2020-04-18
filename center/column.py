from drawable_element import DrawableElement

class Column(DrawableElement):
	# constants
	HEADER_ITEMS_OFFSET = 200
	ITEM_SPACING = 50

	def __init__(self, more_im, more_link, cv):
		super().__init__(cv)
		self.more_im = more_im
		self.more_link = more_link
	
	def add_more_im_link(self, x_center, y):
		if not self.more_link or not self.more_im: return
		more_im_coords = (x_center - self.more_im.size[0] // 2, y)
		self.cv.im.paste(self.more_im, more_im_coords)
		self.cv.links.append(self.more_link)
		self.cv.links_coords.append(more_im_coords)
		self.cv.links_sizes.append(self.more_im.size)

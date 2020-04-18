from column import Column
from column_left_item import ColumnLeftItem

class ColumnLeft(Column):
	# constants
	BASE_Y_OFFSET = 195

	def __init__(self, data, cv):
		super().__init__(data["more_im"], data["more_link"] if "more_link" in data else None, cv)
		self.header = data["header"]
		self.items = data["items"][:5]
		self.width = data["column_offsets"][0]
		self.base_coords = (self.cv.MARGIN, self.BASE_Y_OFFSET)

	def draw(self):
		if not self.items: return
		self.cv.im_draw.text(self.base_coords, self.header, self.cv.main_color_rgb,
							 font=self.cv.h_font)

		header_size = self.cv.im_draw.textsize(self.header, font=self.cv.h_font)
		item_coords = (self.base_coords[0],
					   self.base_coords[1] + header_size[1] + self.HEADER_ITEMS_OFFSET)
		for item in self.items:
			column_left_item = ColumnLeftItem(item, self.cv)
			column_left_item.draw()
			self.cv.im.paste(column_left_item.im, item_coords)
			item_coords = (item_coords[0],
						   item_coords[1] + column_left_item.im.size[1] + self.ITEM_SPACING)
		
		self.add_more_im_link(self.width // 2, item_coords[1])

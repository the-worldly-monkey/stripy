from column import Column
from column_right_item import ColumnRightItem

class ColumnRight(Column):
	# constants
	BASE_Y_OFFSET = 1330

	def __init__(self, data, cv):
		super().__init__(data["more_im"], data["more_link"] if "more_link" in data else None, cv)
		self.header = data["header"]
		self.items = data["items"][:4]
		self.adjusted_offset = data["column_offsets"][1] + data["column_offsets"][2]
		self.width = self.cv.IMG_SIZE[0] - self.adjusted_offset
		self.base_coords = (self.adjusted_offset + self.cv.MARGIN, self.BASE_Y_OFFSET)
	
	def draw(self):
		if not self.items: return
		self.cv.im_draw.text(self.base_coords, self.header, self.cv.main_color_rgb,
							 font=self.cv.h_font)

		header_size = self.cv.im_draw.textsize(self.header, font=self.cv.h_font)
		item_coords = (self.base_coords[0],
					   self.base_coords[1] + header_size[1] + self.HEADER_ITEMS_OFFSET)
		for item in self.items:
			column_right_item_item = ColumnRightItem(item, self.cv)
			column_right_item_item.draw()
			self.transparency_to_color_conversion(column_right_item_item.im, self.cv.WHITE_3CH)
			self.cv.im.paste(column_right_item_item.im, item_coords)
			item_coords = (item_coords[0],
						   item_coords[1] + column_right_item_item.im.size[1] + self.ITEM_SPACING)
		
		self.add_more_im_link(self.adjusted_offset + self.width // 2, item_coords[1])

from sys import implementation

from column import Column
from column_center_item import ColumnCenterItem
from python_item import PythonItem

class ColumnCenter(Column):
	# constants
	BASE_Y_OFFSET = 600

	def __init__(self, data, cv):
		super().__init__(data["more_im"], data["more_link"] if "more_link" in data else None, cv)
		self.header = data["header"]
		self.items = data["items"][:4]
		self.adjusted_offset = data["column_offsets"][0] + data["column_offsets"][2]
		self.width = data["column_offsets"][1] - data["column_offsets"][0]
		self.base_coords = (self.adjusted_offset + self.cv.MARGIN, self.BASE_Y_OFFSET)
	
	def draw(self):
		if not self.items: return
		self.cv.im_draw.text(self.base_coords, self.header, self.cv.main_color_rgb,
							 font=self.cv.h_font)

		header_size = self.cv.im_draw.textsize(self.header, font=self.cv.h_font)
		item_coords = (self.base_coords[0],
					   self.base_coords[1] + header_size[1] + self.HEADER_ITEMS_OFFSET)
		allowed_width = self.width - self.cv.MARGIN * 2
		for item in self.items:
			item["allowed_width"] = allowed_width
			level_str = str(item["level"])
			if level_str.endswith("%"): level_str = level_str[:-1] + "/100"
			item["level"] = eval(level_str)
			column_center_item = PythonItem(item_coords, item, self.cv) \
								 if implementation.name[1:] in item["name"].lower() \
								 else ColumnCenterItem(item, self.cv)
			column_center_item.draw()
			self.transparency_to_color_conversion(column_center_item.im, self.cv.WHITE_3CH)
			self.cv.im.paste(column_center_item.im, item_coords)
			item_coords = (item_coords[0],
						   item_coords[1] + column_center_item.im.size[1] + self.ITEM_SPACING)
		
		self.add_more_im_link(self.adjusted_offset + self.width // 2, item_coords[1])

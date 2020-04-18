from abc import ABC, abstractmethod
from PIL import Image
from os.path import isabs, join, dirname, realpath
from colorsys import rgb_to_hsv, hsv_to_rgb
from re import split

class DrawableElement(ABC):
	# Utility functions
	@staticmethod
	def get_absolute_path(rel_path):
		if isabs(rel_path): return rel_path
		return join(dirname(realpath(__file__)), *split("\\/", rel_path))

	@staticmethod
	def rgb_to_hex(*rgb):
		return ''.join(map(lambda x: "{:02X}".format(min(max(0, x), 255)), rgb))

	@staticmethod
	def hex_to_rgb(hex):
		if len(hex) == 3: hex = ''.join([c + c for c in hex])
		return (int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:], 16))

	@staticmethod
	def hsv_based_color_conversion(im, target_color):
		target_h, target_s, target_v = rgb_to_hsv(*target_color)
		max_s = 0
		min_v = 255
		px = im.load()
		w, h = im.size
		for r in range(h):
			for c in range(w):
				p_rgb = px[c, r][:3]
				if any(chan for chan in p_rgb):
					_, s, v = rgb_to_hsv(*p_rgb)
					if s > max_s: max_s = s
					if v < min_v: min_v = v
		delta_s = target_s - max_s
		delta_v = target_v - min_v
		for r in range(h):
			for c in range(w):
				p = px[c, r]
				_, p_s, p_v = rgb_to_hsv(*p[:3])
				p_s += delta_s
				p_v += delta_v
				px[c, r] = tuple([int(chan) for chan in hsv_to_rgb(target_h, p_s, p_v)] + [p[3]])

	@staticmethod
	def transparency_to_color_conversion(im, target_color):
		px = im.load()
		w, h = im.size
		for r in range(h):
			for c in range(w):
				p = px[c, r]
				if p[3] == 0:
					px[c, r] = tuple(list(target_color) + [255])

	@staticmethod
	def resize_keeping_aspect_ratio(im, target_size, to_smallest_side=True):
		w, h = im.size
		ratios = (target_size[0] / w, target_size[1] / h)
		resize_ratio = max(ratios) if to_smallest_side else min(ratios)
		return im if resize_ratio == 1 else im.resize((round(w * resize_ratio),
													   round(h * resize_ratio)), Image.LANCZOS)

	@staticmethod
	def crop_center_if_not_square(im, target_size):
		w, h = im.size
		if w != h:
			target_w, target_h = target_size
			left = (w - target_w) // 2
			top = (h - target_h) // 2
			right = (w + target_w) // 2
			bottom = (h + target_h) // 2
			im = im.crop((left, top, right, bottom))
		return im

	@staticmethod
	def resize_and_crop_center(im, target_size):
		if im.size[0] != target_size[0] or im.size[1] != target_size[1]:
			im = DrawableElement.resize_keeping_aspect_ratio(im, target_size)
			im = DrawableElement.crop_center_if_not_square(im, target_size)
		return im

	@staticmethod
	def draw_underlined_text(draw, coords, text, font, underline_spacing, fill, width):
		text_w, text_h = draw.textsize(text, font=font)
		line_x, line_y = coords[0], coords[1] + text_h + underline_spacing
		draw.text(coords, text, font=font, fill=fill)
		draw.line((line_x, line_y, line_x + text_w, line_y), fill=fill, width=width)

	def __init__(self, cv):
		self.cv = cv

	@abstractmethod
	def draw(self):
		pass

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from os.path import basename
from io import BytesIO
from fpdf import FPDF
import json

from drawable_element import DrawableElement
from top_triangle import TopTriangle
from central_stripe import CentralStripe
from bottom_triangle import BottomTriangle

class Cv(DrawableElement):
	# constants
	IMG_MODE = "RGBA"
	IMG_SIZE = (2480, 3508)
	A4_SIZE_MM = (210, 297)
	FPDF_PAGE_SETUP = (0, 0, *A4_SIZE_MM) # x, y, w, h
	W_PX_MM_RATIO = IMG_SIZE[0] / A4_SIZE_MM[0]
	H_PX_MM_RATIO = IMG_SIZE[1] / A4_SIZE_MM[1]
	AVG_PX_MM_RATIO = (W_PX_MM_RATIO + H_PX_MM_RATIO) / 2
	MARGIN = 85
	HEADER_FONT_SIZE = 70
	HEADER_INDENT = 15

	# COLORS
	WHITE_4CH = (255, 255, 255, 0)
	WHITE_3CH = (255, 255, 255)
	WHITE_1CH = 255

	def __init__(self, json_config_file):
		with open(json_config_file, encoding="utf-8") as f:
			json_config = json.load(f)
			self.img = json_config["img"]
			self.main_color_rgb = self.hex_to_rgb(self.img["main_color_hex"])
			self.out = self.generate_out_fpath(basename(json_config_file).split(".")[0])
			self.fonts = json_config["font_paths"]
			for font_name, font_relative_path in self.fonts.items():
				self.fonts[font_name] = self.get_absolute_path(font_relative_path)
			self.im = Image.new(self.IMG_MODE, self.IMG_SIZE, self.WHITE_4CH)
			self.im_draw = ImageDraw.Draw(self.im)
			self.elements = [
				BottomTriangle(json_config["bottom_triangle"], self),
				CentralStripe(json_config["central_stripe"], self),
				TopTriangle(json_config["top_triangle"], self)
			]
			self.h_font = ImageFont.truetype(self.fonts["medium"], self.HEADER_FONT_SIZE)
			self.links, self.links_coords, self.links_sizes = [], [], []

	def generate_out_fpath(self, base):
		return "%s_%s.pdf" % (self.get_absolute_path(base), datetime.now().strftime("%Y%m%d"))

	def generate(self):
		self.draw()
		self.save_pdf()
		return self.out

	def draw(self):
		for elem in self.elements: elem.draw()

	def save_pdf(self):
		img_format = self.img["format"]
		img_data = BytesIO()
		
		self.im = self.im.convert(self.img["mode"])
		self.im.save(img_data, format=img_format)

		pdf = FPDF()
		pdf.compress = False
		pdf.add_page()
		pdf.image(img_format, *self.FPDF_PAGE_SETUP, file=img_data)
		if self.links: self.add_links(pdf)
		pdf.output(self.out)

	def add_links(self, pdf):
		for i, (target_x, target_y) in enumerate(self.links_coords):
			pdf.link(x=self.px_to_mm(target_x, self.W_PX_MM_RATIO),
					 y=self.px_to_mm(target_y, self.H_PX_MM_RATIO),
					 w=self.px_to_mm(self.links_sizes[i][0], self.W_PX_MM_RATIO),
					 h=self.px_to_mm(self.links_sizes[i][1], self.H_PX_MM_RATIO),
					 link=self.links[i])

	def px_to_mm(self, px, ratio=AVG_PX_MM_RATIO):
		return px / ratio

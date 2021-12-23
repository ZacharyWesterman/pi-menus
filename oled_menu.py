from PIL import Image, ImageDraw, ImageFont

class oled_menu(object):
	def __init__(self, disp):
		self.opt = []
		self.title = ''
		self.disp = disp
		self.font = ImageFont.load_default()
		self.selected = 0
		self.choiceDisp = 0

	def options(self, optTree, title = ''):
		self.opt = optTree['options']
		self.title = title

	def display(self):
		image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
		draw = ImageDraw.Draw(image)

		pos = 0
		scale = 11
		offset = 0
		maxDisp = int(self.disp.height / scale) + 1
		startH = 0

		if self.title != '':
			startH = 1
			draw.text((1,0), self.title, font=self.font, fill=0)

		# If menu is longer than the display can handle, scroll menu with cursor
		if (len(self.opt) > maxDisp) and (self.selected >= int(maxDisp / 2)):
			offset = self.selected - 2

		# Draw the menu items
		for i in range(offset, len(self.opt)):
			opt = self.opt[i]
			truePos = (i-offset+startH)*scale
			if (i == self.selected): self.choiceDisp = truePos

			draw.rectangle([(0,truePos),(self.disp.width,truePos+scale-1)],fill=int(i != self.selected))

			text = self.opt[i]['text']
			alt_text = self.opt[i]['alt'] if 'alt' in self.opt[i] else text

			draw.text((1,truePos), '> ' + (alt_text if i == self.selected else text), font=self.font, fill=int(i == self.selected))

		# If menu is longer than the display can handle, show scroll bar
		if len(self.opt) > maxDisp:
			#outline
			draw.rectangle([(self.disp.width-scale,0),(self.disp.width-1,self.disp.height-1)],fill=1,outline=0)

			#nav bar
			max = self.disp.height - 3
			min = 2
			barpos = ((max-min) * self.selected / len(self.opt)) + min
			draw.rectangle([(self.disp.width-scale+2,barpos),(self.disp.width-3,barpos+scale-5)],fill=0)

		self.disp.ShowImage(self.disp.getbuffer(image))

	def up(self, _ = None):
		self.selected -= 1
		if self.selected < 0:
			self.selected = len(self.opt) - 1

	def down(self, _ = None):
		self.selected += 1
		if self.selected >= len(self.opt):
			self.selected = 0

	def select(self, _=None):
		return self.opt[self.selected]

from PIL import Image, ImageDraw, ImageFont

class textMenu(object):
	def __init__(self, disp):
		self.opt = []
		self.autoDisplay = False
		self.disp = disp
		self.font = ImageFont.load_default()
		self.selected = 0
		self.choices = []
		self.choiceDisp = 0

	def options(self, optTree):
		self.opt = optTree

	def currentOpt(self):
		# trace menu tree
		opt = self.opt
		for i in self.choices:
			opt = opt[i[0]][1]
		return opt

	def draw(self, status):
		self.autoDisplay = status
		if status:
			self.selected = 0
			self.display()
		else:
			self.disp.clear()

	def display(self):
		image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
		draw = ImageDraw.Draw(image)

		pos = 0
		scale = 11
		offset = 0
		maxDisp = int(self.disp.height / scale) + 1
		startW = 0

		# trace menu tree
		optlist = self.opt
		for i in self.choices:
			optlist = optlist[i[0]][1]
			draw.rectangle([(startW,i[1]),(startW+4,i[1]+scale-1)],fill=0)
			startW += 5


		# If menu is longer than the display can handle, scroll menu with cursor
		if (len(optlist) > maxDisp) and (self.selected >= int(maxDisp / 2)):
			offset = self.selected - 2

		# Draw the menu items
		for i in range(offset, len(optlist)):
			opt = optlist[i]
			truePos = (i-offset)*scale
			if (i == self.selected): self.choiceDisp = truePos

			draw.rectangle([(startW,truePos),(self.disp.width,truePos+scale-1)],fill=int(i != self.selected))

			if type(opt) is not str:
				draw.text((startW+1,truePos), opt[0], font=self.font, fill=int(i == self.selected))
				draw.text((self.disp.width-(scale*2),truePos), '>', font=self.font, fill=int(i == self.selected))
			else:
				draw.text((startW+1,truePos), opt, font=self.font, fill=int(i == self.selected))

			pos += 1

		# If menu is longer than the display can handle, show scroll bar
		if len(optlist) > maxDisp:
			#outline
			draw.rectangle([(self.disp.width-scale,0),(self.disp.width-1,self.disp.height-1)],fill=1,outline=0)

			#nav bar
			max = self.disp.height - 3
			min = 2
			barpos = ((max-min) * self.selected / len(optlist)) + min
			draw.rectangle([(self.disp.width-scale+2,barpos),(self.disp.width-3,barpos+scale-5)],fill=0)

		self.disp.ShowImage(self.disp.getbuffer(image))

	def up(self):
		self.selected -= 1
		if self.selected < 0:
			self.selected = len(self.currentOpt()) - 1

		if self.autoDisplay: self.display()

	def down(self):
		self.selected += 1
		if self.selected >= len(self.currentOpt()):
			self.selected = 0

		if self.autoDisplay: self.display()

	def select(self, choice=None):
		if choice == None: choice = self.selected

		opt = self.currentOpt()

		if type(opt[choice]) is not str:
			if not (choice >= 0 and choice < len(opt)): return
			self.choices += [(choice,self.choiceDisp)]
			self.selected = 0
			if self.autoDisplay: self.display()

	def back(self):
		if len(self.choices):
			opt = self.choices.pop()
			self.selected = opt[0]
			self.choiceDisp = opt[1]
			if self.autoDisplay: self.display()

	def terminal(self):
		return type(self.currentOpt()[self.selected]) is str

	def path(self):
		result = []
		# trace menu tree
		opt = self.opt
		for i in self.choices:
			opt = opt[i[0]]
			result += [opt[0]]
			opt = opt[1]

		opt = opt[self.selected]
		result += [opt if type(opt) is str else opt[0]]

		return '/'.join(result)

	def choice(self):
		result = []
		# trace menu tree
		opt = self.opt
		for i in self.choices:
			opt = opt[i[0]][1]
			result += [i[0]]
		result += [self.selected]

		return result

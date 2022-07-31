from PIL import Image, ImageDraw, ImageFont

class keyboard(object):
	def __init__(self, disp):
		self.autoDisplay = False
		self.disp = disp
		self.font = ImageFont.load_default()
		self.x = 0
		self.y = 0
		self.text = ''
		self.keys = ['`1234567890-=','qwertyuiop[]\\','asdfghjkl;\'  ','zxcvbnm,./   ']
		self.altKeys = ['~!@#$%^&*()_+','QWERTYUIOP{}|','ASDFGHJKL:"  ','ZXCVBNM<>?   ']
		self.shift = False
		self.hidden = False

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

		scale = 11
		scaleX = 8
		y = 0
		for row in (self.altKeys if self.shift else self.keys):
			x = 0
			for key in row:
				draw.rectangle([(x*(scaleX),y*scale + 2),((x+1)*(scaleX)-2,(y+1)*scale+1)],fill=int(x != self.x or y != self.y))
				draw.text((x*(scaleX) + 1,y*scale + 1),key,font=self.font,fill=int(x == self.x and y == self.y))
				x += 1
			y += 1

		# Remind user what the 3 buttons do.
		draw.text((self.disp.width-scale-1, 2),'aA',fill=0)
		draw.text((self.disp.width-scale-1, 20),' »',fill=0)
		draw.text((self.disp.width-scale-1, 38),' «',fill=0)
		draw.line([(self.disp.width-scale-3,0),(self.disp.width-scale-3,self.disp.height-scale-1)],fill=0)

		draw.line([(0,self.disp.height-scale-1),(self.disp.width,self.disp.height-scale-1)],fill=0)
		if self.hidden:
			draw.text((1,self.disp.height-scale),'*'*len(self.text),fill=0)
		else:
			draw.text((1,self.disp.height-scale),self.text,fill=0)

		self.disp.ShowImage(self.disp.getbuffer(image))

	def toggleShift(self, _=None):
		self.shift = not self.shift
		if self.autoDisplay: self.display()

	def __boundXY(self):
		self.y %= len(self.altKeys if self.shift else self.keys)
		self.x %= len((self.altKeys if self.shift else self.keys)[self.y])

	def left(self, _=None):
		self.x -= 1
		self.__boundXY()
		if self.autoDisplay: self.display()

	def right(self, _=None):
		self.x += 1
		self.__boundXY()
		if self.autoDisplay: self.display()

	def up(self, _=None):
		self.y -= 1
		self.__boundXY()
		if self.autoDisplay: self.display()

	def down(self, _=None):
		self.y += 1
		self.__boundXY()
		if self.autoDisplay: self.display()

	def select(self, _=None):
		self.text += (self.altKeys if self.shift else self.keys)[self.y][self.x]
		if self.autoDisplay: self.display()

	def backspace(self, _=None):
		self.text = self.text[:-1]
		if self.autoDisplay: self.display()

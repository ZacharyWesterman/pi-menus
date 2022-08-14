class Keyboard:
	def __init__(self, display):
		self.display = display
		self.x = 0
		self.y = 0
		self.text = ''
		self.keys = ['`1234567890-=','qwertyuiop[]\\','asdfghjkl;\'  ','zxcvbnm,./   ']
		self.altKeys = ['~!@#$%^&*()_+','QWERTYUIOP{}|','ASDFGHJKL:"  ','ZXCVBNM<>?   ']
		self.shift = False
		self.hidden = False
		self.is_displaying = False

	async def show(self):
		if self.is_displaying:
			return

		self.is_displaying = True

		self.display.clear()

		scale = 11
		scaleX = 8
		y = 0
		for row in (self.altKeys if self.shift else self.keys):
			x = 0
			for key in row:
				if x == self.x and y == self.y:
					self.display.rect(bounds=[(x*scaleX, y*scale + 2),((x+1)*(scaleX)-2,(y+1)*scale+1)], fill=True)

				self.display.text(x * scaleX, y * scale, key, inverted=(x == self.x and y == self.y))
				x += 1
			y += 1

		# Remind user what the 3 buttons do.
		self.display.text(-1, 2, 'aA')
		self.display.text(-1, 20, ' »')
		self.display.text(-1, 38, ' «')

		#Make some nice borders
		vertical_bar = self.display.max_width() - 2*scale
		horizontal_bar = self.display.max_height() - int(1.5*scale)
		self.display.vline(vertical_bar, 0, horizontal_bar)
		self.display.hline(0, horizontal_bar, self.display.max_width())

		#Show what user has already input
		msg = '*'*len(self.text) if self.hidden else self.text
		self.display.put(-1, msg)

		await self.display.display()

		self.is_displaying = False

	async def toggleShift(self, _=None):
		self.shift = not self.shift
		await self.show()

	def __boundXY(self):
		self.y %= len(self.altKeys if self.shift else self.keys)
		self.x %= len((self.altKeys if self.shift else self.keys)[self.y])

	async def left(self):
		self.x -= 1
		self.__boundXY()
		await self.show()

	async def right(self):
		self.x += 1
		self.__boundXY()
		await self.show()

	async def up(self):
		self.y -= 1
		self.__boundXY()
		await self.show()

	async def down(self):
		self.y += 1
		self.__boundXY()
		await self.show()

	async def select(self, _=None):
		self.text += (self.altKeys if self.shift else self.keys)[self.y][self.x]
		await self.show()

	async def backspace(self, _=None):
		self.text = self.text[:-1]
		await self.show()

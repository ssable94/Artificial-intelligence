class City:
	def __init__(self, given_ngb, given_color, given_color_list):
		self.ngb = given_ngb
		self.rvalue = len(given_color_list)
		self.degree = len(given_ngb)
		self.color = given_color
		self.color_list = given_color_list

	def color_it(self, given_color):
		if given_color in self.color_list:
			self.color = given_color
			del self.color_list[:]
			self.rvalue = 0
			return 1
		return -1

	def remove_color(self, given_color):
		if given_color in self.color_list:
			self.color_list.remove(given_color)
			self.rvalue -= 1
			return 1
		return -1

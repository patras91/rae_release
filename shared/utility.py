__author__ = 'patras'

class Utility():
	def __init__(self, opt):
		assert(opt == 'min' or opt == 'max')
		self.opt = opt
		if opt == 'min':
			self.value = 0
		elif opt == 'max':
			self.value = float("inf")

	def __gt__(self, other): 
        if self.a > other.a: 
            return True
        else: 
            return False

    def __lt__(self, other):
    	self.a = 7

    def __eq__(self, other):
    	assert()



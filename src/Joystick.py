import pygame

OK = [pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION, pygame.JOYAXISMOTION, pygame.KEYDOWN]
WIN_SIZE = (300, 50)

def gethatcode(ev):
	which = (ev.joy+1) << 12
	hat = ev.hat << 2
	if ev.value & pygame.HAT_UP == 0: value = 0
	elif ev.value & pygame.HAT_DOWN: value = 1
	elif ev.value & pygame.HAT_RIGHT: value = 2
	elif ev.value & pygame.HAT_LEFT: value = 3
	else: value = 0

	result = which | hat | value
	
	return "%04x" % result

def getbuttoncode(ev):
	which = (ev.joy + 1) << 12
	button = ev.button + 0x80
	
	result = which | button

	return "%04x" % result

def getaxiscode(ev):
	which = (ev.joy+1) << 12
	axis = ev.axis << 1
	#strange hack: the value is different from the C API
	if ev.value >= 1: value = 1
	else: value = 0

	result = which | axis | value
	
	return "%04x" % result

def getkeycode(ev):
	return "%04x" % ev.key

class Joystick:
	def __init__(self, iconfile):
		pygame.init()

		self.nbJoy = pygame.joystick.get_count()

		for i in range(self.nbJoy):
			pygame.joystick.Joystick(i).init()
		self.icon = pygame.image.load(iconfile)

	def get_binding(self):
		pygame.display.init()
		pygame.event.clear()
		pygame.display.set_mode(WIN_SIZE)
		pygame.display.set_caption("Control configuration")
		pygame.display.set_icon(self.icon)

		done = False

		while not done:
			pygame.event.pump()
			ev_list = pygame.event.get(OK)

			for ev in ev_list:
				done = True
				if ev.type == pygame.JOYHATMOTION:
					res = gethatcode(ev)
					#print "JOY HAT code:", res
				elif ev.type == pygame.JOYBUTTONDOWN:
					res = getbuttoncode(ev)
					#print "JOY BUTTON code:", res
				elif ev.type == pygame.JOYAXISMOTION:
					res = getaxiscode(ev)
					#print "JOY AXIS code:", res
				elif ev.type == pygame.KEYDOWN:
					if ev.key == pygame.K_ESCAPE:
						res = None
					else:
						res = getkeycode(ev)
						#print "KEY code:", res
					
				else: #outch?
					res = None
		pygame.display.quit()
		return res

	def __del__(self):
		pygame.quit()

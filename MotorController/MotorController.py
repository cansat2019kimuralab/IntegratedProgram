import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
import Motor

mpL = 0
mpR = 0

class _Getch:
	"""Gets a single character from standard input.  Does not echo to the
screen."""
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self): return self.impl()


class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()
 
if __name__ == "__main__":
	while True:
		getch = _Getch()
		x = getch()
		if (x == b's'):
			print("STRAIGHT")		
			Motor.motor(30, 30, 1)
			mpL = 30
			mpR = 30
			print("mpL: ", mpL, "mpR: ", mpR)
			continue
		if (x == b"v"):
			print('REVERSE')
			Motor.motor(-30,- 30, 1)
			Motor.motor(0, 0, 3)
			mpL = 0
			mpR = 0
			print("mpL: ", mpL, "mpR: ", mpR)
			continue
		if x == b'e':
			print('END')
			Motor.motor(0, 0, 5)
			sys.exit()
		if 0 < mpL < 60 and 0 < mpR < 60:
			if (x == b'a'):
				print("ACCEL")
				Motor.motor(mpL + 1, mpR + 1, 0.01)
				mpL = mpL + 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b'r'):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR - 1, 0.01)
				mpL = mpL + 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR + 1, 0.01)
				mpL = mpL - 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL - 1, mpR - 1, 0.01)
				mpL = mpL - 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")
				
		elif mpR == 60 and mpL == 60:
			if (x == b"a"):
				print("cannot ACCEL")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL - 1, mpR - 1, 0.01)
				mpL = mpL - 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR, 0.01)
				mpL = mpL - 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL, mpR - 1, 0.01)
				mpL = mpL
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")

		elif mpL == 0 and mpR == 0:
			if (x == b"a"):
				print("ACCEL")
				Motor.motor(mpL + 1, mpR + 1, 0.01)
				mpL = mpL + 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("Already stopped")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"l"):
				print("LEFT")
				Motor.motor(mpL, mpR + 1, 0.01)
				mpL = mpL
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR, 0.01)
				mpL = mpL + 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")

		elif mpL == 0 and mpR == 60:
			if (x == b"a"):
				print("cannot ACCEL")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL, mpR - 1, 0.01)
				mpL = mpL
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"l"):
				print("max LEFT")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR - 1, 0.01)
				mpL = mpL + 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")

		elif mpL == 60 and mpR == 0:
			if (x == b"a"):
				print("cannot ACCEL")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL- 1, mpR, 0.01)
				mpL = mpL - 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR + 1, 0.01)
				mpL = mpL - 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"r"):
				print(" max RIGHT")
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")

		elif mpL == 60 or mpR == 60:
			if (x == b"a"):
				print("cannot ACCEL")
				print("mpL: ", mpL, "mpR: ", mpR)
			elif (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL - 1, mpR - 1, 0.01)
				mpL = mpL - 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpR == 60 and (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR - 1, 0.01)
				mpL = mpL + 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpR == 60 and (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR, 0.01)
				mpL = mpL - 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpL == 60 and (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL, mpR - 1, 0.01)
				mpL = mpL
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpL == 60 and (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR + 1, 0.01)
				mpL = mpL - 1
				mpR = mpR + 1
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")

		elif mpL == 0 or mpR == 0:
			if (x == b"a"):
				print("ACCEL")
				Motor.motor(mpL + 1, mpR + 1, 0.01)
				mpL = mpL + 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpR == 0 and (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL - 1, mpR, 0.01)
				mpL = mpL - 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpL == 0 and (x == b"b"):
				print("BRAKE")
				Motor.motor(mpL, mpR - 1, 0.01)
				mpL = mpL
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpR == 0 and (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR, 0.01)
				mpL = mpL + 1
				mpR = mpR
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpR == 0 and (x == b"l"):
				print("LEFT")
				Motor.motor(mpL - 1, mpR + 1, 0.01)
				mpL = mpL - 1
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpL == 0 and (x == b"r"):
				print("RIGHT")
				Motor.motor(mpL + 1, mpR - 1, 0.01)
				mpL = mpL + 1
				mpR = mpR - 1
				print("mpL: ", mpL, "mpR: ", mpR)
			elif mpL == 0 and (x == b"l"):
				print("LEFT")
				Motor.motor(mpL, mpR + 1, 0.01)
				mpL = mpL
				mpR = mpR + 1
				print("mpL: ", mpL, "mpR: ", mpR)
			else:
				print(x,"has no command")
				print("Please input / a:ACCEL / b:BRAKE / s:STRAIGHT / l:LEFT / r:RIGHT /")


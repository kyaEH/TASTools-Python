from pywinauto import Desktop, Application
import time
import asyncio
import ctypes
import _thread
import signal
import sys

SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
UP = 0x48
LEFT = 0x4B
RIGHT = 0x4D
DOWN = 0x50
ENTER = 0x1C
ESC = 0x01
TWO = 0x03
BACKSPACE = 0x0E

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
	_fields_ = [("wVk", ctypes.c_ushort),
				("wScan", ctypes.c_ushort),
				("dwFlags", ctypes.c_ulong),
				("time", ctypes.c_ulong),
				("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
	_fields_ = [("uMsg", ctypes.c_ulong),
				("wParamL", ctypes.c_short),
				("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
	_fields_ = [("dx", ctypes.c_long),
				("dy", ctypes.c_long),
				("mouseData", ctypes.c_ulong),
				("dwFlags", ctypes.c_ulong),
				("time", ctypes.c_ulong),
				("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
	_fields_ = [("ki", KeyBdInput),
				("mi", MouseInput),
				("hi", HardwareInput)]


class Input(ctypes.Structure):
	_fields_ = [("type", ctypes.c_ulong),
				("ii", Input_I)]


def PressKey(hexKeyCode):
	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
	x = Input(ctypes.c_ulong(1), ii_)
	ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
						ctypes.pointer(extra))
	x = Input(ctypes.c_ulong(1), ii_)
	ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def main():
	print("Main")
	focusWindow()
	#initTrack()
	readFile()
	

def focusWindow():
	app = Application()
	app.connect(title_re="TrackMania")
	app_dialog = app.top_window()
	app_dialog.minimize()
	app_dialog.restore()


def initTrack():
	print("initTrack")
	time.sleep(1)
	PressKey(BACKSPACE)
	print("3")
	time.sleep(0.6)
	print("2")
	time.sleep(1)
	print("1")
	time.sleep(1)
	print("GO!")

def readFile():
	file1 = open('file.txt', 'r')
	Lines = file1.readlines()
	count = 0
	test = 0
	initTrack()
	for line in Lines:
		count += 1
		arr = line.strip().split(" ")
		arr[0] = int(arr[0])
		time.sleep((arr[0]-test)/1000)
		_thread.start_new_thread ( gameInput,(arr[0],arr[1],arr[2]) )
		test = arr[0]
		#time.sleep(int(arr[2]))
		#asyncio.run(gameInput(arr[0],arr[1],arr[2]))
	print('Fin reached? Press Ctrl+C to close the program')
	time.sleep(60)

def gameInput(startTime,key,duration):
	
	if key == "UP":
		key = UP
	if key == "BRAKE":
		key = DOWN
	if key == "LEFT":
		key = LEFT
	if key == "RIGHT":
		key = RIGHT
	#time.sleep(int(startTime)/1000)
	print("startTime: {}, key: {}, Duration: {}ms".format(startTime,key,duration))
	PressKey(key)
	time.sleep(int(duration)/1000)
	ReleaseKey(key)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    ReleaseKey(UP)
    ReleaseKey(LEFT)
    ReleaseKey(RIGHT)
    ReleaseKey(DOWN)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
	main()
	'''
	while (True):
		print("UP pressed")
		PressKey(UP)
		time.sleep(1)
		ReleaseKey(UP)
		time.sleep(1)
	'''
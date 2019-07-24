import sys

from pynput import keyboard
from pynput.keyboard import Controller, Key

from massivemacro import main

COMMAND_KEY = Key.cmd_l if sys.platform == "darwin" else Key.ctrl_l

ALL_MODIFIERS = set()
ALL_KEY_BINDINGS = set()


class EnterKeyBinding(object):
	def __init__(self, massivizer, *args):
		self.massivizer = massivizer
		self.modifiers = set()

		for modifier in args:
			self.modifiers.add(modifier)
			ALL_MODIFIERS.add(modifier)

		ALL_KEY_BINDINGS.add(self)

	@property
	def massivizer(self):
		return self.__massivizer

	@massivizer.setter
	def massivizer(self, massivizer):
		for key_binding in ALL_KEY_BINDINGS:
			if key_binding is not self and key_binding.__massivizer == massivizer:
				key_binding.__massivizer = self.__massivizer

		self.__massivizer = massivizer


key_controller = Controller()
currently_pressed = set()


def press(key):
	key_controller.press(key)


def release(key):
	key_controller.release(key)


def command(key):
	key_controller.press(COMMAND_KEY)
	key_controller.press(key)
	key_controller.release(key)
	key_controller.release(COMMAND_KEY)


def on_press(key):
	if key != Key.enter:
		if key == Key.ctrl_l or key == Key.ctrl_r:
			key = Key.ctrl
		elif key == Key.alt_l or key == Key.alt_r:
			key = Key.alt
		elif key == Key.shift_l or key == Key.shift_r:
			key = Key.shift

		if key in ALL_MODIFIERS:
			currently_pressed.add(key)
		return

	for key_binding in ALL_KEY_BINDINGS:
		if currently_pressed == key_binding.modifiers:
			for modifier in ALL_MODIFIERS:
				release(modifier)

			main.handle_massivization(key_binding.massivizer)
			return


def on_release(key):
	try:
		currently_pressed.remove(key)
	except KeyError:
		pass


def start_listener(gui):
	if gui:
		keyboard.Listener(on_press=on_press, on_release=on_release).start()

	else:
		with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
			listener.join()

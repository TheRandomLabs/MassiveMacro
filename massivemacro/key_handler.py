import sys
import threading

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
active_modifiers = set()


def press(key):
	key_controller.press(key)


def release(key):
	key_controller.release(key)


def command(key):
	key_controller.press(COMMAND_KEY)
	key_controller.press(key)
	key_controller.release(key)
	key_controller.release(COMMAND_KEY)


def translate_modifier(key):
	if key == Key.ctrl_l or key == Key.ctrl_r:
		return Key.ctrl

	if key == Key.alt_l or key == Key.alt_r:
		return Key.alt

	if key == Key.shift_l or key == Key.shift_r:
		return Key.shift

	return key


def on_press(key):
	if key != Key.enter:
		if translate_modifier(key) in ALL_MODIFIERS:
			active_modifiers.add(key)

		return

	for key_binding in ALL_KEY_BINDINGS:
		if len(key_binding.modifiers) != len(active_modifiers):
			continue

		all_modifiers_found = True

		for modifier in key_binding.modifiers:
			modifier_found = False

			for active_modifier in active_modifiers:
				if translate_modifier(active_modifier) == modifier:
					modifier_found = True

			if not modifier_found:
				all_modifiers_found = False
				break

		if all_modifiers_found:
			main.handle_massivization(key_binding.massivizer)
			return


def on_release(key):
	try:
		active_modifiers.remove(key)
	except KeyError:
		pass


def start_listener(gui):
	if gui:
		thread = threading.Thread(target=actually_start_listener)
		thread.start()
	else:
		actually_start_listener()


def actually_start_listener():
	while True:
		with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
			try:
				listener.join()
			except KeyError:
				print(
					"Non-fatal error. MassiveMacro will continue to run."
				)

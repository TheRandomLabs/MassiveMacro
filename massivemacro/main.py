import sys
import time

from pynput.keyboard import Key

from massivemacro import clipboard, key_handler, massivemacro_gui, massivizers

MESSAGE_SEND_INTERVAL = 0.08


def handle_massivization(massivizer):
	# Make sure none of the modifiers get in the way
	key_handler.release(Key.cmd_l)
	key_handler.release(Key.cmd_r)
	key_handler.release(Key.ctrl_l)
	key_handler.release(Key.ctrl_r)
	key_handler.release(Key.shift_l)
	key_handler.release(Key.shift_r)
	key_handler.release(Key.alt_l)
	key_handler.release(Key.alt_r)
	key_handler.release('a')
	key_handler.release('x')
	key_handler.release('v')
	key_handler.release(Key.enter)

	original_clipboard = clipboard.get()
	clipboard.empty()

	key_handler.command('a')
	key_handler.command('x')

	clipboard.wait()

	massivized = massivizer.massivize(clipboard.get())

	for message in massivized:
		clipboard.empty()
		clipboard.copy(message)
		clipboard.wait()

		key_handler.command('v')

		if sys.platform == "darwin":
			time.sleep(MESSAGE_SEND_INTERVAL)

		key_handler.press(Key.enter)
		key_handler.release(Key.enter)

		time.sleep(MESSAGE_SEND_INTERVAL)

	clipboard.copy(original_clipboard)


def main(gui):
	clipboard.ensure_available()
	massivizers.init(gui)

	if gui:
		massivemacro_gui.init()

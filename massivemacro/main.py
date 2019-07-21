import sys
import time

from pynput.keyboard import Key

from massivemacro import clipboard, key_handler, massivemacro_gui, massivizers

MESSAGE_SEND_INTERVAL = 0.08


def handle_massivization(massivizer):
	print(massivizers.VANESSA.case_behavior.name)

	original_clipboard = clipboard.get()
	clipboard.empty()

	key_handler.release(Key.enter)
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


def main():
	clipboard.ensure_available()
	massivizers.init()
	massivemacro_gui.init()

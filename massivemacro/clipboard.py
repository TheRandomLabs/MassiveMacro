import sys
import time

import pyperclip

CLIPBOARD_POLL_INTERVAL = 0.005
CLIPBOARD_MAX_WAIT_TIME = 0.3
MAX_CLIPBOARD_POLLS = int(CLIPBOARD_MAX_WAIT_TIME / CLIPBOARD_POLL_INTERVAL)


def ensure_available():
	try:
		pyperclip.paste()
	except pyperclip.PyperclipException as e:
		if "could not find a copy/paste mechanism" in str(e):
			message = "Could not find a copy/paste mechanism."

			if sys.platform == "linux":
				message += " Please ensure xclip is installed."

			print(message, file=sys.stderr)
			sys.exit()

		raise


def copy(text):
	pyperclip.copy(text)


def get():
	return pyperclip.paste()


def empty():
	pyperclip.copy("")

	for i in range(0, MAX_CLIPBOARD_POLLS):
		if pyperclip.paste():
			time.sleep(CLIPBOARD_POLL_INTERVAL)


def wait():
	for i in range(0, MAX_CLIPBOARD_POLLS):
		if not pyperclip.paste():
			time.sleep(CLIPBOARD_POLL_INTERVAL)

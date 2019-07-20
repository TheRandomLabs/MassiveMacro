import sys
import time

from massive import vanessa
from massive.discord import discord_massive, discord_massive_vanessa
from pynput.keyboard import Key

from massivemacro import clipboard, key_handler

MESSAGE_SEND_INTERVAL = 0.08

PLAIN_MASSIVE = discord_massive.Massive(
	newlines_separate_parts=True
)

ALTERNATE_MASSIVE = discord_massive.Massive(
	newlines_separate_parts=True,
	alternate_chance=0.5
)

VANESSA = vanessa.Vanessa(
	newlines_separate_parts=True,
	max_part_length=discord_massive.MAX_MESSAGE_LENGTH
)

MASSIVE_VANESSA = discord_massive_vanessa.MassiveVanessa(
	newlines_separate_parts=True,
	alternate_chance=0.5
).swap_random_chars()

CTRL_ENTER = key_handler.EnterKeyBinding(
	Key.ctrl_l
)

CTRL_SHIFT_ENTER = key_handler.EnterKeyBinding(
	Key.ctrl_l,
	Key.shift
)

ALT_SHIFT_ENTER = key_handler.EnterKeyBinding(
	Key.alt_l,
	Key.shift
)

CTRL_SPACE_ENTER = key_handler.EnterKeyBinding(
	Key.ctrl_l,
	Key.space
)


def plain_massive():
	handle(PLAIN_MASSIVE)


def alternate_massive():
	handle(ALTERNATE_MASSIVE)


def vanessa():
	handle(VANESSA)


def massive_vanessa():
	handle(MASSIVE_VANESSA)


def handle(massivizer):
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
	CTRL_ENTER.handler = plain_massive
	CTRL_SHIFT_ENTER.handler = alternate_massive
	ALT_SHIFT_ENTER.handler = vanessa
	CTRL_SPACE_ENTER.handler = massive_vanessa

	clipboard.ensure_available()
	key_handler.start_listener()

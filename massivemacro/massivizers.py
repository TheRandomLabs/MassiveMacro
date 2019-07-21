from massive import vanessa
from massive.discord import discord_massive, discord_massive_vanessa
from pynput.keyboard import Key

from massivemacro import key_handler

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
	PLAIN_MASSIVE,
	Key.ctrl_l
)

CTRL_SHIFT_ENTER = key_handler.EnterKeyBinding(
	ALTERNATE_MASSIVE,
	Key.ctrl_l,
	Key.shift
)

ALT_SHIFT_ENTER = key_handler.EnterKeyBinding(
	VANESSA,
	Key.alt_l,
	Key.shift
)

CTRL_SPACE_ENTER = key_handler.EnterKeyBinding(
	MASSIVE_VANESSA,
	Key.ctrl_l,
	Key.space
)


def init():
	key_handler.start_listener()

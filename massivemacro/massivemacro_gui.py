import json
import os
import sys
from json import JSONDecodeError

from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QFont, QIcon, QRegExpValidator
from PyQt5.QtWidgets import QAction, QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, \
	QLineEdit, QMainWindow, QMenu, QSystemTrayIcon, QWidget, qApp
from massive import vanessa

from massivemacro import massivizers


# TODO move settings out so that they work with --no-gui
# noinspection PyArgumentList,DuplicatedCode
class MassiveMacroWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self.settings = MassiveMacroSettings.load()

		self.icon = QIcon(get_resource("icon.png"))
		self.setWindowIcon(self.icon)

		self.setMinimumSize(400, 0)
		self.setWindowTitle("MassiveMacro")
		self.widget = QWidget(self)
		self.setCentralWidget(self.widget)

		self.x = 0
		self.y = -1

		self.layout = QGridLayout(self)
		self.widget.setLayout(self.layout)

		self.pm_newlines_separate_messages = None
		self.pm_max_message_length = None
		self.pm_random_char_swap_chance = None

		self.am_newlines_separate_messages = None
		self.am_max_message_length = None
		self.am_random_char_swap_chance = None
		self.am_alternate_chance = None

		self.v_newlines_separate_messages = None
		self.v_max_message_length = None
		self.v_random_char_swap_chance = None
		self.v_case_behavior = None

		self.mv_newlines_separate_messages = None
		self.mv_max_message_length = None
		self.mv_random_char_swap_chance = None
		self.mv_alternate_chance = None
		self.mv_massive_chance = None

		self.minimize_to_tray = None
		self.tray_notification = None

		self.tray_icon = None

		self.setFont(QFont("Segoe UI"))
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

		self.add_widgets()
		self.init_system_tray()

	def add_widgets(self):
		self.add_plain_massive_widgets()
		self.add_alternate_massive_widgets()
		self.add_vanessa_widgets()
		self.add_massive_vanessa_widgets()
		self.add_system_tray_widgets()

	def add_plain_massive_widgets(self):
		self.add_widget(self.get_label("Plain massive", True), True)

		self.pm_newlines_separate_messages = self.get_newlines_separate_parts(
			self.settings.pm_newlines_separate_messages,
			massivizers.PLAIN_MASSIVE
		)
		self.add_widget(self.pm_newlines_separate_messages, True)

		self.pm_max_message_length = self.get_max_message_length(
			self.settings.pm_max_message_length,
			massivizers.PLAIN_MASSIVE
		)
		self.add_widget(self.pm_max_message_length, False)

		self.pm_random_char_swap_chance = self.get_random_char_swap_chance(
			self.settings.pm_random_char_swap_chance,
			massivizers.PLAIN_MASSIVE
		)
		self.add_widget(self.pm_random_char_swap_chance, False)

	def add_alternate_massive_widgets(self):
		self.add_widget(self.get_label("Alternate massive", True), True)

		self.am_newlines_separate_messages = self.get_newlines_separate_parts(
			self.settings.am_newlines_separate_messages,
			massivizers.ALTERNATE_MASSIVE
		)
		self.add_widget(self.am_newlines_separate_messages, True)

		self.am_max_message_length = self.get_max_message_length(
			self.settings.am_max_message_length,
			massivizers.ALTERNATE_MASSIVE
		)
		self.add_widget(self.am_max_message_length, False)

		self.am_random_char_swap_chance = self.get_random_char_swap_chance(
			self.settings.am_random_char_swap_chance,
			massivizers.ALTERNATE_MASSIVE
		)
		self.add_widget(self.am_random_char_swap_chance, False)

		self.am_alternate_chance = self.get_alternate_chance(
			self.settings.am_alternate_chance,
			massivizers.ALTERNATE_MASSIVE
		)
		self.add_widget(self.am_alternate_chance, False)

	def add_vanessa_widgets(self):
		self.add_widget(self.get_label("Vanessa", True), True)

		self.v_newlines_separate_messages = self.get_newlines_separate_parts(
			self.settings.v_newlines_separate_messages,
			massivizers.VANESSA
		)
		self.add_widget(self.v_newlines_separate_messages, True)

		self.v_max_message_length = self.get_max_message_length(
			self.settings.v_max_message_length,
			massivizers.VANESSA
		)
		self.add_widget(self.v_max_message_length, False)

		self.v_random_char_swap_chance = self.get_random_char_swap_chance(
			self.settings.v_random_char_swap_chance,
			massivizers.VANESSA
		)
		self.add_widget(self.v_random_char_swap_chance, False)

		self.add_widget(self.get_label("Case behavior:", False), True)

		self.v_case_behavior = self.get_combo_box(
			self.settings.v_case_behavior - 1,
			lambda index: (
				set_case_behavior(index)
			),
			"Start lowercase",
			"Always start lowercase",
			"Start uppercase",
			"Always start uppercase"
		)
		self.add_widget(self.v_case_behavior, False)

	def add_massive_vanessa_widgets(self):
		self.add_widget(self.get_label("Massive Vanessa", True), True)

		self.mv_newlines_separate_messages = self.get_newlines_separate_parts(
			self.settings.mv_newlines_separate_messages,
			massivizers.MASSIVE_VANESSA
		)
		self.add_widget(self.mv_newlines_separate_messages, True)

		self.mv_max_message_length = self.get_max_message_length(
			self.settings.mv_max_message_length,
			massivizers.MASSIVE_VANESSA
		)
		self.add_widget(self.mv_max_message_length, False)

		self.mv_random_char_swap_chance = self.get_random_char_swap_chance(
			self.settings.mv_random_char_swap_chance,
			massivizers.MASSIVE_VANESSA
		)
		self.add_widget(self.mv_random_char_swap_chance, False)

		self.mv_alternate_chance = self.get_alternate_chance(
			self.settings.mv_alternate_chance,
			massivizers.MASSIVE_VANESSA
		)
		self.add_widget(self.mv_alternate_chance, False)

		self.add_widget(self.get_label("Massive chance:", False), True)

		self.mv_massive_chance = self.get_double_line_edit(
			str(self.settings.mv_massive_chance),
			lambda text: (
				set_massive_chance(text)
			)
		)
		self.add_widget(self.mv_massive_chance, False)

	def get_newlines_separate_parts(self, checked, massivizer):
		return self.get_check_box(
			"Newlines separate messages",
			checked,
			on_state_changed=lambda checked: (
				setattr(massivizer, "newlines_separate_parts", checked)
			)
		)

	def get_max_message_length(self, length, massivizer):
		self.add_widget(self.get_label("Max message length:", False), True)
		return self.get_line_edit(
			str(length),
			QRegExpValidator(QRegExp("[1-9][0-9]*")),
			lambda text: (
				set_max_message_length(massivizer, text)
			)
		)

	def get_random_char_swap_chance(self, chance, massivizer):
		self.add_widget(self.get_label("Random character swap chance:", False), True)
		return self.get_double_line_edit(
			str(chance),
			lambda text: (
				set_random_char_swap_chance(massivizer, text)
			)
		)

	def get_alternate_chance(self, chance, massivizer):
		self.add_widget(self.get_label("Alternate emoji chance:", False), True)
		return self.get_double_line_edit(
			str(chance),
			lambda text: (
				set_alternate_chance(massivizer, text)
			)
		)

	def add_system_tray_widgets(self):
		self.add_widget(self.get_label("System tray", True), True)

		self.minimize_to_tray = self.get_check_box(
			"Minimize to system tray",
			self.settings.minimize_to_tray
		)
		self.add_widget(self.minimize_to_tray, True)

		self.tray_notification = self.get_check_box(
			"Display notification",
			self.settings.tray_notification
		)
		self.add_widget(self.tray_notification, False)

	def get_label(self, text, bold):
		label = QLabel(text, self)

		font = QFont()
		font.setBold(bold)

		label.setFont(font)
		return label

	def get_check_box(self, text, checked, on_state_changed=lambda checked: None):
		check_box = QCheckBox(text)
		check_box.setChecked(checked)
		on_state_changed(checked)
		check_box.stateChanged.connect(lambda: (
			on_state_changed(check_box.isChecked()),
			self.settings.save()
		))
		return check_box

	def get_line_edit(self, text, validator, on_text_changed):
		line_edit = QLineEdit()
		line_edit.setText(text)
		line_edit.setValidator(validator)
		on_text_changed(text)
		line_edit.textChanged.connect(lambda: (
			on_text_changed(line_edit.text()),
			self.settings.save()
		))
		return line_edit

	def get_double_line_edit(self, text, on_text_changed):
		return self.get_line_edit(
			text,
			QRegExpValidator(QRegExp("(^1\\.0$)|(^1[\\.]?$)|(^0\\.[0-9]*$)")),
			on_text_changed
		)

	def get_combo_box(self, index, on_item_selected, *items):
		combo_box = QComboBox(self)
		combo_box.addItems(items)
		combo_box.setCurrentIndex(index)
		on_item_selected(index)
		combo_box.currentIndexChanged.connect(lambda: (
			on_item_selected(combo_box.currentIndex()),
			self.settings.save()
		))
		return combo_box

	def add_widget(self, widget, new_line):
		if new_line:
			self.y += 1
			self.x = 0
		else:
			self.x += 1

		self.layout.addWidget(widget, self.y, self.x)

	def add_item(self, widget, new_line):
		if new_line:
			self.y += 1
			self.x = 0
		else:
			self.x += 1

		self.layout.addItem(widget, self.y, self.x)

	def init_system_tray(self):
		self.tray_icon = QSystemTrayIcon(self.icon, parent=self)
		self.tray_icon.setToolTip("MassiveMacro")
		self.tray_icon.activated.connect(self.show)

		show_action = QAction("Show", self)
		hide_action = QAction("Hide", self)
		quit_action = QAction("Exit", self)

		show_action.triggered.connect(self.show)
		hide_action.triggered.connect(self.hide)
		quit_action.triggered.connect(qApp.quit)

		tray_menu = QMenu()
		tray_menu.addAction(show_action)
		tray_menu.addAction(hide_action)
		tray_menu.addAction(quit_action)

		self.tray_icon.setContextMenu(tray_menu)
		self.tray_icon.show()

	def init(self):
		self.move(QApplication.desktop().screen().rect().center() - self.widget.rect().center())
		self.setFixedSize(self.size())

	def closeEvent(self, event):
		if self.settings.minimize_to_tray:
			event.ignore()
			self.hide()

			if self.settings.tray_notification:
				self.tray_icon.showMessage(
					"MassiveMacro",
					"MassiveMacro was minimized to the system tray.",
					self.icon,
					2000
				)


def set_max_message_length(massivizer, text):
	massivizer.max_part_length = int(text) if text else 0


def set_random_char_swap_chance(massivizer, text):
	massivizer.random_char_swap_chance = float(text) if text else 0.0


def set_alternate_chance(massivizer, text):
	massivizer.alternate_chance = float(text) if text else 0.0


def set_case_behavior(index):
	massivizers.VANESSA.case_behavior = vanessa.CaseBehavior(index + 1)


def set_massive_chance(text):
	massivizers.MASSIVE_VANESSA.massive_chance = float(text) if text else 0.0


window = None


# noinspection DuplicatedCode
class MassiveMacroSettings(object):
	def __init__(self, **entries):
		self.pm_newlines_separate_messages = True
		self.pm_max_message_length = massivizers.PLAIN_MASSIVE.max_part_length
		self.pm_random_char_swap_chance = massivizers.PLAIN_MASSIVE.random_char_swap_chance

		self.am_newlines_separate_messages = True
		self.am_max_message_length = massivizers.ALTERNATE_MASSIVE.max_part_length
		self.am_random_char_swap_chance = massivizers.ALTERNATE_MASSIVE.random_char_swap_chance
		self.am_alternate_chance = massivizers.ALTERNATE_MASSIVE.alternate_chance

		self.v_newlines_separate_messages = True
		self.v_max_message_length = massivizers.VANESSA.max_part_length
		self.v_random_char_swap_chance = massivizers.VANESSA.random_char_swap_chance
		self.v_case_behavior = massivizers.VANESSA.case_behavior.value

		self.mv_newlines_separate_messages = True
		self.mv_max_message_length = massivizers.MASSIVE_VANESSA.max_part_length
		self.mv_random_char_swap_chance = massivizers.MASSIVE_VANESSA.random_char_swap_chance
		self.mv_alternate_chance = massivizers.MASSIVE_VANESSA.alternate_chance
		self.mv_massive_chance = massivizers.MASSIVE_VANESSA.massive_chance

		self.minimize_to_tray = True
		self.tray_notification = True

		self.__dict__.update(entries)

		self.__save()

	def save(self):
		self.pm_newlines_separate_messages = window.pm_newlines_separate_messages.isChecked()
		self.pm_max_message_length = get_int(window.pm_max_message_length.text())
		self.pm_random_char_swap_chance = get_float(window.pm_random_char_swap_chance.text())

		self.am_newlines_separate_messages = window.am_newlines_separate_messages.isChecked()
		self.am_max_message_length = get_int(window.am_max_message_length.text())
		self.am_random_char_swap_chance = get_float(window.am_random_char_swap_chance.text())
		self.am_alternate_chance = get_float(window.am_alternate_chance.text())

		self.v_newlines_separate_messages = window.v_newlines_separate_messages.isChecked()
		self.v_max_message_length = get_int(window.v_max_message_length.text())
		self.v_random_char_swap_chance = get_float(window.v_random_char_swap_chance.text())
		self.v_case_behavior = vanessa.CaseBehavior(window.v_case_behavior.currentIndex() + 1).value

		self.mv_newlines_separate_messages = window.mv_newlines_separate_messages.isChecked()
		self.mv_max_message_length = get_int(window.mv_max_message_length.text())
		self.mv_random_char_swap_chance = get_float(window.mv_random_char_swap_chance.text())
		self.mv_alternate_chance = get_float(window.mv_alternate_chance.text())
		self.mv_massive_chance = get_float(window.mv_massive_chance.text())

		self.minimize_to_tray = window.minimize_to_tray.isChecked()
		self.tray_notification = window.tray_notification.isChecked()
		self.__save()

	def __save(self):
		with open("MassiveMacro.json", "w") as file:
			file.write(json.dumps(self.__dict__, indent=4).replace("    ", "\t") + "\n")

	@classmethod
	def load(cls):
		try:
			with open("MassiveMacro.json", "r") as file:
				return cls(**json.loads(file.read()))
		except (JSONDecodeError, FileNotFoundError):
			return cls()


def get_int(text):
	return int(text) if text else 0


def get_float(text):
	return float(text) if text else 0


def get_resource(relative_path):
	try:
		# PyInstaller creates a temporary folder and stores its path in sys._MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)


def init():
	global window
	app = QApplication(sys.argv)
	window = MassiveMacroWindow()
	window.show()
	window.init()
	exit_code = app.exec()
	window.settings.save()
	sys.exit(exit_code)

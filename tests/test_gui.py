"""
Test the setup and run of the GUI as a whole system seperate from unittesting
"""
import os
import sys
import time
import unittest

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from SideKick.__main__ import MainGUI
from SideKick.file_manager import FileManager

app = qtw.QApplication(sys.argv)
path = os.path.dirname(os.path.dirname(__file__)) + "/SideKick"
gui = MainGUI(FileManager(path, False))

INSTALLED_BOARDS = [
"Select Board",
"SK Stem",
"Adafruit Circuit Playground",
"Arduino BT",
"Arduino Duemilanove or Diecimila arduino:avr:diecimila",
"Arduino Esplora",
"Arduino Ethernet",
"Arduino Fio",
"Arduino Gemma",
"Arduino Industrial 101",
"Arduino Leonardo",
"Arduino Leonardo ETH",
"Arduino Mega ADK",
"Arduino Mega or Mega 2560",
"Arduino Micro",
"Arduino Mini",
"Arduino NG or older",
"Arduino Nano",
"Arduino Pro or Pro Mini",
"Arduino Robot Control",
"Arduino Robot Motor",
"Arduino Uno",
"Arduino Uno Mini",
"Arduino Uno WiFi",
"Arduino Yún",
"Arduino Yún Mini",
"LilyPad Arduino",
"LilyPad Arduino USB",
"Linino One",
"Raspberry Pi Pico",
"Teensy 2.0",
"Teensy 3.0",
"Teensy 3.2 / 3.1",
"Teensy 3.5",
"Teensy 3.6",
"Teensy 4.0",
"Teensy 4.1",
"Teensy LC",
"Teensy MicroMod",
"Teensy++ 2.0"
]

class TestGui(unittest.TestCase):
    """
    Testing the main features and backend of the SideKickGUI in an integration test
    """

    @classmethod
    def setUpClass(cls):
        print("Setting up the tests...")
        app.setWindowIcon(qtg.QIcon("Ui/SideKick.ico"))
        gui.show()
        app.processEvents()
        print("Done.")

    @classmethod
    def tearDownClass(cls):
        print("Closing SideKick GUI...")
        app.closeAllWindows()
        gui.close_gui()
        print("Done.")

    def test_check_installed_boards(self):
        """
        Check that all of the correct boards have been installed
        """
        boards = []
        for i in range(gui.main_ui.supported_boards.count()):
            boards.append(gui.main_ui.supported_boards.itemText(i))
        self.assertTrue(set(INSTALLED_BOARDS).issubset(boards))

    def test_check_connection_status(self):
        """
        As there is no device to connect to, check the Connected status is not connected
        """
        self.assertEqual(gui.main_ui.bottom_update.text(), "Not Connected")

    def test_opening_and_closing_menus(self):
        """
        Test opening the main menu window
        """
        gui.main_ui.file.click()
        app.processEvents()
        gui.main_ui.file.click()
        app.processEvents()
        gui.main_ui.device.click()
        app.processEvents()
        gui.main_ui.file.click()
        app.processEvents()

    def test_record_light(self):
        """
        Test the record light by letting it run for 10 seconds
        """
        gui.main_ui.record.click()
        for _ in range(10):
            time.sleep(1)
            app.processEvents()
        gui.main_ui.record.click()
        app.processEvents()

    def test_opening_sub_windows(self):
        """
        Test opening and closing all of the sub windows
        """
        gui.main_ui.tune_actuators.click()
        app.processEvents()
        gui.main_ui.library_manager.click()
        app.processEvents()
        gui.main_ui.boards_manager.click()
        app.processEvents()

if __name__ == "__main__":
    # Run the integration test
    unittest.main()
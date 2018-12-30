from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox
from PyQt5.QtCore import QSize, QRect
from opencl_connector import get_platforms


platforms = get_platforms()


class MandelWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.platforms = platforms

        self.setMinimumSize(QSize(640, 140))
        self.setWindowTitle("Mandelbulbulator")

        platforms_widget = QWidget(self)
        self.setCentralWidget(platforms_widget)

        self.comboBox = QComboBox(platforms_widget)
        self.comboBox.setGeometry(QRect(40, 40, 491, 31))
        self.comboBox.setObjectName(("platforms"))
        for p in self.platforms:
            platform_info = f"{p.name}, {p.vendor}, {p.version}"
            self.comboBox.addItem(platform_info)

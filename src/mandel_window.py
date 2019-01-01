from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox, QDesktopWidget, \
    QAction, QGroupBox, QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize, QRect
from PyQt5.QtGui import QIcon, QImage, QColor, QPixmap
from PyQt5 import QtGui
from opencl_connector import get_platforms
import numpy
from random import uniform


platforms = get_platforms()
w = 100
h = 100


class MandelWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(QSize(640, 480))
        self.create_grid_layout()

        self.setWindowTitle("Mandelbulbulator")
        self.show()

    def create_grid_layout(self):
        grid = QGridLayout()
        # grid.addWidget(self.get_image_settings_box(), 0, 0)
        grid.addWidget(self.get_platforms_combobox(), 0, 1)
        grid.addWidget(self.get_mandelbrot_image_box(), 0, 0)
        self.setLayout(grid)

    def get_mandelbrot_image_box(self):
        self.image = QImage(w, h, QImage.Format_ARGB32)
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                self.image.setPixel(x, y, QColor(255, x * 2.56, y * 2.56, 255).rgb())
        self.mandel_pixels = QPixmap.fromImage(self.image)
        self.mandel_image = QPixmap(self.mandel_pixels)
        self.mandel = QLabel(self)
        self.mandel.setPixmap(self.mandel_image)

        mandel_label = QLabel('Image')

        get_image_button = QPushButton('Reload', self)
        get_image_button.clicked.connect(self.reload_button_clicked)

        group_box = QGroupBox("Mandelbulbulator with Raytracing")
        vbox = QVBoxLayout()
        vbox.addWidget(mandel_label)
        vbox.addWidget(self.mandel)
        vbox.addWidget(get_image_button)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box

    def get_platforms_combobox(self):
        platforms_combobox = QComboBox(self)
        self.choosed_platform = QLabel("Choose your platform")

        for p in platforms:
            platform_info = f"{p.name}, {p.vendor}, {p.version}"
            platforms_combobox.addItem(platform_info)

        platforms_combobox.currentTextChanged.connect(self.platform_change)
        platforms_combobox.setMaximumWidth(400)

        group_box = QGroupBox("Platforms")
        vbox = QVBoxLayout()
        vbox.addWidget(self.choosed_platform)
        vbox.addWidget(platforms_combobox)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box

    def platform_change(self, platform):
        self.choosed_platform.setText(f"Current platform: {platform}")

    def reload_button_clicked(self):
        r_change = uniform(1.0, 2.56)
        g_change = uniform(1.0, 2.56)
        b_change = uniform(1.0, 2.56)
        for x in range(self.image.width()):
            for y in range(self.image.height()):
                self.image.setPixel(x, y, QColor(x * r_change, x * g_change, y * b_change, 255).rgb())
        self.mandel.setPixmap(QPixmap.fromImage(self.image))

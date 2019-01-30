from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QComboBox, QGroupBox, QVBoxLayout, \
    QPushButton
from src.opencl_connector import Connector
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QComboBox, QGroupBox, QVBoxLayout, \
    QPushButton, QDoubleSpinBox, QSpinBox, QCheckBox
import time

import numpy as np


class MandelWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.animate = False
        self.connector = Connector()
        self.setMinimumSize(QSize(640, 640))
        self.create_grid_layout()

        self.setWindowTitle("Mandelbulbulator")
        self.show()
        self.animation()

    def create_grid_layout(self):
        grid = QGridLayout()
        grid.addWidget(self.get_mandelbrot_image_box(), 0, 0)
        grid.addWidget(self.get_platforms_combobox(), 0, 1)
        self.setLayout(grid)

    def get_mandelbrot_image_box(self):
        self.image = self.connector.get_image()
        self.mandel_pixels = QPixmap.fromImage(self.image)
        self.mandel_image = QPixmap(self.mandel_pixels)
        self.mandel = QLabel(self)
        self.mandel.setPixmap(self.mandel_image)

        mandel_label = QLabel('Image')

        get_image_button = QPushButton('Reload', self)
        get_image_button.clicked.connect(self.reload_button_clicked)
        reset_image_button = QPushButton('Reset', self)
        reset_image_button.clicked.connect(self.reset)

        group_box = QGroupBox("Mandelbulbulator with Raytracing")
        vbox = QVBoxLayout()
        vbox.addWidget(mandel_label)
        vbox.addWidget(self.mandel)
        vbox.addWidget(get_image_button)
        vbox.addWidget(reset_image_button)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box

    def get_platforms_combobox(self):
        platforms = self.connector.get_platforms()
        platforms_combobox = QComboBox(self)

        self.position_box_x = QDoubleSpinBox(self)
        self.position_box_x.setRange(-10.0, 10.0)
        self.position_box_x.setSingleStep(0.01)
        self.position_box_x.setValue(0)
        self.position_box_y = QDoubleSpinBox(self)
        self.position_box_y.setRange(-10.0, 10.0)
        self.position_box_y.setSingleStep(0.01)
        self.position_box_y.setValue(0)
        self.position_box_z = QDoubleSpinBox(self)
        self.position_box_z.setRange(-10.0, 10.0)
        self.position_box_z.setSingleStep(0.01)
        self.position_box_z.setValue(-2)

        self.direction_box_x = QDoubleSpinBox(self)
        self.direction_box_x.setRange(-10.0, 10.0)
        self.direction_box_x.setSingleStep(0.01)
        self.direction_box_x.setValue(0)
        self.direction_box_y = QDoubleSpinBox(self)
        self.direction_box_y.setRange(-10.0, 10.0)
        self.direction_box_y.setSingleStep(0.01)
        self.direction_box_y.setValue(0)
        self.direction_box_z = QDoubleSpinBox(self)
        self.direction_box_z.setRange(-10.0, 10.0)
        self.direction_box_z.setSingleStep(0.01)
        self.direction_box_z.setValue(1)

        self.n_value = QSpinBox(self)
        self.n_value.setRange(2, 10)
        self.n_value.setValue(3)

        self.reverse_box = QCheckBox(self)
        self.reverse_box.setChecked(False)

        self.choosed_platform = QLabel("Choose your platform")
        self.position_label = QLabel("Choose position")
        self.direction_label = QLabel("Choose direction")
        self.n_label = QLabel("Choose n")
        self.reverse_label = QLabel("Reverse image")

        for p in platforms:
            platform_info = f"{p.name}, {p.vendor}, {p.version}"
            platforms_combobox.addItem(platform_info)

        platforms_combobox.currentTextChanged.connect(self.platform_change)
        platforms_combobox.setMaximumWidth(400)

        group_box = QGroupBox("Options")
        vbox = QVBoxLayout()
        vbox.addWidget(self.choosed_platform)
        vbox.addWidget(platforms_combobox)
        vbox.addWidget(self.position_label)
        vbox.addWidget(self.position_box_x)
        vbox.addWidget(self.position_box_y)
        vbox.addWidget(self.position_box_z)
        vbox.addWidget(self.direction_label)
        vbox.addWidget(self.direction_box_x)
        vbox.addWidget(self.direction_box_y)
        vbox.addWidget(self.direction_box_z)
        vbox.addWidget(self.n_label)
        vbox.addWidget(self.n_value)
        vbox.addWidget(self.reverse_label)
        vbox.addWidget(self.reverse_box)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box

    def platform_change(self, platform):
        self.choosed_platform.setText(f"Current platform: {platform}")

    def reset(self):
        self.position_box_x.setValue(0)
        self.position_box_y.setValue(0)
        self.position_box_z.setValue(-2)

        self.direction_box_x.setValue(0)
        self.direction_box_y.setValue(0)
        self.direction_box_z.setValue(1)

        self.n_value.setValue(3)

        self.reverse_box.setChecked(False)

        self.reload_button_clicked()

    def reload_button_clicked(self):
        position = np.array([self.position_box_x.value(), self.position_box_y.value(), self.position_box_z.value()])
        direction = np.array([self.direction_box_x.value(), self.direction_box_y.value(), self.direction_box_z.value()])
        n = self.n_value.value()
        reverse = self.reverse_box.isChecked()
        self.connector.update_image(position, direction, n, reverse)
        self.animation()

    def animation(self):
        self.image = self.connector.get_image()
        self.mandel.setPixmap(QPixmap.fromImage(self.image))

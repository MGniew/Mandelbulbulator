from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QComboBox, QGroupBox, QVBoxLayout, \
    QPushButton
from opencl_connector import Connector
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QComboBox, QGroupBox, QVBoxLayout, \
    QPushButton


class MandelWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.connector = Connector()
        self.setMinimumSize(QSize(640, 640))
        self.create_grid_layout()

        self.setWindowTitle("Mandelbulbulator")
        self.show()

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

        group_box = QGroupBox("Mandelbulbulator with Raytracing")
        vbox = QVBoxLayout()
        vbox.addWidget(mandel_label)
        vbox.addWidget(self.mandel)
        vbox.addWidget(get_image_button)
        vbox.addStretch(1)
        group_box.setLayout(vbox)
        return group_box

    def get_platforms_combobox(self):
        platforms = self.connector.get_platforms()
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
        self.connector.set_device(platform)

    def reload_button_clicked(self):
        self.image = self.connector.get_image()
        self.mandel.setPixmap(QPixmap.fromImage(self.image))

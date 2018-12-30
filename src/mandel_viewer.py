import sys
from style import get_app_with_dark_theme
from mandel_window import MandelWindow


if __name__ == "__main__":
    app = get_app_with_dark_theme()
    window = MandelWindow()
    window.show()
    sys.exit(app.exec_())

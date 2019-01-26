import sys
from src.style import get_app_with_dark_theme
from src.mandel_window import MandelWindow


if __name__ == "__main__":
    app = get_app_with_dark_theme()
    window = MandelWindow()
    sys.exit(app.exec_())

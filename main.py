import sys
import os
import traceback

# 全局异常捕获，写入日志方便排查
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.log')

def _log_exception(exc_type, exc_value, exc_tb):
    msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(msg)
    print(msg, file=sys.stderr)

sys.excepthook = _log_exception

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from theme import STYLE_SHEET
from login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    font = QFont("Inter", 13)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

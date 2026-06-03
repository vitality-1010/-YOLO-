import pymysql.err
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from config import db_connect
from theme import STYLE_SHEET
from main_window import YOLOv10App


# ---------- 登录窗口 ----------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(440, 580)
        self.setObjectName("centralWidget")
        self.setStyleSheet(STYLE_SHEET)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container = QVBoxLayout()
        container.setContentsMargins(40, 40, 40, 40)
        container.setSpacing(0)
        container.addStretch()

        icon_label = QLabel("◈")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Inter", 24))
        icon_label.setStyleSheet("color: #0f172a; margin-bottom: 6px;")

        title_label = QLabel("视觉检测")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Inter", 22, QFont.DemiBold))
        title_label.setStyleSheet("color: #0f172a; letter-spacing: -0.5px;")

        subtitle_label = QLabel("YOLOv10 智能检测平台 · 前沿版")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Inter", 13))
        subtitle_label.setStyleSheet("color: #94a3b8; margin-bottom: 36px;")

        card_frame = QFrame()
        card_frame.setObjectName("card")
        card_frame.setStyleSheet("""
            QFrame#card {
                background-color: #ffffff;
                border: 1px solid #f1f5f9;
                border-radius: 20px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 12))
        shadow.setOffset(0, 2)
        card_frame.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        welcome_label = QLabel("欢迎回来")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        welcome_label.setStyleSheet("color: #0f172a; letter-spacing: -0.2px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setMinimumHeight(42)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(42)

        self.login_btn = QPushButton("登录")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.setMinimumHeight(42)
        self.login_btn.setCursor(Qt.PointingHandCursor)

        self.register_btn = QPushButton("还没有账户？注册")
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #64748b;
                border: none;
                font-weight: 400;
                font-size: 13px;
                padding: 4px;
            }
            QPushButton:hover {
                color: #0f172a;
            }
        """)

        card_layout.addWidget(welcome_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.register_btn)

        footer_label = QLabel("v3.0 · 智能进化")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #cbd5e1; font-size: 12px; margin-top: 20px;")

        container.addWidget(icon_label)
        container.addWidget(title_label)
        container.addWidget(subtitle_label)
        container.addWidget(card_frame)
        container.addWidget(footer_label)
        container.addStretch()

        main_layout.addLayout(container)
        self.setLayout(main_layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.register)
        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "提示", "请输入用户名和密码")
            return
        try:
            conn = db_connect()
        except Exception as e:
            QMessageBox.critical(self, "连接失败", f"数据库连接错误：{str(e)}")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "查询错误", f"数据库查询失败：{str(e)}")
            conn.close()
            return
        if result:
            try:
                self.accept_login(username)
            except Exception as e:
                QMessageBox.critical(self, "启动错误", f"主窗口初始化失败：{str(e)}")
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "提示", "用户名和密码不能为空")
            return
        if len(username) < 3 or len(password) < 4:
            QMessageBox.warning(self, "格式错误", "用户名至少3位，密码至少4位")
            return
        conn = db_connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            QMessageBox.information(self, "注册成功", "账户已创建，请登录")
        except pymysql.err.IntegrityError:
            QMessageBox.warning(self, "注册失败", "该用户名已被使用")
        finally:
            conn.close()

    def accept_login(self, username):
        self.main_window = YOLOv10App(username=username)
        self.main_window.show()
        self.close()

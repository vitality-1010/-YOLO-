STYLE_SHEET = """
QWidget {
    font-family: "Inter", "SF Pro Text", "Segoe UI", "Microsoft YaHei", -apple-system, sans-serif;
    font-size: 13.5px;
    color: #1e293b;
}
QMainWindow, QDialog {
    background-color: #f1f5f9;
}
QWidget#centralWidget {
    background-color: #f1f5f9;
}

QGroupBox {
    font-weight: 600;
    border: none;
    border-radius: 14px;
    margin-top: 16px;
    background-color: #ffffff;
    padding: 20px 16px 16px 16px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 10px 0 10px;
    color: #0f172a;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: -0.2px;
}

QLabel {
    color: #334155;
    background: transparent;
}

QLineEdit {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 16px;
    background-color: #ffffff;
    selection-background-color: #e2e8f0;
    font-size: 14px;
    color: #0f172a;
}
QLineEdit:focus {
    border: 1.5px solid #94a3b8;
    background-color: #ffffff;
}
QLineEdit::placeholder {
    color: #94a3b8;
}

QPushButton {
    background-color: #ffffff;
    color: #1e293b;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 500;
    font-size: 13.5px;
    transition: all 0.15s ease;
}
QPushButton:hover {
    background-color: #f8fafc;
    border-color: #94a3b8;
}
QPushButton:pressed {
    background-color: #f1f5f9;
    border-color: #64748b;
}
QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}
QPushButton#loginBtn {
    background-color: #0f172a;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#loginBtn:hover {
    background-color: #1e293b;
}
QPushButton#loginBtn:pressed {
    background-color: #334155;
}
QPushButton#stopBtn {
    background-color: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
}
QPushButton#stopBtn:hover {
    background-color: #fee2e2;
    border-color: #fca5a5;
}
QPushButton#stopBtn:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}
QPushButton#manualAlertBtn {
    background-color: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
    font-weight: 600;
    font-size: 13px;
}
QPushButton#manualAlertBtn:hover {
    background-color: #fee2e2;
    border-color: #fca5a5;
}

QComboBox {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 8px 14px;
    background-color: #ffffff;
    font-size: 13.5px;
    color: #0f172a;
    min-height: 28px;
}
QComboBox:hover {
    border-color: #cbd5e1;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
}
QComboBox::down-arrow {
    width: 10px;
    height: 6px;
}
QComboBox QAbstractItemView {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    background: #ffffff;
    selection-background-color: #f1f5f9;
    selection-color: #0f172a;
    padding: 6px;
    outline: none;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #e2e8f0;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #0f172a;
    border: none;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #1e293b;
}
QSlider::sub-page:horizontal {
    background: #cbd5e1;
    border-radius: 2px;
}

QTableWidget {
    border: 1px solid #f1f5f9;
    border-radius: 12px;
    background-color: #ffffff;
    gridline-color: #f8fafc;
    selection-background-color: #f1f5f9;
    selection-color: #0f172a;
    font-size: 13px;
}
QTableWidget::item {
    padding: 8px 12px;
    border-bottom: 1px solid #f8fafc;
}
QTableWidget::item:selected {
    background-color: #f1f5f9;
    color: #0f172a;
}
QHeaderView::section {
    background-color: #fafafa;
    color: #64748b;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #f1f5f9;
    font-weight: 500;
    font-size: 12px;
}

QScrollBar:vertical {
    width: 6px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    height: 6px;
    background: transparent;
}
QScrollBar::handle:horizontal {
    background: #cbd5e1;
    border-radius: 3px;
    min-width: 30px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""

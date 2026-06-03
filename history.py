import os
import csv as _csv
import cv2
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from config import db_connect
from theme import STYLE_SHEET


# ---------- 历史记录窗口 ----------
class HistoryWindow(QDialog):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("检测记录")
        self.setMinimumSize(1000, 620)
        self.setObjectName("centralWidget")
        self.setStyleSheet(STYLE_SHEET)
        self.username = username

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)

        title = QLabel("检测记录")
        title.setFont(QFont("Inter", 18, QFont.DemiBold))
        title.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.cellDoubleClicked.connect(self.show_image)

        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("导出 CSV")
        self.delete_btn = QPushButton("删除选中")
        self.clear_btn = QPushButton("清空记录")
        for btn in [self.export_btn, self.delete_btn, self.clear_btn]:
            btn.setMinimumHeight(38)
            btn.setCursor(Qt.PointingHandCursor)

        self.export_btn.clicked.connect(self.export_to_csv)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.clear_btn.clicked.connect(self.clear_all)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, image_path, file_name, target_type, count, detected_at FROM detections WHERE username=%s ORDER BY detected_at DESC",
            (self.username,))
        self.records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(self.records))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "图片路径", "文件名", "目标类型", "数量", "检测时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)

        for row_idx, row_data in enumerate(self.records):
            for col_idx, value in enumerate(row_data[1:], start=1):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def show_image(self, row, column):
        image_path = self.records[row][1]
        if not os.path.exists(image_path):
            QMessageBox.warning(self, "无法打开图片", f"图片文件不存在：{image_path}")
            return
        img = cv2.imread(image_path)
        if img is None:
            return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img_rgb.shape
        qimg = QImage(img_rgb.data, width, height, 3 * width, QImage.Format_RGB888)
        self.viewer = QLabel()
        self.viewer.setPixmap(QPixmap.fromImage(qimg).scaled(950, 650, Qt.KeepAspectRatio))
        self.viewer.setWindowTitle("检测图像预览")
        self.viewer.show()

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "导出为CSV", "检测记录.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = _csv.writer(f)
                writer.writerow(["图片路径", "文件名", "目标类型", "数量", "检测时间"])
                for record in self.records:
                    writer.writerow([str(item) for item in record[1:]])
            QMessageBox.information(self, "导出成功", f"记录已导出到：{path}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", str(e))

    def delete_selected(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选中要删除的记录")
            return
        reply = QMessageBox.question(self, "确认删除", f"确定要删除选中的 {len(selected_rows)} 条记录吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        ids_to_delete = [self.records[row][0] for row in selected_rows]
        try:
            conn = db_connect()
            cursor = conn.cursor()
            format_strings = ','.join(['%s'] * len(ids_to_delete))
            cursor.execute(f"DELETE FROM detections WHERE id IN ({format_strings})", tuple(ids_to_delete))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "成功", f"已删除 {len(ids_to_delete)} 条记录")
            self.load_history()
        except Exception as e:
            QMessageBox.critical(self, "删除失败", str(e))

    def clear_all(self):
        reply = QMessageBox.question(self, "确认清空", "确定要删除所有历史记录吗？此操作不可恢复！",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detections WHERE username=%s", (self.username,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "成功", "所有记录已清空")
            self.load_history()
        except Exception as e:
            QMessageBox.critical(self, "清空失败", str(e))

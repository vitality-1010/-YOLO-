import numpy as np
from PyQt5.QtWidgets import QLabel, QMenu
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRect, QPointF, QLineF, pyqtSignal


# ---------- 自定义图像标签（支持画矩形、方向线）----------
class EditableImageLabel(QLabel):
    rect_created = pyqtSignal(QRect)
    line_created = pyqtSignal(QPointF, QPointF)  # 发射起点和终点
    roi_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.drawing = False
        self.start_point = QPoint()
        self.current_rect = QRect()
        self.drawing_line = False
        self.line_start = QPointF()
        self.line_end = QPointF()
        self.temp_line = None

        # 绘制的形状存储
        self.rois = []          # 矩形区域 (QRect)
        self.lines = []         # 方向线段 [(QPointF, QPointF), ...]
        self.current_mode = 'rect'  # 'rect' 或 'line'

    def set_drawing_mode(self, mode):
        """切换绘制模式：'rect' 画禁行区，'line' 画方向线"""
        self.current_mode = mode

    def setPixmap(self, pixmap):
        self.base_pixmap = pixmap
        super().setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_mode == 'rect':
                self.drawing = True
                self.start_point = event.pos()
                self.current_rect = QRect(self.start_point, self.start_point)
            elif self.current_mode == 'line':
                self.drawing_line = True
                self.line_start = event.pos()
                self.line_end = event.pos()
                self.temp_line = (self.line_start, self.line_end)
                self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.current_rect = QRect(self.start_point, event.pos()).normalized()
            self.update()
        elif self.drawing_line:
            self.line_end = event.pos()
            self.temp_line = (self.line_start, self.line_end)
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing:
                self.drawing = False
                rect = QRect(self.start_point, event.pos()).normalized()
                if rect.width() > 5 and rect.height() > 5:
                    self.rois.append(rect)
                    self.rect_created.emit(rect)
            elif self.drawing_line:
                self.drawing_line = False
                if (self.line_start - self.line_end).manhattanLength() > 10:
                    self.lines.append((self.line_start, self.line_end))
                    self.line_created.emit(self.line_start, self.line_end)
                self.temp_line = None
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # 绘制禁行区矩形
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
        for roi in self.rois:
            painter.drawRect(roi)
        if self.drawing:
            painter.drawRect(self.current_rect)

        # 绘制方向线
        painter.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
        for start, end in self.lines:
            painter.drawLine(QLineF(start, end))
            # 绘制箭头头部
            self._draw_arrow(painter, start, end)
        if self.temp_line:
            painter.drawLine(QLineF(self.temp_line[0], self.temp_line[1]))
            self._draw_arrow(painter, self.temp_line[0], self.temp_line[1])

    def _draw_arrow(self, painter, start, end):
        line = QLineF(start, end)
        if line.length() == 0:
            return
        angle = line.angle()  # 角度，0指向右，逆时针
        arrow_size = 10
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawLine(line)
        # 简单画一个三角形箭头
        p1 = end + QPointF(
            arrow_size * np.cos(np.radians(angle + 150)),
            -arrow_size * np.sin(np.radians(angle + 150))
        )
        p2 = end + QPointF(
            arrow_size * np.cos(np.radians(angle - 150)),
            -arrow_size * np.sin(np.radians(angle - 150))
        )
        painter.drawLine(QLineF(end, p1))
        painter.drawLine(QLineF(end, p2))

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.addAction("切换到矩形模式 (禁行区)").triggered.connect(lambda: self.set_drawing_mode('rect'))
        menu.addAction("切换到方向线模式 (允许方向)").triggered.connect(lambda: self.set_drawing_mode('line'))
        menu.addSeparator()
        clear_rect = menu.addAction("清除所有矩形")
        clear_lines = menu.addAction("清除所有方向线")
        clear_all = menu.addAction("清除全部")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == clear_rect:
            self.rois.clear()
        elif action == clear_lines:
            self.lines.clear()
        elif action == clear_all:
            self.rois.clear()
            self.lines.clear()
        self.update()
        self.roi_changed.emit(self.rois)

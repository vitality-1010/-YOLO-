from PyQt5.QtCore import QObject, pyqtSignal


# ---------- 报告生成线程桥接（安全回调到主线程） ----------
class _ReportBridge(QObject):
    """将工作线程的回调安全转到主线程"""
    finished = pyqtSignal(str, str, str)  # stats_summary, alert_summary, analysis_text
    error = pyqtSignal(str)

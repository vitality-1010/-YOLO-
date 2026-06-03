import time
import numpy as np
from collections import defaultdict, deque


# ---------- 交通规则监控 ----------
class TrafficMonitor:
    def __init__(self):
        # 存储每个目标的轨迹：id -> deque of (x,y,timestamp)
        self.tracks = defaultdict(lambda: deque(maxlen=20))
        # 允许的行进方向线段 (起点, 终点) 列表
        self.direction_lines = []
        # 行人禁行区域 (矩形) 列表
        self.restricted_zones = []
        # 当前活跃的预警列表，每个元素为 (id, label, type, level, timestamp)
        self.active_alerts = []
        # 防止重复预警的冷却
        self.alert_cooldown = defaultdict(lambda: 0)

    def set_direction_lines(self, lines):
        self.direction_lines = lines  # [(QPointF, QPointF), ...]

    def set_restricted_zones(self, zones):
        self.restricted_zones = zones  # [(x1,y1,x2,y2), ...]

    def update(self, obj_id, cls_label, center):
        # center: (x, y)
        now = time.time()
        track = self.tracks[obj_id]
        track.append((*center, now))

        alerts = []
        if len(track) < 2:
            return alerts

        # 计算速度向量 (dx, dy) 和时间差
        p0 = np.array(track[-2][:2])
        p1 = np.array(center)
        move_vec = p1 - p0
        speed = np.linalg.norm(move_vec)

        # 1. 逆行检测（仅对车辆/行人均可，由方向线定义允许方向）
        if self.direction_lines and speed > 3.0:  # 像素移动阈值
            for (start, end) in self.direction_lines:
                # 方向线向量
                dir_vec = np.array([end.x() - start.x(), end.y() - start.y()])
                if np.linalg.norm(dir_vec) < 1e-3:
                    continue
                dir_vec = dir_vec / np.linalg.norm(dir_vec)
                # 移动向量单位化
                move_norm = move_vec / (np.linalg.norm(move_vec) + 1e-6)
                # 点积判断方向一致性
                dot = np.dot(move_norm, dir_vec)
                # 如果反向 (夹角 > 90度，点积 < 0)
                if dot < -0.2:  # 允许一定缓冲
                    level = 2  # 二级警告
                    if speed > 15.0:
                        level = 3  # 高速逆行，三级危险
                    alerts.append(("逆行", level))
                    break  # 一个目标只报一次逆行

        # 2. 禁行区域闯入（如行人进入机动车道）
        if self.restricted_zones:
            cx, cy = center
            for (rx1, ry1, rx2, ry2) in self.restricted_zones:
                if rx1 <= cx <= rx2 and ry1 <= cy <= ry2:
                    # 行人标签判定
                    if "person" in cls_label.lower() or "行人" in cls_label:
                        level = 1 if speed < 5.0 else 2
                        alerts.append(("行人闯入", level))
                        break

        # 去重冷却：同一个目标相同类型短时间内不重复
        filtered = []
        for alert_type, level in alerts:
            key = (obj_id, alert_type)
            if now - self.alert_cooldown[key] > 2.0:
                self.alert_cooldown[key] = now
                filtered.append((obj_id, cls_label, alert_type, level, now))
        return filtered

    # 车辆相关类别
    VEHICLE_CLASSES = {'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'boat',
                       'train', 'aeroplane', '三轮车', '电动车'}

    def check_collisions(self, boxes_info):
        """两两计算车辆框 IoU，重叠即报警"""
        now = time.time()
        alerts = []
        n = len(boxes_info)
        for i in range(n):
            for j in range(i + 1, n):
                id1, label1, box1 = boxes_info[i]
                id2, label2, box2 = boxes_info[j]
                if label1 not in self.VEHICLE_CLASSES or label2 not in self.VEHICLE_CLASSES:
                    continue

                xA = max(box1[0], box2[0]); yA = max(box1[1], box2[1])
                xB = min(box1[2], box2[2]); yB = min(box1[3], box2[3])
                interArea = max(0, xB - xA) * max(0, yB - yA)
                if interArea <= 0:
                    continue

                area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
                area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
                iou = interArea / min(area1, area2)

                if iou > 0.08:
                    key = (min(id1, id2), max(id1, id2), 'collision')
                    if now - self.alert_cooldown[key] > 3.0:
                        self.alert_cooldown[key] = now
                        level = 3 if iou > 0.3 else (2 if iou > 0.15 else 1)
                        alerts.append((id1, f'{label1}↔{label2}', '车辆碰撞', level, now))
        return alerts

import sys
import random
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush,
    QPolygonF
)

# ================== THEME ==================
PRIMARY_COLOR = QColor("#00bfff")   # AI Blue
ACCENT_COLOR  = QColor("#e6f7ff")   # Soft White Blue
BG_COLOR      = QColor("#000000")
WARNING_COLOR = QColor("#ff3b3b")   # Alert Red


# ================== HEX PANEL ==================
class HexagonPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.opacity = 60
        self.increasing = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(80)

    def animate(self):
        if self.increasing:
            self.opacity += 4
            if self.opacity >= 180:
                self.increasing = False
        else:
            self.opacity -= 4
            if self.opacity <= 60:
                self.increasing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = 30
        rows, cols = 4, 3
        x_offset, y_offset = 20, 60

        for r in range(rows):
            for c in range(cols):
                color = QColor(PRIMARY_COLOR)
                color.setAlpha(self.opacity if (r + c) % 2 else max(50, self.opacity - 40))

                pen = QPen(color, 2)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)

                x = x_offset + c * (size * 1.5)
                y = y_offset + r * (size * math.sqrt(3))
                if c % 2:
                    y += size * math.sqrt(3) / 2

                self.draw_hexagon(painter, x, y, size)

    def draw_hexagon(self, painter, x, y, size):
        points = [
            QPointF(
                x + size * math.cos(math.radians(60 * i)),
                y + size * math.sin(math.radians(60 * i))
            )
            for i in range(6)
        ]
        painter.drawPolygon(QPolygonF(points))


# ================== TELEMETRY PANEL ==================
class TelemetryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.bar_heights = [30, 50, 70, 40]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(90)

    def animate(self):
        self.bar_heights = [
            max(10, min(100, h + random.randint(-12, 12)))
            for h in self.bar_heights
        ]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QBrush(PRIMARY_COLOR))
        painter.setPen(Qt.PenStyle.NoPen)

        bar_width = 26
        gap = 12
        start_x = 20
        base_y = 160

        for i, h in enumerate(self.bar_heights):
            x = start_x + i * (bar_width + gap)
            painter.drawRect(QRectF(x, base_y - h, bar_width, h))


# ================== CENTRAL REACTOR ==================
class CentralReactor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle_outer = 0
        self.angle_inner = 0
        self.is_paused = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        if not self.is_paused:
            self.angle_outer = (self.angle_outer + 1) % 360
            self.angle_inner = (self.angle_inner - 6) % 360
            self.update()

    def set_paused(self, paused):
        self.is_paused = paused
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width() / 2, self.height() / 2
        main_color = WARNING_COLOR if self.is_paused else PRIMARY_COLOR

        # Core pulse
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(main_color))
        pulse = (math.sin(self.angle_outer * 0.08) + 1) * 12 if not self.is_paused else 0
        painter.drawEllipse(QPointF(cx, cy), 22 + pulse, 22 + pulse)

        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Middle ring
        pen = QPen(main_color, 12)
        pen.setDashPattern([10, 10])
        painter.setPen(pen)

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle_outer)
        painter.drawEllipse(QPointF(0, 0), 100, 100)
        painter.restore()

        # Inner ring
        pen = QPen(ACCENT_COLOR, 4)
        pen.setDashPattern([6, 6])
        painter.setPen(pen)

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle_inner)
        painter.drawEllipse(QPointF(0, 0), 70, 70)
        painter.restore()

        # Outer arcs
        pen = QPen(main_color, 3)
        painter.setPen(pen)
        rect = QRectF(cx - 130, cy - 130, 260, 260)
        painter.drawArc(rect, 45 * 16, 90 * 16)
        painter.drawArc(rect, 225 * 16, 90 * 16)


# ================== MAIN GUI ==================
class JarvisGUI(QMainWindow):
    def __init__(self, pause_event):
        super().__init__()
        self.pause_event = pause_event
        self.is_paused = False

        self.setWindowTitle("JARVIS HUD")
        self.resize(1000, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: black;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(HexagonPanel())
        self.reactor = CentralReactor()
        layout.addWidget(self.reactor, stretch=2)
        layout.addWidget(TelemetryPanel())

    def mousePressEvent(self, event):
        self.toggle_pause()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.reactor.set_paused(self.is_paused)

        if self.is_paused:
            self.pause_event.set()
            self.setStyleSheet("background-color: #120000;")
            print("GUI: PAUSED")
        else:
            self.pause_event.clear()
            self.setStyleSheet("background-color: black;")
            print("GUI: RESUMED")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


# ================== RUN ==================
def run_gui(pause_event):
    app = QApplication(sys.argv)
    window = JarvisGUI(pause_event)
    window.show()
    sys.exit(app.exec())
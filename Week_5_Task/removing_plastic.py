"""
Biofouling Camera Cleaner — PyQt5 GUI
Holyrood Subsea Observatory

Rotate the inner plastic sheeting so the target colour (Blue or Orange)
passes through the camera window EXACTLY 3 times in one direction.
Three cone-shaped indicators track each successful pass.

Install:  pip install PyQt5
Run:      python biofouling_cleaner.py
"""

import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QComboBox, QGraphicsDropShadowEffect,
    QSizePolicy, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QPainter, QPen, QBrush,
    QRadialGradient, QPolygonF, QPainterPath
)

# ─────────────────────────────────────────────────────────
#  UI Colour palette
# ─────────────────────────────────────────────────────────
DEEP    = "#0b1e2d"
PANEL   = "#0f2a3f"
CARD    = "#112e45"
ACCENT  = "#00d4aa"
ACCENT2 = "#00aaee"
WARN    = "#f0a500"
SUCCESS = "#22cc88"
DANGER  = "#e05555"
TEXT    = "#dff0f8"
MUTED   = "#6a9ab5"
TNR     = "'Times New Roman', Times, serif"
BASE_PT = 16

# ─────────────────────────────────────────────────────────
#  Sheet drum — only Blue and Orange as target colours
# ─────────────────────────────────────────────────────────
SHEET_COLORS = [
    ("Blue",   QColor("#1565C0")),
    ("White",  QColor("#dce8f0")),
    ("White",  QColor("#dce8f0")),
    ("Orange", QColor("#E65100")),
    ("White",  QColor("#dce8f0")),
    ("White",  QColor("#dce8f0")),
]
N_SEG     = len(SHEET_COLORS)
SEG_ANGLE = 360.0 / N_SEG


# ─────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────
def shadow(w, r=18, col="#00d4aa"):
    ef = QGraphicsDropShadowEffect()
    ef.setBlurRadius(r)
    ef.setColor(QColor(col))
    ef.setOffset(0, 0)
    w.setGraphicsEffect(ef)
    return ef


def qlabel(text, size=BASE_PT, bold=False, color=TEXT, italic=False):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-family:{TNR}; font-size:{size}pt; color:{color};"
        f"{'font-weight:bold;' if bold else ''}"
        f"{'font-style:italic;' if italic else ''}"
        f"background:transparent;"
    )
    return lbl


# ─────────────────────────────────────────────────────────
#  Cone Pass Indicator
# ─────────────────────────────────────────────────────────
class ConePassIndicator(QWidget):
    """
    Three upright traffic-cone silhouettes.
    Each cone fills with the target colour when a pass is scored.
    """

    def __init__(self, target_color: QColor = QColor("#1565C0"), parent=None):
        super().__init__(parent)
        self._count        = 0
        self._target_qcol  = target_color
        self.setMinimumSize(280, 120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_count(self, n: int):
        self._count = max(0, min(3, n))
        self.update()

    def set_target_color(self, qc: QColor):
        self._target_qcol = qc
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h    = self.width(), self.height()
        n_cones = 3
        gap     = 22
        cone_w  = (w - gap * (n_cones + 1)) / n_cones
        cone_h  = h - 18

        for i in range(n_cones):
            x = gap + i * (cone_w + gap)
            self._draw_cone(p, x, 8, cone_w, cone_h, i < self._count)

    def _draw_cone(self, p, x, y, cw, ch, active: bool):
        apex_x = x + cw / 2
        apex_y = float(y)
        base_y = float(y + ch)

        # Colours
        if active:
            fill_col   = QColor(self._target_qcol)
            dark_col   = fill_col.darker(170)
            stripe_col = QColor("#ffffff"); stripe_col.setAlpha(190)
            base_col   = QColor("#777777")
        else:
            fill_col   = QColor(MUTED);    fill_col.setAlpha(50)
            dark_col   = QColor(MUTED);    dark_col.setAlpha(28)
            stripe_col = QColor("#ffffff"); stripe_col.setAlpha(35)
            base_col   = QColor(MUTED);    base_col.setAlpha(45)

        # Main cone body
        body = QPolygonF([
            QPointF(apex_x,    apex_y),
            QPointF(x,         base_y),
            QPointF(x + cw,    base_y),
        ])
        p.setBrush(QBrush(fill_col))
        p.setPen(QPen(dark_col, 1.5))
        p.drawPolygon(body)

        # Right-side 3-D shadow
        mid_y  = apex_y + ch * 0.5
        mx_r   = apex_x + (x + cw - apex_x) * 0.5
        shad   = QPolygonF([
            QPointF(apex_x, apex_y),
            QPointF(mx_r,   mid_y),
            QPointF(x + cw, base_y),
        ])
        dc = QColor(dark_col); dc.setAlpha(80 if active else 25)
        p.setBrush(QBrush(dc))
        p.setPen(Qt.NoPen)
        p.drawPolygon(shad)

        # Reflective white stripe
        t1, t2 = 0.38, 0.62
        sl_t = apex_x + (x       - apex_x) * t1
        sr_t = apex_x + (x + cw  - apex_x) * t1
        sl_b = apex_x + (x       - apex_x) * t2
        sr_b = apex_x + (x + cw  - apex_x) * t2
        stripe = QPolygonF([
            QPointF(sl_t, apex_y + ch * t1),
            QPointF(sr_t, apex_y + ch * t1),
            QPointF(sr_b, apex_y + ch * t2),
            QPointF(sl_b, apex_y + ch * t2),
        ])
        p.setBrush(QBrush(stripe_col))
        p.setPen(Qt.NoPen)
        p.drawPolygon(stripe)

        # Flat base ellipse
        base_ry   = ch * 0.07
        base_rect = QRectF(x, base_y - base_ry, cw, base_ry * 2)
        p.setBrush(QBrush(base_col))
        p.setPen(QPen(dark_col, 1))
        p.drawEllipse(base_rect)

        # Check-mark on active cones
        if active:
            p.setPen(QColor("#ffffff"))
            p.setFont(QFont("Times New Roman", 9, QFont.Bold))
            p.drawText(
                QRectF(x, apex_y + ch * 0.65, cw, ch * 0.28),
                Qt.AlignCenter, "✓"
            )


# ─────────────────────────────────────────────────────────
#  Camera Window Widget
# ─────────────────────────────────────────────────────────
class CameraWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)
        self._angle       = 0.0
        self._target      = "Blue"
        self._pass_count  = 0
        self._completed   = False
        self._flash_alpha = 0
        self._flash_col   = QColor(SUCCESS)
        self._flash_timer = QTimer(self)
        self._flash_timer.timeout.connect(self._fade_flash)

    @property
    def angle(self): return self._angle

    @angle.setter
    def angle(self, v):
        self._angle = v % 360.0
        self.update()

    def set_target(self, name: str):
        self._target     = name
        self._pass_count = 0
        self._completed  = False
        self.update()

    def reset(self):
        self._angle       = 0.0
        self._pass_count  = 0
        self._completed   = False
        self._flash_alpha = 0
        self.update()

    def get_pass_count(self): return self._pass_count
    def is_completed(self):   return self._completed
    def get_centre_colour_name(self): return self._centre_colour_name()

    def _centre_colour_name(self):
        lookup = (270.0 - self._angle) % 360.0
        idx    = int(lookup / SEG_ANGLE) % N_SEG
        return SHEET_COLORS[idx][0]

    def notify_colour_change(self, prev: str, new: str):
        if self._completed: return
        if new == self._target:
            self._pass_count += 1
            self._flash_col = (QColor("#1565C0") if self._target == "Blue"
                               else QColor("#E65100"))
            self._trigger_flash()
            if self._pass_count >= 3:
                self._completed = True
        self.update()

    def _trigger_flash(self):
        self._flash_alpha = 200
        self._flash_timer.start(35)

    def _fade_flash(self):
        self._flash_alpha = max(0, self._flash_alpha - 16)
        self.update()
        if self._flash_alpha == 0:
            self._flash_timer.stop()

    def paintEvent(self, _):
        p  = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h   = self.width(), self.height()
        cx, cy = w / 2, h / 2
        R      = min(w, h) / 2 - 10
        WIN_R  = R * 0.56

        # Housing
        hr = QRadialGradient(cx, cy, R)
        hr.setColorAt(0.68, QColor("#1a3a55"))
        hr.setColorAt(0.85, QColor("#0d2035"))
        hr.setColorAt(1.00, QColor("#06131f"))
        p.setBrush(QBrush(hr))
        p.setPen(QPen(QColor(ACCENT), 2))
        p.drawEllipse(QPointF(cx, cy), R, R)

        # Drum segments
        p.save()
        clip = QPainterPath()
        clip.addEllipse(QPointF(cx, cy), R - 4, R - 4)
        p.setClipPath(clip)
        rect = QRectF(cx - R + 4, cy - R + 4, (R - 4) * 2, (R - 4) * 2)
        for i, (_, qcol) in enumerate(SHEET_COLORS):
            sa = i * SEG_ANGLE + self._angle
            p.setBrush(QBrush(qcol))
            p.setPen(Qt.NoPen)
            p.drawPie(rect, int(-sa * 16), int(-SEG_ANGLE * 16))
        p.restore()

        # Biofouling overlay
        foul_a = max(0, 210 - self._pass_count * 70)
        if foul_a > 0:
            fg = QRadialGradient(cx + 12, cy - 8, WIN_R * 1.1)
            c1 = QColor("#3d2b1f"); c1.setAlpha(foul_a)
            c2 = QColor("#2a4a1e"); c2.setAlpha(int(foul_a * 0.55))
            c3 = QColor("#1a2e0a"); c3.setAlpha(int(foul_a * 0.25))
            fg.setColorAt(0.0, c1); fg.setColorAt(0.5, c2); fg.setColorAt(1.0, c3)
            p.save()
            wp = QPainterPath()
            wp.addEllipse(QPointF(cx, cy), WIN_R, WIN_R)
            p.setClipPath(wp)
            p.setBrush(QBrush(fg)); p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(cx, cy), WIN_R, WIN_R)
            p.restore()

        # Flash
        if self._flash_alpha > 0:
            fc = QColor(self._flash_col); fc.setAlpha(self._flash_alpha)
            p.setBrush(QBrush(fc)); p.setPen(Qt.NoPen)
            p.drawEllipse(QPointF(cx, cy), WIN_R - 2, WIN_R - 2)

        # Bezel
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(ACCENT), 3))
        p.drawEllipse(QPointF(cx, cy), WIN_R, WIN_R)

        # 12 o'clock tick
        p.setPen(QPen(QColor(WARN), 3, Qt.SolidLine, Qt.RoundCap))
        p.drawLine(QPointF(cx, cy - WIN_R - 2), QPointF(cx, cy - WIN_R - 14))


# ─────────────────────────────────────────────────────────
#  Toggle Switch
# ─────────────────────────────────────────────────────────
class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cw = True
        self.setFixedSize(160, 44)
        self.setCursor(Qt.PointingHandCursor)

    def is_clockwise(self): return self._cw

    def mousePressEvent(self, _):
        self._cw = not self._cw
        self.update()
        if hasattr(self.parent(), "_on_direction_toggle"):
            self.parent()._on_direction_toggle(self._cw)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        tc = QColor(ACCENT) if self._cw else QColor(ACCENT2)
        tc.setAlpha(180)
        p.setBrush(QBrush(tc)); p.setPen(QPen(QColor(ACCENT), 2))
        p.drawRoundedRect(0, 0, w, h, h / 2, h / 2)
        tx = w - h + 4 if self._cw else 4
        p.setBrush(QBrush(QColor("#ffffff"))); p.setPen(Qt.NoPen)
        p.drawEllipse(int(tx), 4, h - 8, h - 8)
        p.setPen(QColor(DEEP))
        p.setFont(QFont("Times New Roman", 11, QFont.Bold))
        p.drawText(0, 0, w, h, Qt.AlignCenter,
                   "CW  ↻" if self._cw else "↺  CCW")


# ─────────────────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────────────────
class BiofoulingApp(QMainWindow):

    STEP_DEG      = 3.0
    AUTO_INTERVAL = 28

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Biofouling Camera Cleaner — Holyrood Subsea Observatory"
        )
        self.setMinimumSize(1060, 700)
        self._direction  = 1
        self._locked_dir = None
        self._auto_timer = QTimer(self)
        self._auto_timer.timeout.connect(self._auto_rotate)
        self._holding    = False
        self._build_ui()
        self.setStyleSheet(f"QMainWindow {{ background:{DEEP}; }}")

    # ─────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(22, 16, 22, 16)
        root.setSpacing(12)
        root.addWidget(self._build_header())
        body = QHBoxLayout(); body.setSpacing(18)
        body.addWidget(self._build_left_panel(),  stretch=4)
        body.addWidget(self._build_right_panel(), stretch=5)
        root.addLayout(body)
        root.addWidget(self._build_status_bar())

    def _build_header(self):
        f = QFrame()
        f.setStyleSheet(f"""
            background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {PANEL}, stop:0.5 #0d3050, stop:1 {PANEL});
            border:1px solid #1a5070; border-radius:12px;
        """)
        lay = QVBoxLayout(f); lay.setContentsMargins(22, 12, 22, 10); lay.setSpacing(3)
        t = QLabel("🔬  Biofouling Camera Cleaner")
        t.setStyleSheet(f"font-family:{TNR}; font-size:22pt; font-weight:bold;"
                        f"color:{ACCENT}; background:transparent;")
        lay.addWidget(t)
        s = QLabel("Holyrood Subsea Observatory  ·  "
                   "Rotate the sheeting so the target colour passes the window 3 times.")
        s.setStyleSheet(f"font-family:{TNR}; font-size:{BASE_PT}pt; font-style:italic;"
                        f"color:{MUTED}; background:transparent;")
        lay.addWidget(s)
        shadow(f, 24, ACCENT)
        return f

    def _build_left_panel(self):
        f = QFrame()
        f.setStyleSheet(f"background:{PANEL}; border:1px solid #1a4060; border-radius:12px;")
        lay = QVBoxLayout(f); lay.setContentsMargins(18, 18, 18, 18); lay.setSpacing(14)

        lay.addWidget(self._sec("⚙  Judge Settings"))
        lay.addWidget(self._sep())

        # Target colour — only Blue & Orange
        tc = QHBoxLayout()
        tc.addWidget(qlabel("Target Colour:", BASE_PT, bold=True))
        self.colour_combo = QComboBox()
        self.colour_combo.addItems(["Blue", "Orange"])
        self.colour_combo.setStyleSheet(self._combo_style())
        self.colour_combo.currentTextChanged.connect(self._on_target_changed)
        tc.addWidget(self.colour_combo)
        lay.addLayout(tc)

        lay.addWidget(self._sep())
        lay.addWidget(self._sec("↻  Rotation Direction"))

        dr = QHBoxLayout()
        dr.addWidget(qlabel("Direction:", BASE_PT, color=MUTED))
        self.toggle = ToggleSwitch(self)
        dr.addWidget(self.toggle); dr.addStretch()
        lay.addLayout(dr)

        self.dir_info = qlabel(
            "Clockwise selected.  Direction locks on first move.",
            BASE_PT - 2, color=MUTED, italic=True
        )
        self.dir_info.setWordWrap(True)
        lay.addWidget(self.dir_info)

        lay.addWidget(self._sep())
        lay.addWidget(self._sec("🎛  Rotate Sheeting"))

        bg = QGridLayout(); bg.setSpacing(10)
        self.ccw_btn = self._big_btn("↺  Rotate CCW", ACCENT2, DEEP)
        self.cw_btn  = self._big_btn("↻  Rotate CW",  ACCENT,  DEEP)
        self.cw_btn.pressed.connect(lambda:  self._start_hold(1))
        self.cw_btn.released.connect(self._stop_hold)
        self.ccw_btn.pressed.connect(lambda: self._start_hold(-1))
        self.ccw_btn.released.connect(self._stop_hold)
        bg.addWidget(self.ccw_btn, 0, 0); bg.addWidget(self.cw_btn, 0, 1)
        lay.addLayout(bg)

        hint = qlabel("Hold a button to spin continuously.  "
                      "Direction locks after first move.",
                      BASE_PT - 2, color=MUTED, italic=True)
        hint.setWordWrap(True)
        lay.addWidget(hint)
        lay.addWidget(self._sep())

        rb = self._big_btn("⟳  Reset / New Attempt", DANGER, "#fff")
        rb.clicked.connect(self._reset)
        lay.addWidget(rb)
        lay.addStretch()
        return f

    def _build_right_panel(self):
        f = QFrame()
        f.setStyleSheet(f"background:{PANEL}; border:1px solid #1a4060; border-radius:12px;")
        lay = QVBoxLayout(f); lay.setContentsMargins(18, 18, 18, 18); lay.setSpacing(12)

        lay.addWidget(self._sec("📷  Camera Window"))
        lay.addWidget(self._sep())

        # ── Label ABOVE the circle — current colour showing ──
        self.colour_above_lbl = QLabel("Current:  —")
        self.colour_above_lbl.setAlignment(Qt.AlignCenter)
        self.colour_above_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
            f"color:{MUTED}; background:transparent;"
        )
        lay.addWidget(self.colour_above_lbl)

        # Camera
        cr = QHBoxLayout(); cr.addStretch()
        self.camera = CameraWindow()
        self.camera.setFixedSize(300, 300)
        cr.addWidget(self.camera); cr.addStretch()
        lay.addLayout(cr)

        # ── Label BELOW the circle — completion status ──
        self.completion_lbl_below = QLabel("Rotate the sheeting to begin cleaning.")
        self.completion_lbl_below.setAlignment(Qt.AlignCenter)
        self.completion_lbl_below.setWordWrap(True)
        self.completion_lbl_below.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-style:italic;"
            f"color:{MUTED}; background:transparent;"
        )
        lay.addWidget(self.completion_lbl_below)

        # Swatch row
        sr = QHBoxLayout(); sr.addStretch()
        sr.addWidget(qlabel("Target:", BASE_PT, bold=True))
        self.swatch = QLabel("   ")
        self.swatch.setFixedSize(70, 28)
        self.swatch.setStyleSheet(f"background:#1565C0; border:2px solid {ACCENT}; border-radius:5px;")
        sr.addWidget(self.swatch)
        self.target_name_lbl = qlabel("Blue", BASE_PT, bold=True, color=ACCENT)
        sr.addWidget(self.target_name_lbl); sr.addStretch()
        lay.addLayout(sr)

        lay.addWidget(self._sep())

        # ── Cone pass indicators ──
        lay.addWidget(self._sec("🚧  Pass Counter  —  3 cones must light up"))

        self.cone_indicator = ConePassIndicator(QColor("#1565C0"))
        lay.addWidget(self.cone_indicator)

        self.pass_count_lbl = qlabel("0 / 3", BASE_PT + 4, bold=True, color=MUTED)
        self.pass_count_lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.pass_count_lbl)

        lay.addWidget(self._sep())

        # Completion banner
        self.banner = QFrame()
        self.banner.setStyleSheet(
            f"background:{CARD}; border:1px solid #1a4060; border-radius:10px;"
        )
        bl = QVBoxLayout(self.banner); bl.setContentsMargins(12, 10, 12, 10)
        self.banner_lbl = QLabel("Rotate the sheeting to begin cleaning.")
        self.banner_lbl.setAlignment(Qt.AlignCenter)
        self.banner_lbl.setWordWrap(True)
        self.banner_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt;"
            f"color:{MUTED}; background:transparent;"
        )
        bl.addWidget(self.banner_lbl)
        lay.addWidget(self.banner)

        lay.addStretch()
        self._refresh_swatch("Blue")
        return f

    def _build_status_bar(self):
        f = QFrame(); f.setFixedHeight(44)
        f.setStyleSheet(f"background:{CARD}; border:1px solid #1a4060; border-radius:8px;")
        lay = QHBoxLayout(f); lay.setContentsMargins(16, 0, 16, 0)
        self.status_lbl = qlabel("Ready.  Set the target colour and start rotating.",
                                 BASE_PT - 1, color=MUTED, italic=True)
        lay.addWidget(self.status_lbl); lay.addStretch()
        self.angle_lbl = qlabel("Angle: 0°", BASE_PT - 1, color=MUTED)
        lay.addWidget(self.angle_lbl)
        lay.addSpacing(18)
        self.dir_lbl = qlabel("Direction: CW", BASE_PT - 1, color=ACCENT)
        lay.addWidget(self.dir_lbl)
        return f

    # ─── Style helpers ───────────────────────
    def _combo_style(self):
        return f"""
            QComboBox {{
                background:{CARD}; color:{TEXT};
                border:2px solid #1e5070; border-radius:6px;
                padding:6px 12px;
                font-family:{TNR}; font-size:{BASE_PT}pt;
            }}
            QComboBox:focus {{ border:2px solid {ACCENT}; }}
            QComboBox QAbstractItemView {{
                background:{CARD}; color:{TEXT};
                font-family:{TNR}; font-size:{BASE_PT}pt;
                selection-background-color:#1a5070;
            }}
            QComboBox::drop-down {{ border:none; }}
        """

    @staticmethod
    def _sec(text):
        l = QLabel(text)
        l.setStyleSheet(f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
                        f"color:{ACCENT}; background:transparent;")
        return l

    @staticmethod
    def _sep():
        s = QFrame(); s.setFrameShape(QFrame.HLine)
        s.setStyleSheet("color:#1a4060; background:#1a4060;")
        s.setFixedHeight(1); return s

    @staticmethod
    def _big_btn(text, bg, fg):
        b = QPushButton(text); b.setMinimumHeight(46)
        b.setStyleSheet(f"""
            QPushButton {{
                background:{bg}; color:{fg}; border:none; border-radius:8px;
                font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;
                padding:8px 16px;
            }}
            QPushButton:hover {{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {bg}, stop:1 #ffffff40);
            }}
            QPushButton:pressed {{ opacity:0.8; }}
        """)
        return b

    # ─── Logic ───────────────────────────────
    def _on_target_changed(self, name: str):
        self._reset(confirm=False)
        self._refresh_swatch(name)
        self.camera.set_target(name)
        tc = QColor("#1565C0") if name == "Blue" else QColor("#E65100")
        self.cone_indicator.set_target_color(tc)
        self._set_status(f"Target set to {name}.  Start rotating to clean the camera.")

    def _on_direction_toggle(self, cw: bool):
        if self._locked_dir is not None:
            self.toggle._cw = (self._locked_dir == 1); self.toggle.update()
            self._set_status("⚠  Direction locked after first rotation.  Reset to change.", error=True)
            return
        self._direction = 1 if cw else -1
        lab = "Clockwise" if cw else "Counter-Clockwise"
        self.dir_info.setText(f"{lab} selected.  Direction locks on first move.")
        self.dir_lbl.setText(f"Direction: {'CW' if cw else 'CCW'}")

    def _start_hold(self, direction: int):
        if self.camera.is_completed(): return
        if self._locked_dir is not None and direction != self._locked_dir:
            self._set_status("⚠  Rotate in one direction only.  Reset to change.", error=True)
            return
        if self._locked_dir is None:
            self._locked_dir = direction; self._direction = direction
            self.toggle._cw = (direction == 1); self.toggle.update()
            self.dir_lbl.setText(f"Direction: {'CW' if direction == 1 else 'CCW'}")
        self._holding = True
        self._auto_timer.start(self.AUTO_INTERVAL)

    def _stop_hold(self):
        self._holding = False; self._auto_timer.stop()

    def _auto_rotate(self):
        if not self._holding: self._auto_timer.stop(); return
        self._do_rotate(self._direction * self.STEP_DEG)

    def _do_rotate(self, delta: float):
        if self.camera.is_completed(): self._auto_timer.stop(); return
        prev = self.camera._centre_colour_name()
        self.camera.angle = self.camera.angle + delta
        new  = self.camera._centre_colour_name()
        # Update the outside colour label
        col_hex = "#1565C0" if new == "Blue" else ("#E65100" if new == "Orange" else MUTED)
        self.colour_above_lbl.setText(f"Current:  {new}")
        self.colour_above_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
            f"color:{col_hex}; background:transparent;"
        )
        if new != prev:
            self.camera.notify_colour_change(prev, new)
            self._update_pass_display()
        self.angle_lbl.setText(f"Angle: {self.camera.angle:.1f}°")
        if self.camera.is_completed(): self._on_completed()

    def _update_pass_display(self):
        n = self.camera.get_pass_count()
        self.cone_indicator.set_count(n)
        self.pass_count_lbl.setText(f"{n} / 3")
        col = {0: MUTED, 1: WARN, 2: ACCENT2, 3: SUCCESS}.get(n, SUCCESS)
        self.pass_count_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT + 4}pt; font-weight:bold;"
            f"color:{col}; background:transparent;"
        )
        target = self.colour_combo.currentText()
        msgs = {
            1: f"Pass 1 ✓ — {target} spotted once.  Keep rotating!",
            2: f"Pass 2 ✓ — {target} spotted twice.  One more pass!",
        }
        if n in msgs: self._set_status(msgs[n])

    def _on_completed(self):
        self._auto_timer.stop()
        target = self.colour_combo.currentText()
        # Update the below-circle completion label
        self.completion_lbl_below.setText(
            f"✅  Camera cleaned!  {target} passed 3 times."
        )
        self.completion_lbl_below.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
            f"color:{SUCCESS}; background:transparent;"
        )
        self.banner_lbl.setText(
            f"✅  Camera successfully cleaned!\n"
            f"{target} passed through the window 3 times."
        )
        self.banner_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
            f"color:{SUCCESS}; background:transparent;"
        )
        shadow(self.banner, 28, SUCCESS)
        self._set_status(
            f"✅  SUCCESS — Biofouling removed!  {target} completed 3 full passes."
        )

    def _reset(self, confirm=True):
        if confirm and self.camera.is_completed():
            r = QMessageBox.question(self, "Reset?",
                "The camera has been cleaned.  Start a new attempt?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r != QMessageBox.Yes: return

        self._auto_timer.stop()
        self._locked_dir = None; self._direction = 1
        self.camera.reset()
        self.camera.set_target(self.colour_combo.currentText())
        tc = QColor("#1565C0") if self.colour_combo.currentText() == "Blue" \
            else QColor("#E65100")
        self.cone_indicator.set_target_color(tc)
        self.cone_indicator.set_count(0)
        self.pass_count_lbl.setText("0 / 3")
        self.pass_count_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT + 4}pt; font-weight:bold;"
            f"color:{MUTED}; background:transparent;"
        )
        self.colour_above_lbl.setText("Current:  —")
        self.colour_above_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-weight:bold;"
            f"color:{MUTED}; background:transparent;"
        )
        self.completion_lbl_below.setText("Rotate the sheeting to begin cleaning.")
        self.completion_lbl_below.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt; font-style:italic;"
            f"color:{MUTED}; background:transparent;"
        )
        self.banner_lbl.setText("Rotate the sheeting to begin cleaning.")
        self.banner_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT}pt;"
            f"color:{MUTED}; background:transparent;"
        )
        self.banner.setGraphicsEffect(None)
        self.angle_lbl.setText("Angle: 0°")
        self.dir_lbl.setText("Direction: CW")
        self.toggle._cw = True; self.toggle.update()
        self.dir_info.setText("Clockwise selected.  Direction locks on first move.")
        self._set_status("Reset complete.  Set the target colour and start rotating.")

    def _refresh_swatch(self, name: str):
        c = "#1565C0" if name == "Blue" else "#E65100"
        self.swatch.setStyleSheet(
            f"background:{c}; border:2px solid {ACCENT}; border-radius:5px;"
        )
        self.target_name_lbl.setText(name)

    def _set_status(self, msg: str, error=False):
        self.status_lbl.setText(msg)
        self.status_lbl.setStyleSheet(
            f"font-family:{TNR}; font-size:{BASE_PT - 1}pt;"
            f"color:{'#e05555' if error else MUTED}; font-style:italic;"
            f"background:transparent;"
        )

    def keyPressEvent(self, e):
        if self.camera.is_completed(): return
        if e.key() == Qt.Key_Right:   self._start_hold(1)
        elif e.key() == Qt.Key_Left:  self._start_hold(-1)

    def keyReleaseEvent(self, e):
        if e.key() in (Qt.Key_Right, Qt.Key_Left): self._stop_hold()


# ─────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Times New Roman", BASE_PT))

    pal = QPalette()
    pal.setColor(QPalette.Window,          QColor(DEEP))
    pal.setColor(QPalette.WindowText,      QColor(TEXT))
    pal.setColor(QPalette.Base,            QColor(PANEL))
    pal.setColor(QPalette.AlternateBase,   QColor(CARD))
    pal.setColor(QPalette.Text,            QColor(TEXT))
    pal.setColor(QPalette.Button,          QColor(PANEL))
    pal.setColor(QPalette.ButtonText,      QColor(TEXT))
    pal.setColor(QPalette.Highlight,       QColor(ACCENT))
    pal.setColor(QPalette.HighlightedText, QColor(DEEP))
    app.setPalette(pal)

    w = BiofoulingApp()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
"""
eDNA Species Frequency Calculator — PyQt5 GUI
Holyrood Subsea Observatory

Install dependency:
    pip install PyQt5

Run:
    python edna_frequency_app.py
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QBrush,
    QPainter, QPixmap, QIcon
)

# Color GIven

DEEP_OCEAN   = "#0a1628"
MID_OCEAN    = "#0d2137"
PANEL_BG     = "#0f2a45"
CARD_BG      = "#112d4a"
ACCENT_TEAL  = "#00c8a0"
ACCENT_BLUE  = "#00a8e8"
ACCENT_GLOW  = "#00e5c3"
TEXT_PRIMARY  = "#e8f4f8"
TEXT_MUTED    = "#7ab3cc"
ROW_EVEN     = "#0e2840"
ROW_ODD      = "#0c2035"
HEADER_BG    = "#0a3352"
TOTAL_BG     = "#003d2a"


#  Font and Size declare

TNR          = "'Times New Roman', Times, serif"   # CSS font-family string
TNR_PT       = 16                                   # base point size


# text labelling

def make_label(text, size=TNR_PT, bold=False, color=TEXT_PRIMARY):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color: {color}; font-family: {TNR}; font-size: {size}pt;"
        f"{'font-weight: bold;' if bold else ''} background: transparent;"
    )
    return lbl


def shadow(widget, radius=18, color="#00c8a0", opacity=80):
    ef = QGraphicsDropShadowEffect()
    ef.setBlurRadius(radius)
    ef.setColor(QColor(color))
    ef.setOffset(0, 0)
    ef.setEnabled(True)
    widget.setGraphicsEffect(ef)
    return ef


class SpeciesInputRow(QFrame):
    """One row: species name + number seen."""

    def __init__(self, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self.setStyleSheet(f"""
            QFrame {{
                background: {CARD_BG};
                border: 1px solid #1a4060;
                border-radius: 8px;
                margin: 2px 0px;
            }}
        """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(12)

        # Index badge

        badge = QLabel(f"{index:02d}")
        badge.setFixedSize(32, 32)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 {ACCENT_TEAL}, stop:1 {ACCENT_BLUE});
            color: {DEEP_OCEAN};
            font-family: {TNR};
            font-weight: bold;
            font-size: {TNR_PT}pt;
            border-radius: 16px;
        """)
        lay.addWidget(badge)

        # Species name field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(f"Species {index} name  (e.g. Snow crab)")
        self.name_edit.setStyleSheet(self._field_style())
        self.name_edit.setMinimumWidth(320)
        lay.addWidget(self.name_edit, stretch=3)

        # Number seen field
        num_lbl = make_label("Seen:", TNR_PT, color=TEXT_MUTED)
        lay.addWidget(num_lbl)

        self.count_edit = QLineEdit()
        self.count_edit.setPlaceholderText("0")
        self.count_edit.setFixedWidth(80)
        self.count_edit.setAlignment(Qt.AlignCenter)
        self.count_edit.setStyleSheet(self._field_style())
        lay.addWidget(self.count_edit)

    @staticmethod
    def _field_style():
        return f"""
            QLineEdit {{
                background: {MID_OCEAN};
                color: {TEXT_PRIMARY};
                border: 2px solid #1e5070;
                border-radius: 6px;
                padding: 8px 12px;
                font-family: {TNR};
                font-size: {TNR_PT}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {ACCENT_TEAL};
            }}
            QLineEdit::placeholder {{
                color: {TEXT_MUTED};
                font-style: italic;
            }}
        """

    def get_data(self):
        """Return (name_str, count_int) or raise ValueError."""
        name = self.name_edit.text().strip()
        raw  = self.count_edit.text().strip()
        if not name:
            raise ValueError(f"Row {self.index}: species name is empty.")
        if not raw:
            raise ValueError(f"Row {self.index}: number seen is empty.")
        try:
            count = int(raw)
            if count < 0:
                raise ValueError()
        except ValueError:
            raise ValueError(f"Row {self.index}: '{raw}' is not a valid whole number.")
        return name, count



#  GUI Interface

class EDNAApp(QMainWindow):

    MAX_SPECIES = 10

    def __init__(self):
        super().__init__()
        self.setWindowTitle("eDNA Species Frequency Calculator — Holyrood Subsea Observatory")
        self.setMinimumSize(1000, 750)
        self._build_ui()
        self._apply_global_style()

    
    def _apply_global_style(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background: {DEEP_OCEAN}; }}
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{
                background: {MID_OCEAN}; width: 8px; border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {ACCENT_TEAL}; border-radius: 4px; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QToolTip {{
                background: {CARD_BG}; color: {TEXT_PRIMARY};
                border: 1px solid {ACCENT_TEAL}; padding: 4px;
            }}
        """)

   
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)   
        root.addWidget(self._build_header())

        
        content = QHBoxLayout()
        content.setSpacing(20)
        content.addWidget(self._build_input_panel(), stretch=5)
        content.addWidget(self._build_result_panel(), stretch=6)

        root.addLayout(content)
        root.addWidget(self._build_button_bar())

   
    def _build_header(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {PANEL_BG}, stop:0.5 #0d3050, stop:1 {PANEL_BG});
            border: 1px solid #1a5070;
            border-radius: 12px;
        """)
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(20, 14, 20, 14)
        lay.setSpacing(4)

        title = QLabel(" eDNA Frequency Calculator")
        title.setStyleSheet(f"""
            font-family: {TNR};
            font-size: 22pt;
            font-weight: bold;
            color: {ACCENT_GLOW};
            background: transparent;
        """)
        lay.addWidget(title)

        sub = QLabel("Holyrood Subsea Observatory  ·  Enter up to 10 species, "
                     "then click Calculate to see percentage frequencies.")
        sub.setStyleSheet(
            f"color: {TEXT_MUTED}; font-family: {TNR}; font-size: {TNR_PT}pt;"
            f" font-style: italic; background: transparent;"
        )
        lay.addWidget(sub)

        shadow(frame, radius=24, color=ACCENT_TEAL)
        return frame

   
    def _build_input_panel(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {PANEL_BG};
                border: 1px solid #1a4060;
                border-radius: 12px;
            }}
        """)
        outer = QVBoxLayout(frame)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(10)

        hdr = make_label("  Species Input", TNR_PT + 2, bold=True, color=ACCENT_TEAL)
        outer.addWidget(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: #1a4060;")
        outer.addWidget(sep)

        # Scroll area for rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.rows_layout = QVBoxLayout(container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(6)
        self.rows_layout.addStretch()

        scroll.setWidget(container)
        outer.addWidget(scroll)

        
        btn_row = QHBoxLayout()
        self.add_btn = self._make_small_btn("＋  Add Species", ACCENT_TEAL, DEEP_OCEAN)
        self.add_btn.clicked.connect(self._add_row)
        self.remove_btn = self._make_small_btn("－  Remove Last", "#e05050", "#fff")
        self.remove_btn.clicked.connect(self._remove_row)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addStretch()
        outer.addLayout(btn_row)

        
        self.counter_lbl = make_label("0 / 10 species added", TNR_PT - 2, color=TEXT_MUTED)
        outer.addWidget(self.counter_lbl)

        self.input_rows: list[SpeciesInputRow] = []

        # By default 10 rows (initially)

        defaults = [
            ("Snow crab (Chionecetes opilio)",                        19),
            ("Acadian hermit crab (Pagurus acadianus)",                3),
            ("Western Atlantic Hairy Hermit Crab (Pagurus arcuatus)",  1),
            ("European Green Crab (Carcinus maenas)",                  9),
            ("Rock Crab (Cancer pagurus)",                            10),
            ("Jonah Crab (Cancer borealis)",                           5),
            ("Spiny Sunstar (Crossaster papposus)",                    8),
            ("Sea Urchin (Strongylocentrotus droebachiensis)",        10),
            ("Boreal Sea Star (Boreal asterias)",                     12),
            ("Daisy brittle star (Ophiopholis aculeata)",              7),
        ]
        for name, count in defaults:
            self._add_row(name, count)

        return frame

    def _add_row(self, name="", count=""):
        if len(self.input_rows) >= self.MAX_SPECIES:
            QMessageBox.information(self, "Limit reached",
                                    "Maximum 10 species can be entered.")
            return
        idx  = len(self.input_rows) + 1
        row  = SpeciesInputRow(idx)
        if name:
            row.name_edit.setText(str(name))
        if count != "":
            row.count_edit.setText(str(count))
        
        self.rows_layout.insertWidget(self.rows_layout.count() - 1, row)
        self.input_rows.append(row)
        self._update_counter()

    def _remove_row(self):
        if not self.input_rows:
            return
        row = self.input_rows.pop()
        self.rows_layout.removeWidget(row)
        row.deleteLater()
        self._update_counter()

    def _update_counter(self):
        n = len(self.input_rows)
        self.counter_lbl.setText(f"{n} / {self.MAX_SPECIES} species added")
        self.add_btn.setEnabled(n < self.MAX_SPECIES)

    
    def _build_result_panel(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {PANEL_BG};
                border: 1px solid #1a4060;
                border-radius: 12px;
            }}
        """)
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        hdr = make_label("  Frequency Results", TNR_PT + 2, bold=True, color=ACCENT_TEAL)
        lay.addWidget(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: #1a4060;")
        lay.addWidget(sep)

        
        stats = QHBoxLayout()
        self.total_lbl  = self._stat_card("Total Seen", "—")
        self.count_lbl  = self._stat_card("No. Species", "—")
        self.max_lbl    = self._stat_card("Most Common", "—")
        stats.addWidget(self.total_lbl[0])
        stats.addWidget(self.count_lbl[0])
        stats.addWidget(self.max_lbl[0])
        lay.addLayout(stats)

        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Species", "Number Seen", "% Frequency"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(False)
        self.table.setStyleSheet(self._table_style())
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self.table)

        return frame

    def _stat_card(self, title: str, value: str):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {CARD_BG};
                border: 1px solid #1a4060;
                border-radius: 8px;
            }}
        """)
        vl = QVBoxLayout(frame)
        vl.setContentsMargins(10, 8, 10, 8)
        vl.setSpacing(2)
        t = QLabel(title)
        t.setStyleSheet(
            f"color:{TEXT_MUTED}; font-family:{TNR}; font-size:{TNR_PT - 2}pt;"
            f" font-style:italic; background:transparent;"
        )
        t.setAlignment(Qt.AlignCenter)
        v = QLabel(value)
        v.setStyleSheet(
            f"color:{ACCENT_GLOW}; font-family:{TNR}; font-size:{TNR_PT + 2}pt;"
            f" font-weight:bold; background:transparent;"
        )
        v.setAlignment(Qt.AlignCenter)
        vl.addWidget(t); vl.addWidget(v)
        return frame, v  

    @staticmethod
    def _table_style():
        return f"""
            QTableWidget {{
                background: {ROW_EVEN};
                color: {TEXT_PRIMARY};
                gridline-color: #1a4060;
                border: 1px solid #1a4060;
                border-radius: 8px;
                font-family: {TNR};
                font-size: {TNR_PT}pt;
                outline: none;
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                border-bottom: 1px solid #1a3050;
            }}
            QTableWidget::item:selected {{
                background: #1a5070;
                color: {TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background: {HEADER_BG};
                color: {ACCENT_TEAL};
                font-family: {TNR};
                font-weight: bold;
                font-size: {TNR_PT}pt;
                padding: 10px 12px;
                border: none;
                border-bottom: 2px solid {ACCENT_TEAL};
            }}
        """

    
    def _build_button_bar(self):
        frame = QFrame()
        frame.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        calc_btn = self._make_btn(" Calculate Frequency", ACCENT_TEAL, DEEP_OCEAN)
        calc_btn.clicked.connect(self._calculate)
        shadow(calc_btn, radius=20, color=ACCENT_TEAL)

        clear_btn = self._make_btn(" Clear All", "#e05050", "#fff")
        clear_btn.clicked.connect(self._clear_all)

        export_btn = self._make_btn(" Copy Results", ACCENT_BLUE, "#fff")
        export_btn.clicked.connect(self._copy_results)

        lay.addStretch()
        lay.addWidget(clear_btn)
        lay.addWidget(export_btn)
        lay.addWidget(calc_btn)

        return frame

    
    @staticmethod
    def _make_btn(text, bg, fg, size=TNR_PT):
        btn = QPushButton(text)
        btn.setMinimumHeight(46)
        btn.setMinimumWidth(200)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {fg};
                border: none;
                border-radius: 8px;
                font-family: {TNR};
                font-size: {size}pt;
                font-weight: bold;
                padding: 8px 22px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {bg}, stop:1 #ffffff30);
            }}
            QPushButton:pressed {{ opacity: 0.8; }}
            QPushButton:disabled {{ background: #333; color: #666; }}
        """)
        return btn

    @staticmethod
    def _make_small_btn(text, bg, fg):
        btn = QPushButton(text)
        btn.setMinimumHeight(36)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {fg};
                border: none;
                border-radius: 6px;
                font-family: {TNR};
                font-size: {TNR_PT - 2}pt;
                font-weight: bold;
                padding: 5px 16px;
            }}
            QPushButton:hover {{ opacity: 0.85; }}
            QPushButton:disabled {{ background: #333; color: #666; }}
        """)
        return btn

    # Caluculation logic
    def _calculate(self):
        if not self.input_rows:
            QMessageBox.warning(self, "No Data", "Please add at least one species.")
            return

        
        rows_data = []
        for row in self.input_rows:
            try:
                name, count = row.get_data()
                rows_data.append((name, count))
            except ValueError as e:
                QMessageBox.critical(self, "Input Error", str(e))
                return

        total = sum(c for _, c in rows_data)
        if total == 0:
            QMessageBox.warning(self, "Zero Total",
                                "Total number seen is zero — cannot divide by zero.")
            return

        
        n = len(rows_data)
        self.table.setRowCount(n + 1)   # +1 for total row

        for i, (name, count) in enumerate(rows_data):
            pct = (count / total) * 100
            bg  = QColor(ROW_EVEN) if i % 2 == 0 else QColor(ROW_ODD)

            items = [
                QTableWidgetItem(name),
                self._centered_item(str(count)),
                self._centered_item(f"{pct:.8f}"),
            ]
            tnr_font = QFont("Times New Roman", TNR_PT)
            for col, item in enumerate(items):
                item.setBackground(bg)
                item.setForeground(QColor(TEXT_PRIMARY))
                item.setFont(tnr_font)
                self.table.setItem(i, col, item)

        
        total_row = n
        total_bg  = QColor(TOTAL_BG)
        t_items   = [
            QTableWidgetItem("  TOTAL"),
            self._centered_item(str(total)),
            self._centered_item("100.00000000"),
        ]
        for col, item in enumerate(t_items):
            item.setBackground(total_bg)
            item.setForeground(QColor(ACCENT_GLOW))
            tnr_bold = QFont("Times New Roman", TNR_PT)
            tnr_bold.setBold(True)
            item.setFont(tnr_bold)
            self.table.setItem(total_row, col, item)

        
        self.total_lbl[1].setText(str(total))
        self.count_lbl[1].setText(str(n))
        max_name, max_count = max(rows_data, key=lambda x: x[1])
        short = max_name.split("(")[0].strip()
        self.max_lbl[1].setText(f"{short[:18]}… ({max_count})" if len(short) > 18
                                else f"{short} ({max_count})")

        self.table.resizeRowsToContents()

    @staticmethod
    def _centered_item(text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def _clear_all(self):
        reply = QMessageBox.question(
            self, "Clear All",
            "Remove all species rows and clear the results table?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            while self.input_rows:
                self._remove_row()
            self.table.setRowCount(0)
            self.total_lbl[1].setText("—")
            self.count_lbl[1].setText("—")
            self.max_lbl[1].setText("—")

    def _copy_results(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "Nothing to copy",
                                    "Calculate results first.")
            return
        lines = ["Species\tNumber Seen\t% Frequency"]
        for row in range(self.table.rowCount()):
            cols = [self.table.item(row, c).text().strip()
                    for c in range(self.table.columnCount())]
            lines.append("\t".join(cols))
        QApplication.clipboard().setText("\n".join(lines))
        QMessageBox.information(self, "Copied",
                                "Results copied to clipboard as tab-separated text.")



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set Times New Roman , font size : 16pt 

    app_font = QFont("Times New Roman", TNR_PT)
    app.setFont(app_font)

    
    pal = QPalette()
    pal.setColor(QPalette.Window,          QColor(DEEP_OCEAN))
    pal.setColor(QPalette.WindowText,      QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Base,            QColor(MID_OCEAN))
    pal.setColor(QPalette.AlternateBase,   QColor(PANEL_BG))
    pal.setColor(QPalette.Text,            QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Button,          QColor(PANEL_BG))
    pal.setColor(QPalette.ButtonText,      QColor(TEXT_PRIMARY))
    pal.setColor(QPalette.Highlight,       QColor(ACCENT_TEAL))
    pal.setColor(QPalette.HighlightedText, QColor(DEEP_OCEAN))
    app.setPalette(pal)

    window = EDNAApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
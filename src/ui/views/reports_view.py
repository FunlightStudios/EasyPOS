from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QDateEdit,
    QTableWidget
)
from PySide6.QtCore import QDate

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Top controls
        controls = QHBoxLayout()
        
        # Report type selection
        self.report_type = QComboBox()
        self.report_type.addItems([
            "Tagesumsatz",
            "Produktverkäufe",
            "Lagerbestand",
            "Kundenanalyse"
        ])
        
        # Date range
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate())
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        
        # Export button
        self.export_btn = QPushButton("Exportieren")
        
        controls.addWidget(QLabel("Bericht:"))
        controls.addWidget(self.report_type)
        controls.addWidget(QLabel("Von:"))
        controls.addWidget(self.date_from)
        controls.addWidget(QLabel("Bis:"))
        controls.addWidget(self.date_to)
        controls.addWidget(self.export_btn)
        
        # Statistics grid
        stats = QGridLayout()
        stats_widgets = [
            ("Gesamtumsatz:", "0,00 €"),
            ("Anzahl Verkäufe:", "0"),
            ("Durchschn. Verkauf:", "0,00 €"),
            ("Meistverkauftes Produkt:", "-")
        ]
        
        row = 0
        for label, value in stats_widgets:
            stats.addWidget(QLabel(label), row, 0)
            stats.addWidget(QLabel(value), row, 1)
            row += 1
            
        # Report table
        self.table = QTableWidget()
        
        # Add all widgets to main layout
        layout.addLayout(controls)
        layout.addLayout(stats)
        layout.addWidget(self.table)

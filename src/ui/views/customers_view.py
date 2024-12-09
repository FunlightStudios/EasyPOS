from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem
)

class CustomersView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Top toolbar
        toolbar = QHBoxLayout()
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kunden suchen...")
        toolbar.addWidget(self.search_input)
        
        # Buttons
        self.add_btn = QPushButton("Neuer Kunde")
        self.import_btn = QPushButton("Importieren")
        self.export_btn = QPushButton("Exportieren")
        
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.import_btn)
        toolbar.addWidget(self.export_btn)
        
        # Customer table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Kunden-Nr.", "Name", "Email", 
            "Telefon", "Adresse", "Registriert am"
        ])
        
        # Add widgets to main layout
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

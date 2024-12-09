from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFrame, QSpinBox,
    QDoubleSpinBox, QWidget, QGroupBox
)
from PySide6.QtCore import Qt
from src.services.tax_rate_service import TaxRateService
from src.services.settings_service import SettingsService

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_service = SettingsService.get_instance()
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.init_ui()
        self.load_tax_rates()
        
    def init_ui(self):
        self.setObjectName("settingsDialog")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title Bar
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QLabel("Einstellungen")
        title_label.setObjectName("titleLabel")
        close_button = QPushButton("×")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addWidget(close_button)
        layout.addWidget(title_bar)
        
        # Content Area
        content = QWidget()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(20)
        
        # Währung
        currency_group = QGroupBox("Währung")
        currency_layout = QVBoxLayout()
        
        self.currency_combo = QComboBox()
        currencies = [
            ("CHF", "Schweizer Franken"),
            ("EUR", "Euro"),
            ("USD", "US Dollar"),
            ("GBP", "Britisches Pfund"),
            ("JPY", "Japanischer Yen"),
            ("CNY", "Chinesischer Yuan"),
            ("AUD", "Australischer Dollar"),
            ("CAD", "Kanadischer Dollar"),
            ("SEK", "Schwedische Krone"),
            ("NOK", "Norwegische Krone"),
            ("DKK", "Dänische Krone")
        ]
        
        for code, name in currencies:
            self.currency_combo.addItem(f"{code} - {name}", code)
        
        # Setze die aktuelle Währung
        current_currency = self.settings_service.get_currency()
        index = self.currency_combo.findData(current_currency)
        if index >= 0:
            self.currency_combo.setCurrentIndex(index)
            
        currency_layout.addWidget(self.currency_combo)
        currency_group.setLayout(currency_layout)
        content_layout.addWidget(currency_group)
        
        # MwSt Verwaltung
        tax_label = QLabel("Mehrwertsteuersätze")
        tax_label.setObjectName("sectionHeader")
        content_layout.addWidget(tax_label)
        
        # MwSt Tabelle
        self.tax_table = QTableWidget()
        self.tax_table.setColumnCount(4)
        self.tax_table.setHorizontalHeaderLabels(["Name", "Satz (%)", "Standard", ""])
        self.tax_table.horizontalHeader().setStretchLastSection(True)
        content_layout.addWidget(self.tax_table)
        
        # Neuer MwSt Satz
        new_tax_frame = QFrame()
        new_tax_layout = QHBoxLayout(new_tax_frame)
        
        self.tax_name_input = QLineEdit()
        self.tax_name_input.setPlaceholderText("Name (z.B. Standard)")
        
        self.tax_rate_input = QDoubleSpinBox()
        self.tax_rate_input.setRange(0, 100)
        self.tax_rate_input.setValue(19)
        self.tax_rate_input.setSuffix("%")
        
        add_tax_btn = QPushButton("Hinzufügen")
        add_tax_btn.clicked.connect(self.add_tax_rate)
        
        new_tax_layout.addWidget(self.tax_name_input)
        new_tax_layout.addWidget(self.tax_rate_input)
        new_tax_layout.addWidget(add_tax_btn)
        
        content_layout.addWidget(new_tax_frame)
        
        # Buttons
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        save_btn = QPushButton("Speichern")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        content_layout.addWidget(button_container)
        layout.addWidget(content)
        
    def load_tax_rates(self):
        tax_rates = TaxRateService.get_all_tax_rates()
        self.tax_table.setRowCount(len(tax_rates))
        
        for i, tax in enumerate(tax_rates):
            name_item = QTableWidgetItem(tax.name)
            rate_item = QTableWidgetItem(f"{tax.rate * 100:.1f}")
            default_item = QTableWidgetItem("✓" if tax.is_default else "")
            default_item.setTextAlignment(Qt.AlignCenter)
            
            delete_btn = QPushButton("Löschen")
            delete_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; border: none; padding: 5px; }")
            delete_btn.clicked.connect(lambda checked, x=tax.id: self.delete_tax_rate(x))
            
            self.tax_table.setItem(i, 0, name_item)
            self.tax_table.setItem(i, 1, rate_item)
            self.tax_table.setItem(i, 2, default_item)
            self.tax_table.setCellWidget(i, 3, delete_btn)
            
    def add_tax_rate(self):
        name = self.tax_name_input.text().strip()
        rate = self.tax_rate_input.value() / 100
        
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Namen ein.")
            return
            
        try:
            TaxRateService.create_tax_rate(name, rate)
            self.tax_name_input.clear()
            self.tax_rate_input.setValue(19)
            self.load_tax_rates()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))
            
    def delete_tax_rate(self, tax_id: int):
        try:
            TaxRateService.delete_tax_rate(tax_id)
            self.load_tax_rates()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))
            
    def accept(self):
        # Speichere die Währung
        selected_currency = self.currency_combo.currentData()
        self.settings_service.set_currency(selected_currency)
        
        super().accept()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 50:  # Nur in der Titelleiste
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragging') and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

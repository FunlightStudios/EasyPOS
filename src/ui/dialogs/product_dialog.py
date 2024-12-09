from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QMessageBox, QDoubleSpinBox, QSpinBox, QFrame,
    QWidget, QGridLayout
)
from PySide6.QtCore import Qt
from src.services.product_service import ProductService
from src.services.tax_rate_service import TaxRateService
from src.services.settings_service import SettingsService

class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.settings_service = SettingsService.get_instance()
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName("productDialog")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title Bar
        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(20, 10, 20, 10)
        
        title = QLabel(self.tr("Produkt anlegen") if not self.product else self.tr("Produkt bearbeiten"))
        title.setObjectName("titleLabel")
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.reject)
        close_btn.setFocusPolicy(Qt.NoFocus)  # Verhindert, dass der Button den Fokus erhält
        
        title_bar_layout.addWidget(title)
        title_bar_layout.addWidget(close_btn)
        layout.addWidget(title_bar)
        
        # Content Area
        content = QWidget()
        content.setObjectName("contentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 20, 40, 20)
        content_layout.setSpacing(20)
        
        # Grid layout for form
        form = QGridLayout()
        form.setSpacing(15)
        
        # Left Column
        current_row = 0
        
        # Name
        name_label = QLabel(self.tr("Name"))
        name_label.setObjectName("fieldLabel")
        self.name_input = QLineEdit()
        self.name_input.setObjectName("nameInput")
        if self.product:
            self.name_input.setText(self.product.name)
        form.addWidget(name_label, current_row, 0)
        form.addWidget(self.name_input, current_row, 1)
        
        current_row += 1
        
        # Barcode
        barcode_label = QLabel(self.tr("Barcode"))
        barcode_label.setObjectName("fieldLabel")
        self.barcode_input = QLineEdit()
        self.barcode_input.setObjectName("barcodeInput")
        if self.product:
            self.barcode_input.setText(self.product.barcode)
        form.addWidget(barcode_label, current_row, 0)
        form.addWidget(self.barcode_input, current_row, 1)
        
        current_row += 1
        
        # Category
        category_label = QLabel(self.tr("Kategorie"))
        category_label.setObjectName("fieldLabel")
        self.category_input = QComboBox()
        self.category_input.setObjectName("categoryInput")
        categories = ["Getränke", "Essen", "Snacks", "Sonstiges"]
        self.category_input.addItems(categories)
        if self.product and self.product.category in categories:
            self.category_input.setCurrentText(self.product.category)
        form.addWidget(category_label, current_row, 0)
        form.addWidget(self.category_input, current_row, 1)
        
        # Right Column
        current_row = 0
        
        # Price
        currency = self.settings_service.get_currency()
        price_label = QLabel(self.tr(f"Preis ({currency})"))
        price_label.setObjectName("fieldLabel")
        self.price_input = QDoubleSpinBox()
        self.price_input.setObjectName("priceInput")
        self.price_input.setRange(0, 9999.99)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(f" {currency}")
        if self.product:
            self.price_input.setValue(self.product.price)
        form.addWidget(price_label, current_row, 2)
        form.addWidget(self.price_input, current_row, 3)
        
        current_row += 1
        
        # Cost Price
        cost_price_label = QLabel(self.tr(f"Einkaufspreis ({currency})"))
        cost_price_label.setObjectName("fieldLabel")
        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setObjectName("costPriceInput")
        self.cost_price_input.setRange(0, 9999.99)
        self.cost_price_input.setDecimals(2)
        self.cost_price_input.setSuffix(f" {currency}")
        if self.product:
            self.cost_price_input.setValue(self.product.cost_price or 0)
        form.addWidget(cost_price_label, current_row, 2)
        form.addWidget(self.cost_price_input, current_row, 3)
        
        current_row += 1
        
        # Tax Rate
        tax_rate_label = QLabel(self.tr("MwSt"))
        tax_rate_label.setObjectName("fieldLabel")
        self.tax_rate_combo = QComboBox()
        self.load_tax_rates()
        form.addWidget(tax_rate_label, current_row, 2)
        form.addWidget(self.tax_rate_combo, current_row, 3)
        current_row += 1
        
        # Inventory Section
        inventory_title = QLabel(self.tr("Lagerbestand"))
        inventory_title.setObjectName("sectionTitle")
        content_layout.addWidget(inventory_title)
        
        inventory_form = QGridLayout()
        inventory_form.setSpacing(15)
        
        # Quantity
        quantity_label = QLabel(self.tr("Aktueller Bestand"))
        quantity_label.setObjectName("fieldLabel")
        self.quantity_input = QSpinBox()
        self.quantity_input.setObjectName("quantityInput")
        self.quantity_input.setRange(0, 999999)
        if self.product and self.product.inventory:
            self.quantity_input.setValue(self.product.inventory.quantity)
        inventory_form.addWidget(quantity_label, 0, 0)
        inventory_form.addWidget(self.quantity_input, 0, 1)
        
        # Minimum Stock
        min_stock_label = QLabel(self.tr("Mindestbestand"))
        min_stock_label.setObjectName("fieldLabel")
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setObjectName("minStockInput")
        self.min_stock_input.setRange(0, 999999)
        if self.product and self.product.inventory:
            self.min_stock_input.setValue(self.product.inventory.minimum_stock)
        inventory_form.addWidget(min_stock_label, 0, 2)
        inventory_form.addWidget(self.min_stock_input, 0, 3)
        
        content_layout.addLayout(form)
        content_layout.addLayout(inventory_form)
        content_layout.addStretch()
        
        # Buttons
        button_container = QWidget()
        button_container.setObjectName("buttonContainer")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        save_btn = QPushButton(self.tr("Speichern"))
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_product)
        save_btn.setFocusPolicy(Qt.NoFocus)  # Kein Fokus für Speichern-Button
        
        cancel_btn = QPushButton(self.tr("Abbrechen"))
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFocusPolicy(Qt.NoFocus)  # Kein Fokus für Abbrechen-Button
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        content_layout.addWidget(button_container)
        layout.addWidget(content)

        # Setze den Fokus auf das Barcode-Eingabefeld
        self.barcode_input.setFocus()
        
    def load_tax_rates(self):
        """Lädt die verfügbaren MwSt-Sätze in die Combobox"""
        self.tax_rate_combo.clear()
        tax_rates = TaxRateService.get_all_tax_rates()
        
        for tax in tax_rates:
            self.tax_rate_combo.addItem(f"{tax.name} ({tax.rate * 100:.1f}%)", tax.rate)
            
        # Setze den Standard-MwSt-Satz oder den des Produkts
        if self.product and self.product.tax_rate:
            # Finde den Index des aktuellen MwSt-Satzes
            index = self.tax_rate_combo.findData(self.product.tax_rate)
            if index >= 0:
                self.tax_rate_combo.setCurrentIndex(index)
        else:
            # Setze den Standard-MwSt-Satz
            default_tax = TaxRateService.get_default_tax_rate()
            if default_tax:
                index = self.tax_rate_combo.findData(default_tax.rate)
                if index >= 0:
                    self.tax_rate_combo.setCurrentIndex(index)
                    
    def save_product(self):
        name = self.name_input.text().strip()
        barcode = self.barcode_input.text().strip()
        price = self.price_input.value()
        cost_price = self.cost_price_input.value()
        tax_rate = self.tax_rate_combo.currentData()  # Hole den ausgewählten MwSt-Satz
        category = self.category_input.currentText()
        quantity = self.quantity_input.value()
        min_stock = self.min_stock_input.value()
        
        if not name:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie einen Namen ein.")
            return
            
        try:
            if self.product:
                ProductService.update_product(
                    self.product.id,
                    name=name,
                    barcode=barcode,
                    price=price,
                    cost_price=cost_price,
                    tax_rate=tax_rate,
                    category=category,
                    quantity=quantity,
                    minimum_stock=min_stock
                )
            else:
                ProductService.create_product(
                    name=name,
                    barcode=barcode,
                    price=price,
                    cost_price=cost_price,
                    tax_rate=tax_rate,
                    category=category,
                    quantity=quantity,
                    minimum_stock=min_stock
                )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern: {str(e)}")
            
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel,
    QLineEdit, QHeaderView
)
from PySide6.QtCore import Qt
from src.services.product_service import ProductService
from src.services.settings_service import SettingsService
from src.ui.dialogs.product_dialog import ProductDialog

class InventoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.product_service = ProductService()
        self.settings_service = SettingsService.get_instance()
        self.init_ui()
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Lager")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suchen...")
        self.search_input.textChanged.connect(self.filter_products)
        header_layout.addWidget(self.search_input)
        
        # Add Product Button
        add_btn = QPushButton("+ Produkt hinzufügen")
        add_btn.clicked.connect(self.show_add_dialog)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)

        # Products Table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "Name", "Barcode", "Preis", "Bestand", "Min. Bestand", "MwSt"
        ])
        
        # Set column widths
        self.products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Name
        for i in range(1, 6):  # Other columns
            self.products_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
            self.products_table.setColumnWidth(i, 100)
        
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        self.products_table.doubleClicked.connect(self.show_edit_dialog)
        
        layout.addWidget(self.products_table)

    def load_products(self):
        """Lädt alle Produkte in die Tabelle"""
        products = self.product_service.get_all_products()
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # Name
            self.products_table.setItem(row, 0, QTableWidgetItem(product.name))
            
            # Barcode
            self.products_table.setItem(row, 1, QTableWidgetItem(product.barcode))
            
            # Preis
            price_item = QTableWidgetItem(self.settings_service.format_currency(product.price))
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 2, price_item)
            
            # Bestand
            inventory = getattr(product, 'inventory', None)
            quantity = inventory.quantity if inventory else 0
            qty_item = QTableWidgetItem(str(quantity))
            qty_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 3, qty_item)
            
            # Min. Bestand
            min_stock = inventory.minimum_stock if inventory else 0
            min_stock_item = QTableWidgetItem(str(min_stock))
            min_stock_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 4, min_stock_item)
            
            # MwSt
            tax_item = QTableWidgetItem(f"{product.tax_rate * 100:.1f}%")
            tax_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 5, tax_item)
            
            # Warnfarbe wenn Bestand unter Minimum
            if quantity < min_stock:
                for col in range(self.products_table.columnCount()):
                    item = self.products_table.item(row, col)
                    item.setBackground(Qt.yellow)

    def filter_products(self, text):
        """Filtert die Produkte nach Suchtext"""
        for row in range(self.products_table.rowCount()):
            show = False
            for col in range(self.products_table.columnCount()):
                item = self.products_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show = True
                    break
            self.products_table.setRowHidden(row, not show)

    def show_add_dialog(self):
        """Zeigt den Dialog zum Hinzufügen eines Produkts"""
        dialog = ProductDialog(self)
        if dialog.exec_() == ProductDialog.Accepted:
            self.load_products()

    def show_edit_dialog(self, index):
        """Zeigt den Dialog zum Bearbeiten eines Produkts"""
        row = index.row()
        product_name = self.products_table.item(row, 0).text()
        product = self.product_service.get_product_by_name(product_name)
        
        if product:
            dialog = ProductDialog(self, product)
            if dialog.exec_() == ProductDialog.Accepted:
                self.load_products()

    def update_display(self):
        """Aktualisiert die Anzeige (z.B. nach Währungsänderungen)"""
        self.load_products()

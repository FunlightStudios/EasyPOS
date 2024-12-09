from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy, QMessageBox,
    QMenu, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from src.ui.controllers.pos_controller import POSController
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.services.settings_service import SettingsService

class POSView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = POSController()
        self.settings_service = SettingsService.get_instance()
        self.controller.cart_updated.connect(self.update_cart)
        self.controller.error_occurred.connect(self.show_error)
        self.controller.sale_completed.connect(self.handle_sale_completed)
        self.controller.settings_updated.connect(self.update_display)
        self.setObjectName("posView")
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left side - Cart
        cart_widget = QWidget()
        cart_layout = QVBoxLayout(cart_widget)
        cart_layout.setContentsMargins(20, 20, 20, 20)
        cart_layout.setSpacing(10)
        
        # Cart header with search
        header_layout = QHBoxLayout()
        
        cart_header = QLabel("Warenkorb")
        cart_header.setObjectName("sectionHeader")
        header_layout.addWidget(cart_header)
        
        # Barcode input with icon
        barcode_layout = QHBoxLayout()
        barcode_label = QLabel("🔍")
        barcode_layout.addWidget(barcode_label)
        
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode scannen oder eingeben...")
        self.barcode_input.returnPressed.connect(self.add_product)
        barcode_layout.addWidget(self.barcode_input)
        
        header_layout.addLayout(barcode_layout)
        cart_layout.addLayout(header_layout)
        
        # Cart table with context menu
        self.cart_table = QTableWidget()
        self.cart_table.setObjectName("cartTable")
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels([
            "Artikel", "Preis", "Menge", "Rabatt", "MwSt", "Gesamt"
        ])
        
        # Set column widths
        self.cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 6):
            self.cart_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Fixed)
            self.cart_table.setColumnWidth(i, 100)
            
        # Enable context menu
        self.cart_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.cart_table.customContextMenuRequested.connect(self.show_context_menu)
        
        cart_layout.addWidget(self.cart_table)
        
        # Total and checkout
        totals_layout = QHBoxLayout()
        
        self.subtotal_label = QLabel("Zwischensumme: ")
        self.subtotal_label.setObjectName("totalLabel")
        self.subtotal_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.subtotal_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        totals_layout.addWidget(self.subtotal_label)
        
        self.tax_label = QLabel("MwSt: ")
        self.tax_label.setObjectName("totalLabel")
        self.tax_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tax_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        totals_layout.addWidget(self.tax_label)
        
        self.discount_label = QLabel("Rabatt: ")
        self.discount_label.setObjectName("totalLabel")
        self.discount_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.discount_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        totals_layout.addWidget(self.discount_label)
        
        self.total_label = QLabel("Gesamt: ")
        self.total_label.setObjectName("totalLabel")
        self.total_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_label.setStyleSheet("""
            QLabel {
                color: #2196F3;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        totals_layout.addWidget(self.total_label)
        
        # Payment buttons layout
        payment_layout = QHBoxLayout()
        payment_layout.setSpacing(20)
        payment_layout.setContentsMargins(0, 20, 0, 20)
        
        # Zahlungsbuttons mit direkter Styling
        cash_btn = QPushButton("BAR")
        cash_btn.setObjectName("cashButton")
        cash_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; min-height: 80px; min-width: 120px; font-size: 16px; }")
        cash_btn.clicked.connect(lambda: self.checkout("cash"))
        cash_btn.setCursor(Qt.PointingHandCursor)
        
        twint_btn = QPushButton("TWINT")
        twint_btn.setObjectName("twintButton")
        twint_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border: none; min-height: 80px; min-width: 120px; font-size: 16px; }")
        twint_btn.clicked.connect(lambda: self.checkout("twint"))
        twint_btn.setCursor(Qt.PointingHandCursor)
        
        card_btn = QPushButton("KARTE")
        card_btn.setObjectName("cardButton")
        card_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; border: none; min-height: 80px; min-width: 120px; font-size: 16px; }")
        card_btn.clicked.connect(lambda: self.checkout("card"))
        card_btn.setCursor(Qt.PointingHandCursor)
        
        other_btn = QPushButton("ANDERE")
        other_btn.setObjectName("otherButton")
        other_btn.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; border: none; min-height: 80px; min-width: 120px; font-size: 16px; }")
        other_btn.clicked.connect(lambda: self.checkout("other"))
        other_btn.setCursor(Qt.PointingHandCursor)
        
        # Füge die Buttons zum Payment Layout hinzu mit stretch factor
        payment_layout.addWidget(cash_btn, 1)
        payment_layout.addWidget(twint_btn, 1)
        payment_layout.addWidget(card_btn, 1)
        payment_layout.addWidget(other_btn, 1)
        
        cart_layout.addLayout(totals_layout)
        cart_layout.addLayout(payment_layout)
        
        # Right side - Quick actions
        actions_widget = QWidget()
        actions_widget.setObjectName("actionsPanel")
        actions_widget.setFixedWidth(200)
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setContentsMargins(10, 20, 10, 20)
        actions_layout.setSpacing(10)
        
        # Actions header
        actions_header = QLabel("Aktionen")
        actions_header.setObjectName("sectionHeader")
        actions_layout.addWidget(actions_header)
        
        # Action buttons
        button_style = """
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                padding: 8px;
                min-height: 30px;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        """
        
        clear_btn = QPushButton("Warenkorb leeren")
        clear_btn.setStyleSheet(button_style)
        clear_btn.clicked.connect(self.clear_cart)
        
        discount_btn = QPushButton("Rabatt")
        discount_btn.setStyleSheet(button_style)
        
        cancel_btn = QPushButton("Stornieren")
        cancel_btn.setStyleSheet(button_style)
        
        # Füge die Buttons zum Layout hinzu
        actions_layout.addWidget(clear_btn)
        actions_layout.addWidget(discount_btn)
        actions_layout.addWidget(cancel_btn)
        actions_layout.addStretch()
        
        # Add widgets to main layout
        layout.addWidget(cart_widget, stretch=1)
        layout.addWidget(actions_widget)
        
        # Set focus to barcode input
        self.barcode_input.setFocus()
        
    def add_product(self, barcode=None):
        """Fügt ein Produkt zum Warenkorb hinzu"""
        if not barcode:
            barcode = self.barcode_input.text().strip()
            self.barcode_input.clear()
            
        if not barcode:
            return
            
        # Füge zum Warenkorb hinzu
        self.controller.add_to_cart(barcode)
        self.update_cart()
        
    def format_price(self, price):
        """Formatiert einen Preis mit der aktuellen Währung"""
        return self.settings_service.format_currency(price)
        
    def update_cart(self):
        """Aktualisiert die Anzeige des Warenkorbs"""
        self.cart_table.clearContents()
        self.cart_table.setRowCount(0)
        
        cart_items = self.controller.get_cart_items()
        totals = self.controller.get_cart_total()
        
        for row, item in enumerate(cart_items):
            self.cart_table.insertRow(row)
            
            # Name
            name_item = QTableWidgetItem(item.product.name)
            self.cart_table.setItem(row, 0, name_item)
            
            # Einzelpreis
            price_item = QTableWidgetItem(self.settings_service.format_currency(item.product.price))
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 1, price_item)
            
            # Menge
            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 2, qty_item)
            
            # Rabatt
            if hasattr(item, 'discount') and item.discount > 0:
                discount_item = QTableWidgetItem(f"{item.discount}%")
            else:
                discount_item = QTableWidgetItem("-")
            discount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 3, discount_item)
            
            # MwSt
            tax_item = QTableWidgetItem(f"{item.product.tax_rate * 100:.1f}%")
            tax_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 4, tax_item)
            
            # Gesamtpreis
            row_total = item.product.price * item.quantity
            if hasattr(item, 'discount') and item.discount > 0:
                row_total -= row_total * (item.discount / 100)
            total_item = QTableWidgetItem(self.settings_service.format_currency(row_total))
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 5, total_item)
        
        # Aktualisiere Summen
        self.subtotal_label.setText(f"Zwischensumme: {self.settings_service.format_currency(totals['subtotal'])}")
        self.tax_label.setText(f"MwSt: {self.settings_service.format_currency(totals['tax_total'])}")
        if totals['discounts'] > 0:
            self.discount_label.setText(f"Rabatt: -{self.settings_service.format_currency(totals['discounts'])}")
            self.discount_label.setVisible(True)
        else:
            self.discount_label.setVisible(False)
        self.total_label.setText(f"Gesamt: {self.settings_service.format_currency(totals['total'])}")
        
    def clear_cart(self):
        self.controller.clear_cart()
        self.update_cart()
        
    def checkout(self, payment_method):
        """Führt den Bezahlvorgang durch"""
        if not self.controller.get_cart_items():
            QMessageBox.warning(self, "Warnung", "Der Warenkorb ist leer")
            return
            
        self.controller.complete_sale(payment_method)
            
    def show_error(self, message: str):
        QMessageBox.critical(self, "Fehler", message)

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
        
    def handle_sale_completed(self, sale_id: int):
        QMessageBox.information(self, "Erfolg", f"Verkauf #{sale_id} erfolgreich abgeschlossen!")
        self.update_cart()

    def update_display(self):
        """Aktualisiert die Anzeige (z.B. nach Änderungen in den Einstellungen)"""
        self.update_cart()  # Dies wird auch die Währung aktualisieren

    def show_context_menu(self, pos):
        """Zeigt das Kontextmenü für Warenkorb-Einträge"""
        row = self.cart_table.rowAt(pos.y())
        if row >= 0:
            menu = QMenu(self)
            
            # Menge ändern
            quantity_action = QAction("Menge ändern", self)
            quantity_action.triggered.connect(lambda: self.change_quantity(row))
            menu.addAction(quantity_action)
            
            # Rabatt hinzufügen
            discount_action = QAction("Rabatt", self)
            discount_action.triggered.connect(lambda: self.add_discount(row))
            menu.addAction(discount_action)
            
            # Entfernen
            remove_action = QAction("Entfernen", self)
            remove_action.triggered.connect(lambda: self.remove_item(row))
            menu.addAction(remove_action)
            
            # Zeige Menü
            menu.exec_(self.cart_table.viewport().mapToGlobal(pos))
            
    def change_quantity(self, row):
        """Dialog zum Ändern der Menge"""
        item = self.cart_table.item(row, 2)
        current_qty = int(item.text())
        
        quantity, ok = QInputDialog.getInt(
            self, "Menge ändern",
            "Neue Menge eingeben:",
            current_qty, 1, 9999, 1
        )
        
        if ok:
            self.controller.update_item_quantity(row, quantity)
            
    def add_discount(self, row):
        """Dialog zum Hinzufügen eines Rabatts"""
        discount, ok = QInputDialog.getDouble(
            self, "Rabatt hinzufügen",
            "Rabatt in % (0-100):",
            0, 0, 100, 1
        )
        
        if ok:
            self.controller.apply_discount(row, discount)
            
    def remove_item(self, row):
        """Entfernt ein Produkt aus dem Warenkorb"""
        if QMessageBox.question(
            self,
            "Produkt entfernen",
            "Möchten Sie dieses Produkt wirklich aus dem Warenkorb entfernen?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            self.controller.remove_item(row)

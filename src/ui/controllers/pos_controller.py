from PySide6.QtCore import QObject, Signal
from src.services.product_service import ProductService
from src.services.sale_service import SaleService
from src.database.database import SessionLocal
from src.models.sale import Sale, SaleItem
from datetime import datetime
from src.services.settings_service import SettingsService

class POSController(QObject):
    cart_updated = Signal()
    error_occurred = Signal(str)
    sale_completed = Signal(int)  # sale_id
    settings_updated = Signal()  # Neues Signal für Einstellungsänderungen
    quantity_changed = Signal(int, int)  # product_id, new_quantity

    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self._cart_items = []  # Liste von CartItems
        self.current_user_id = None
        self.settings_service = SettingsService.get_instance()

    @property
    def cart_items(self):
        return self._cart_items

    def get_cart_items(self):
        return self._cart_items

    def set_current_user(self, user_id: int):
        self.current_user_id = user_id

    def add_to_cart(self, barcode, quantity=1):
        """Fügt ein Produkt zum Warenkorb hinzu"""
        try:
            # Get product from database
            product = ProductService.get_product_by_barcode(barcode)
            if not product:
                self.error_occurred.emit(f"Produkt mit Barcode {barcode} nicht gefunden")
                return False

            # Check if product already in cart
            for item in self._cart_items:
                if item.product.barcode == product.barcode:
                    if product.inventory and item.quantity + quantity > product.inventory.quantity:
                        self.error_occurred.emit("Nicht genügend Lagerbestand")
                        return False
                    item.quantity += quantity
                    self.cart_updated.emit()
                    return True

            # Add new product to cart
            if product.inventory is None or product.inventory.quantity < quantity:
                self.error_occurred.emit("Produkt nicht auf Lager")
                return False

            self._cart_items.append(CartItem(product, quantity))
            self.cart_updated.emit()
            return True

        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    def clear_cart(self):
        self._cart_items.clear()
        self.cart_updated.emit()

    def update_item_quantity(self, row: int, new_quantity: int) -> bool:
        """Aktualisiert die Menge eines Produkts im Warenkorb"""
        try:
            if 0 <= row < len(self._cart_items):
                item = self._cart_items[row]
                if item.product.inventory and new_quantity > item.product.inventory.quantity:
                    self.error_occurred.emit("Nicht genügend Lagerbestand")
                    return False
                    
                if new_quantity <= 0:
                    self._cart_items.pop(row)
                else:
                    item.quantity = new_quantity
                    
                self.cart_updated.emit()
                self.quantity_changed.emit(item.product.id, new_quantity)
                return True
            return False
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False
            
    def remove_item(self, row: int) -> bool:
        """Entfernt ein Produkt aus dem Warenkorb"""
        try:
            if 0 <= row < len(self._cart_items):
                self._cart_items.pop(row)
                self.cart_updated.emit()
                return True
            return False
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    def apply_discount(self, row: int, discount_percent: float) -> bool:
        """Wendet einen Rabatt auf ein Produkt an"""
        try:
            if 0 <= row < len(self._cart_items):
                item = self._cart_items[row]
                if 0 <= discount_percent <= 100:
                    item.discount = discount_percent
                    self.cart_updated.emit()
                    return True
            return False
        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    def get_cart_total(self) -> dict:
        """Berechnet die Gesamtsummen für den Warenkorb"""
        try:
            subtotal = 0
            tax_total = 0
            discounts = 0
            
            for item in self._cart_items:
                item_price = item.product.price * item.quantity
                if hasattr(item, 'discount') and item.discount > 0:
                    discount_amount = item_price * (item.discount / 100)
                    discounts += discount_amount
                    item_price -= discount_amount
                    
                subtotal += item_price
                tax_total += item_price * item.product.tax_rate
                
            return {
                'subtotal': subtotal,
                'tax_total': tax_total,
                'discounts': discounts,
                'total': subtotal + tax_total
            }
        except Exception as e:
            self.error_occurred.emit(str(e))
            return {'subtotal': 0, 'tax_total': 0, 'discounts': 0, 'total': 0}

    def complete_sale(self, payment_method):
        if not self._cart_items:
            self.error_occurred.emit("Der Warenkorb ist leer")
            return

        try:
            # Berechne Gesamtbetrag
            total = sum(item.product.price * item.quantity for item in self._cart_items)

            # Erstelle einen neuen Verkauf
            sale = Sale(
                total_amount=total,
                payment_method=payment_method,
                payment_status="paid",
                date=datetime.now()
            )

            # Füge Verkaufsposten hinzu
            for item in self._cart_items:
                sale_item = SaleItem(
                    product_id=item.product.id,
                    quantity=item.quantity,
                    price=item.product.price,
                    discount=0,
                    sale=sale
                )
                sale.items.append(sale_item)

                # Aktualisiere den Lagerbestand
                if item.product.inventory:
                    item.product.inventory.quantity -= item.quantity

            # Speichere den Verkauf in der Datenbank
            with SessionLocal() as db:
                db.add(sale)
                db.commit()

            # Leere den Warenkorb
            self._cart_items.clear()
            self.cart_updated.emit()
            self.sale_completed.emit(sale.id)

            return True

        except Exception as e:
            self.error_occurred.emit(str(e))
            return False

    def __del__(self):
        self.db.close()


class CartItem:
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity
        self.discount = 0  # Rabatt in Prozent

from PySide6.QtCore import QSettings

class SettingsService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.settings = QSettings("Codeium", "POS")
        
    def get_currency(self):
        """Gibt den aktuellen Währungscode zurück"""
        return self.settings.value("currency", "CHF")
    
    def set_currency(self, currency_code):
        """Setzt den Währungscode"""
        self.settings.setValue("currency", currency_code)
        self.settings.sync()
    
    def get_currency_symbol(self):
        """Gibt das Währungssymbol für die aktuelle Währung zurück"""
        currency_symbols = {
            "CHF": "CHF",
            "EUR": "€",
            "USD": "$",
            "GBP": "£",
            "JPY": "¥",
            "CNY": "¥",
            "AUD": "A$",
            "CAD": "C$",
            "SEK": "kr",
            "NOK": "kr",
            "DKK": "kr"
        }
        return currency_symbols.get(self.get_currency(), self.get_currency())
    
    def format_currency(self, amount):
        """Formatiert einen Betrag mit der aktuellen Währung"""
        currency = self.get_currency()
        symbol = self.get_currency_symbol()
        
        if currency in ["JPY", "CNY"]:  # Währungen ohne Dezimalstellen
            return f"{symbol} {int(amount):,}"
        elif currency in ["SEK", "NOK", "DKK"]:  # Skandinavische Währungen
            return f"{amount:.2f} {symbol}"
        else:  # Standardformat
            return f"{symbol} {amount:.2f}"

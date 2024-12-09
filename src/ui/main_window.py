from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QMessageBox, QDialog,
    QApplication, QFrame
)
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QIcon, QScreen
from src.ui.views.pos_view import POSView
from src.ui.views.inventory_view import InventoryView
from src.ui.views.customers_view import CustomersView
from src.ui.views.reports_view import ReportsView
from src.ui.dialogs.login_dialog import LoginDialog
from src.ui.dialogs.settings_dialog import SettingsDialog
from src.ui.widgets.title_bar import TitleBar
from src.services.auth_service import AuthService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        
        # Remove window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Set size and position
        self.resize(1200, 800)
        self.center_on_screen()
        
        # Show login dialog
        if not self.show_login():
            import sys
            sys.exit(0)
            
        self.init_ui()
        self.load_stylesheet()
        self.showMaximized()
        
    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    def load_stylesheet(self):
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        style_file = QFile(os.path.join(current_dir, "styles", "style.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            self.setStyleSheet(stream.readAll())
            style_file.close()
            
    def show_login(self):
        # Debug-Modus: Login überspringen
        debug_mode = True  # Setze auf False für normalen Betrieb
        
        if debug_mode:
            # Debug-User erstellen
            from src.models.user import User
            self.current_user = User(
                username="admin",
                role="admin",
                id=1
            )
            return True
            
        # Normaler Login-Dialog
        dialog = LoginDialog(self)
        if dialog.exec_():
            self.current_user = dialog.get_user()
            return True
        return False
        
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add custom title bar
        self.title_bar = TitleBar(self)
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.closeClicked.connect(self.close)
        main_layout.addWidget(self.title_bar)
        
        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create sidebar
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # User info
        user_info = QLabel(f"Benutzer: {self.current_user.username}")
        user_info.setStyleSheet("color: white; padding: 20px;")
        sidebar_layout.addWidget(user_info)
        
        # Navigation buttons
        nav_button_style = """
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                padding: 8px;
                min-height: 30px;
                border-radius: 4px;
                margin: 2px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
            QPushButton:checked {
                background-color: #455A64;
                font-weight: bold;
            }
        """
        
        self.pos_btn = QPushButton("🛒 Kasse")
        self.pos_btn.setCheckable(True)
        self.pos_btn.setChecked(True)
        self.pos_btn.clicked.connect(lambda: self.change_view(0, self.pos_btn))
        self.pos_btn.setStyleSheet(nav_button_style)
        
        self.inventory_btn = QPushButton("📦 Lager")
        self.inventory_btn.setCheckable(True)
        self.inventory_btn.clicked.connect(lambda: self.change_view(1, self.inventory_btn))
        self.inventory_btn.setStyleSheet(nav_button_style)
        
        self.customers_btn = QPushButton("👥 Kunden")
        self.customers_btn.setCheckable(True)
        self.customers_btn.clicked.connect(lambda: self.change_view(2, self.customers_btn))
        self.customers_btn.setStyleSheet(nav_button_style)
        
        self.reports_btn = QPushButton("📊 Berichte")
        self.reports_btn.setCheckable(True)
        self.reports_btn.clicked.connect(lambda: self.change_view(3, self.reports_btn))
        self.reports_btn.setStyleSheet(nav_button_style)
        
        # Settings button
        self.settings_btn = QPushButton("⚙ Einstellungen")
        self.settings_btn.clicked.connect(self.show_settings)
        self.settings_btn.setStyleSheet(nav_button_style)
        
        # Logout at bottom
        self.logout_btn = QPushButton("🚪 Abmelden")
        self.logout_btn.clicked.connect(self.handle_logout)
        self.logout_btn.setStyleSheet(nav_button_style)
        
        # Add buttons to sidebar
        sidebar_layout.addWidget(self.pos_btn)
        if self.current_user.role in ["admin", "manager"]:
            sidebar_layout.addWidget(self.inventory_btn)
            sidebar_layout.addWidget(self.customers_btn)
            sidebar_layout.addWidget(self.reports_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addWidget(self.logout_btn)
        
        # Create content area
        content_widget = QWidget()
        content_widget.setObjectName("contentArea")
        content_layout.addWidget(sidebar)
        content_layout.addWidget(content_widget)
        
        # Create stacked widget for different views
        self.stack = QStackedWidget(content_widget)
        content_widget_layout = QVBoxLayout(content_widget)
        content_widget_layout.setContentsMargins(10, 10, 10, 10)
        content_widget_layout.addWidget(self.stack)
        
        # Initialize views
        self.pos_view = POSView()
        self.inventory_view = InventoryView()
        self.customers_view = CustomersView()
        self.reports_view = ReportsView()
        
        # Set current user for POS view
        self.pos_view.controller.set_current_user(self.current_user.id)
        
        # Add views to stack
        self.stack.addWidget(self.pos_view)
        self.stack.addWidget(self.inventory_view)
        self.stack.addWidget(self.customers_view)
        self.stack.addWidget(self.reports_view)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        
    def change_view(self, index: int, button: QPushButton):
        # Uncheck all buttons
        for btn in [self.pos_btn, self.inventory_btn, self.customers_btn, self.reports_btn]:
            btn.setChecked(False)
        # Check the clicked button and change view
        button.setChecked(True)
        self.stack.setCurrentIndex(index)
        
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.title_bar.max_button.setText("🗖")
        else:
            self.showMaximized()
            self.title_bar.max_button.setText("🗗")
        
    def handle_logout(self):
        reply = QMessageBox.question(
            self, 'Abmelden',
            'Möchten Sie sich wirklich abmelden?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()
            # Restart application
            import sys
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Aktualisiere die Anzeige nach Änderungen
            self.pos_view.controller.settings_updated.emit()
            # Aktualisiere auch die Lageransicht
            self.inventory_view.update_display()

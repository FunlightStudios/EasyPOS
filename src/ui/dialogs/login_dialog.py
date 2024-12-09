from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QWidget
)
from PySide6.QtCore import Qt
from src.services.auth_service import AuthService

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 0, 10, 0)
        
        title = QLabel("Anmeldung")
        title.setObjectName("titleLabel")
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.reject)
        
        title_bar_layout.addWidget(title)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_btn)
        
        # Content
        content = QWidget()
        content.setObjectName("loginContent")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(40, 40, 40, 40)
        
        # Welcome message
        welcome = QLabel("Willkommen im POS System")
        welcome.setObjectName("welcomeLabel")
        welcome.setAlignment(Qt.AlignCenter)
        
        # Username
        username_layout = QVBoxLayout()
        username_label = QLabel("Benutzername")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername eingeben")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password
        password_layout = QVBoxLayout()
        password_label = QLabel("Passwort")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Passwort eingeben")
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Anmelden")
        login_btn.setObjectName("loginButton")
        login_btn.clicked.connect(self.handle_login)
        
        # Add widgets to content layout
        content_layout.addWidget(welcome)
        content_layout.addLayout(username_layout)
        content_layout.addLayout(password_layout)
        content_layout.addWidget(login_btn)
        content_layout.addStretch()
        
        # Add widgets to main layout
        layout.addWidget(title_bar)
        layout.addWidget(content)
        
        # Set focus to username input
        self.username_input.setFocus()
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte geben Sie Benutzername und Passwort ein."
            )
            return
            
        auth_service = AuthService()
        user = auth_service.authenticate_user(username, password)
        
        if user:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Fehler",
                "Ungültiger Benutzername oder Passwort."
            )
            
    def get_user(self):
        return self.user
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

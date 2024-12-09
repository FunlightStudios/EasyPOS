from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class TitleBar(QWidget):
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    closeClicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.pressing = False
        self.start_pos = None
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        self.title_label = QLabel("POS System")
        self.title_label.setObjectName("titleLabel")
        
        # Window controls
        min_button = QPushButton("🗕")
        min_button.setObjectName("minButton")
        min_button.clicked.connect(self.minimizeClicked)
        
        self.max_button = QPushButton("🗖")
        self.max_button.setObjectName("maxButton")
        self.max_button.clicked.connect(self.maximizeClicked)
        
        close_button = QPushButton("✕")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.closeClicked)
        
        # Add widgets to layout
        layout.addSpacing(10)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(min_button)
        layout.addWidget(self.max_button)
        layout.addWidget(close_button)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start_pos = event.globalPosition().toPoint()
            
    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.window().isMaximized():
                self.window().showNormal()
                # Adjust the start position to maintain relative cursor position
                screen_ratio = event.globalPosition().toPoint().x() / self.window().width()
                new_x = int(self.window().width() * screen_ratio)
                self.start_pos = event.globalPosition().toPoint() - self.mapToGlobal(self.pos()) + self.pos()
                self.start_pos.setX(new_x)
            
            end_pos = event.globalPosition().toPoint()
            movement = end_pos - self.start_pos
            self.window().move(self.window().pos() + movement)
            self.start_pos = end_pos
            
    def mouseReleaseEvent(self, event):
        self.pressing = False
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.window().isMaximized():
                self.window().showNormal()
                self.max_button.setText("🗖")
            else:
                self.window().showMaximized()
                self.max_button.setText("🗗")

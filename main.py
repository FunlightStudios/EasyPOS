#!/usr/bin/env python3
import sys
from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from pathlib import Path
import os
from dotenv import load_dotenv
from src.database.database import init_db

def main():
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Set High DPI attributes before creating QApplication
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Initialize database
    init_db()
    
    # Set application info
    app.setApplicationName("ModernPOS")
    app.setOrganizationName("Codeium")
    app.setOrganizationDomain("codeium.com")
    
    # Load and set stylesheet
    style_file = Path(__file__).parent / "src" / "ui" / "styles" / "dark_theme.qss"
    if style_file.exists():
        try:
            with open(style_file, "r", encoding='utf-8') as f:
                style = f.read()
                app.setStyleSheet(style)
                print("Stylesheet loaded successfully")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
    else:
        print(f"Stylesheet file not found: {style_file}")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

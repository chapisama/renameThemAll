try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
except ImportError:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton

from renameThemAll.constants import ABOUT_TEXT

class AboutDialog(QDialog):
    """
    Dialog window displaying the 'About' information.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedWidth(600)
        self.setMinimumHeight(600)
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        text_browser = QTextBrowser()
        text_browser.setReadOnly(True)
        text_browser.setMinimumWidth(400)
        text_browser.setOpenExternalLinks(True)
        
        try:
            with open(ABOUT_TEXT, 'r', encoding='utf-8') as file:
                content = file.read()
                text_browser.setMarkdown(content)
        except Exception as e:
            text_browser.setText(f"Error reading file: {str(e)}")
            
        layout.addWidget(text_browser)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

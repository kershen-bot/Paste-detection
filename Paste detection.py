# =========================
# Import's & From's
# =========================
import pyautogui  # type: ignore
import time
import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QWidget, QCheckBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor

# =========================
# CONFIGURATION OF VARIABLES
# =========================
BASE_DELAY = 0.07
VARIANCE = 0.04
THINK_CHANCE = 0.05
TYPO_CHANCE = 0.03
LETTER ="abcdefghijklmnopqrstuvwxyz"
CAPITAL_LETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER = "1234567890"
#Typo printed to comand line for testing purposes
TYPO = random.choice(LETTER +LETTER + CAPITAL_LETTER + NUMBER)
print(random.choice(LETTER +LETTER + CAPITAL_LETTER + NUMBER))

# =========================
# TYPING WORKER THREAD
# =========================
class TypingThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, text, enable_typos):
        super().__init__()
        self.text = text
        self.enable_typos = enable_typos
    
    def run(self):
        human_typing(self.text, self.enable_typos)
        self.finished.emit()

# =========================
# CORE FUNCTION
# =========================
def human_typing(text, enable_typos=True):
    time.sleep(2)
    for char in text:
        try:
            if enable_typos and random.random() < TYPO_CHANCE and char.isalpha():
                typo = random.choice(TYPO)
                pyautogui.write(typo)
                time.sleep(0.1)
                pyautogui.press('backspace')

            pyautogui.write(char)
 
            delay = random.uniform(BASE_DELAY - VARIANCE, BASE_DELAY + VARIANCE)
            time.sleep(max(0.01, delay))

            if random.random() < THINK_CHANCE:
                time.sleep(random.uniform(0.3, 1.0))

        except KeyboardInterrupt:
            print("\nTyping interrupted by user.")
            sys.exit(0)

# =========================
# MAIN WINDOW CREATION
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.typing_thread = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Paste detection")
        self.setGeometry(100, 100, 500, 350)

        pixmap = QPixmap(48, 48)
        pixmap.fill(QColor("#D94ABC"))
        self.setWindowIcon(QIcon(pixmap))
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Enter text to type")
        layout.addWidget(label)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter the text you want to type")
        layout.addWidget(self.text_input)
        
        self.typo_checkbox = QCheckBox("Enable Typos")
        self.typo_checkbox.setChecked(True)
        layout.addWidget(self.typo_checkbox)
        
        self.start_button = QPushButton("Start Typing")
        self.start_button.clicked.connect(self.start_typing)
        layout.addWidget(self.start_button)
        print("Start Typing")
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        print("Ready")
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def start_typing(self):
        text = self.text_input.text()
        
        if not text:
            self.status_label.setText("ERROR:Enter some text")
            print("Error")
            print("Error")
            return
        
        self.start_button.setEnabled(False)
        self.typo_checkbox.setEnabled(False)
        self.status_label.setText("Starting in 5 seconds switch to your typing document window")
        
        enable_typos = self.typo_checkbox.isChecked()
        
        self.typing_thread = TypingThread(text, enable_typos)
        self.typing_thread.finished.connect(self.on_typing_finished)
        self.typing_thread.start()
    
    def on_typing_finished(self):
        self.start_button.setEnabled(True)
        self.typo_checkbox.setEnabled(True)
        self.status_label.setText("Typing completed")

# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pixmap = QPixmap(48, 48)
    pixmap.fill(QColor("#D94ABC"))
    app.setWindowIcon(QIcon(pixmap))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
# =========================
# Credit's
# =========================
# https://duck.ai
#Helping expand the project and make it better, also providing some of the code for the project.
# https://chatgpt.com/
# Coding the first version of the project, providing the base code and helping with the development of the project.
# https://claude.ai/
# Fixing the bugs of the project and providing some of the code for the project, also helping with the development of the project.
# https://github.com/kershen-bot
# My github profile where I post some of my projects.

print("""
Credits to:
https://duck.ai
https://chatgpt.com/
https://claude.ai/
https://github.com/kershen-bot
""")

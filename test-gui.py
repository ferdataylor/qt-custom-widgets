import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget

def test_gui():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Test GUI")
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel("GUI is working!", window)
    label.move(100, 100)
    
    window.show()
    
    # For headless testing, close immediately
    window.close()
    print("GUI test completed successfully!")

if __name__ == "__main__":
    test_gui()
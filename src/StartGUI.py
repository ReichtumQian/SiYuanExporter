import sys
from ExportWindow import SiYuanExportWindow
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog

app = QApplication(sys.argv)
window = SiYuanExportWindow()
window.show()
sys.exit(app.exec_())

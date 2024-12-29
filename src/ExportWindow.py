
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog
from SiYuanExporter import *

class SiYuanExportWindow(QWidget):
  def __init__(self, json_file = "config.json"):
    super().__init__()
    super().setWindowTitle('SiYuan Exporter')
    self._layout = QVBoxLayout()
    self._exporter = SiYuanExporter(json_file)
    self._set_notebook_selection(*self._exporter.list_notebook())
    self._set_export_path()
    self._set_export_button()

  def show(self, w = 400, h = 300):
    super().setLayout(self._layout)
    super().resize(w, h)
    super().show()
  
  def _set_notebook_selection(self, notebook_ids, notebook_names):
    notebook_label = QLabel("Select Notebook:")
    self._layout.addWidget(notebook_label)
    notebook_combo = QComboBox()
    for i in range(len(notebook_ids)):
      notebook_combo.addItem(notebook_names[i])
    self._layout.addWidget(notebook_combo)
    self._notebook_id = notebook_ids[0]
    self._notebook_name = notebook_names[0]
    def on_notebook_changed(value):
      self._notebook_id = notebook_ids[value]
      self._notebook_name = notebook_names[value]
    notebook_combo.currentIndexChanged.connect(on_notebook_changed)
  
  def _set_export_path(self):
    path_label = QLabel("Selected Path: ")
    self._layout.addWidget(path_label)
    def on_directory_button_clicked():
      directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
      if directory_path:
        path_label.setText(f"Selected Path: {directory_path}")
        self._directory_path = directory_path
    directory_button = QPushButton("Select Directory")
    directory_button.clicked.connect(on_directory_button_clicked)
    self._layout.addWidget(directory_button)
  
  def _set_export_button(self):
    export_button = QPushButton("Export Notebook Markdown Zip")
    def export_notebook_markdown_zip():
      self._exporter.export_notebook_markdown_zip(self._notebook_id, f"{self._notebook_name}.zip", self._directory_path)
    export_button.clicked.connect(export_notebook_markdown_zip)
    self._layout.addWidget(export_button)






if __name__ == '__main__':
  app = QApplication(sys.argv) 
  window = SiYuanExportWindow()
  window.show()
  sys.exit(app.exec_())
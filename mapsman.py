import sys
from PySide6 import QtWidgets
from widgets.main import MainWidget

if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  widget = MainWidget()
  widget.show()
  sys.exit(app.exec())

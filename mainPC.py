import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QMessageBox
from utils import clone


class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(400, 400, 350, 50)
        self.setWindowTitle("Download addon")
        self.downloaded = False
        self.button = QPushButton("Download", self)
        self.button.resize(330, 30)
        self.button.move(10, 10)
        self.button.clicked.connect(self.download)

    def download(self):
        global app
        path = QFileDialog.getExistingDirectory()
        if path:
            clone("https://github.com/Ryorama/TerrariaCraft-Bedrock", path)
            ok = QMessageBox.information(self, "Success", "Addon was successfully downloaded")
            if ok:
                app.exit(0)
        else:
            ok = QMessageBox.critical(self, "Error", "Download was canceled by user")
            if ok:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Downloader()
    sys.exit(app.exec())

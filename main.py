import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFileDialog, QLineEdit, QProgressBar, QComboBox, QMessageBox
from PyQt5.QtWidgets import *
from tqdm import tqdm
import requests


class DownloadManagerApp(QMainWindow):
    def __init__(self, parent=None):
        super(DownloadManagerApp, self).__init__(parent)
        QMainWindow.__init__(self)

        uic.loadUi("dm.ui", self)

        # Define our widgets

        self.label_title = self.findChild(QLabel, "label")
        self.label = self.findChild(QLabel, "label_2")
        self.downloadButton = self.findChild(QPushButton, "downloadButton")
        self.locationButton = self.findChild(QPushButton, "locationButton")
        self.url_lineEdit = self.findChild(QLineEdit, "url_lineEdit")
        self.location_lineEdit = self.findChild(QLineEdit, "location_lineEdit")
        self.progressBar = self.findChild(QProgressBar, "progressBar")
        self.quality_comboBox = self.findChild(QComboBox, "comboBox")

        self.quality_comboBox.addItem("Low")
        self.quality_comboBox.addItem("Medium")
        self.quality_comboBox.addItem("High")

        self.downloadButton.clicked.connect(self.download)
        self.locationButton.clicked.connect(self.handel_browse)

    def handel_browse(self):
        save_location, _ = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.location_lineEdit.setText(save_location)

    def download(self):
        print("start downloading")
        download_url = self.url_lineEdit.text()
        save_location = self.location_lineEdit.text()
        quality = self.quality_comboBox.currentText()

        if download_url == "" or save_location == "":
            QMessageBox.warning(self, "Data Error", "Please provide a valid URL and save location.")
            return

        try:
            response = requests.get(download_url, stream=True)

            save_path = save_location
            total_size = int(response.headers['content-length'])
            chunk_size = 1024

            with open(save_path, "wb") as file:
                for chunk in tqdm(iterable=response.iter_content(chunk_size=chunk_size), total=total_size/chunk_size, unit='kb'):
                    file.write(chunk)
                    self.handel_progress(file.tell(), chunk_size, total_size)
            self.progressBar.setValue(100)
            QMessageBox.information(self, "Download Completed", "Download completed successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Download Error", f"Download failed. Error: {str(e)}")

        self.url_lineEdit.setText("")
        self.location_lineEdit.setText("")
        self.progressBar.setValue(0)

    def handel_progress(self, blocknum, blocksize, totalsize):

        if totalsize > 0:
            download_percentage = blocknum * blocksize * 100 / totalsize
            self.progressBar.setValue(int(download_percentage))
            QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dm_app = DownloadManagerApp()
    dm_app.show()
    app.exec_()

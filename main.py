import os
import re
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QMessageBox
from urllib.error import URLError
from urllib.request import *

headers = {
    'User-Agent':
    r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    r'Chrome/72.0.3626.109 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'identity',
}


def clone(git_url, path=os.getcwd(), branch_name='master'):
    git_url = git_url.replace(' ', '')
    if git_url[-1] == '/':
        git_url = git_url[:-1]
    elif git_url[-4:] == '.git':
        git_url = git_url[:-4]
    username, projectname = re.match('https://github.com/(.+)/(.+)',
                                     git_url).groups()[0:2]
    url = 'https://codeload.github.com/{}/{}/zip/{}'.format(
        username, projectname, branch_name)
    filename = path + '/' + projectname
    zipfile_name = filename + '.mcaddon'
    try:
        urlretrieve(url, zipfile_name, reporthook=report_hook)
    except URLError:
        headers['Host'] = 'github.com'
        request = Request(
            'https://github.com/{}/{}'.format(username, projectname),
            headers=headers)
        response = urlopen(request)

        pattern = '/{}/{}/tree/(.*?)/'.format(username, projectname)
        b_name = re.findall(pattern, str(response.read()))[-1]
        return clone(git_url, path, b_name)


def report_hook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return

    duration = time.time() - start_time + 0.000001
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    if 100 >= percent >= 0:
        sys.stdout.write("\r{} %, {} KB, {} KB/s, {} seconds passed         ".format(
            percent, progress_size / 1024, speed, round(duration, 2)))
    else:
        sys.stdout.write("\r{} KB, {} KB/s, {} seconds passed         ".format(
            progress_size / 1024, speed, round(duration, 2)))
    sys.stdout.flush()


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
            ok = QMessageBox.critical(self, "Error", "Skipped downloading")
            if ok:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Downloader()
    sys.exit(app.exec())

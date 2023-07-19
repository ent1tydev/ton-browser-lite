import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from threading import Thread
from os import popen
from time import sleep

proxy_start_command = ".\\rldp-http-proxy.exe -p 40888 -c 30333 -C global.config.json"
history_file = "history.txt"

def start_proxy():
    if "rldp-http-proxy.exe" not in str(popen('tasklist').read()):
        popen(proxy_start_command)


class Browser(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lite TON Browser by LazyRiver")
        self.setWindowIcon(QIcon('icon.ico'))

        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.HttpProxy)
        proxy.setHostName("127.0.0.1")
        proxy.setPort(40888)
        QNetworkProxy.setApplicationProxy(proxy)

        search_line = QLineEdit()
        back_button = QPushButton("◀️")
        reload_button = QPushButton("🔄")
        search_button = QPushButton("🔎")
        history_button = QPushButton("📂")

        self.browser = QWebEngineView()
        self.history_dialog = HistoryDialog()

        search_layout = QHBoxLayout()
        search_layout.addWidget(history_button)
        search_layout.addWidget(back_button)
        search_layout.addWidget(reload_button)
        search_layout.addWidget(search_line)
        search_layout.addWidget(search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.browser)

        self.setLayout(main_layout)

        back_button.clicked.connect(self.browser.back)
        reload_button.clicked.connect(self.browser.reload)
        self.browser.urlChanged.connect(lambda url: search_line.setText(url.toString()))

        self.browser.load(QUrl('http://searching.ton'))

        search_button.clicked.connect(lambda: self.search(search_line.text()))
        search_line.returnPressed.connect(lambda: self.search(search_line.text()))
        history_button.clicked.connect(self.show_history)

        self.history_list = []
        self.load_history_from_file()

        self.show()

    def search(self, query):
        if not query.startswith('http://') and not query.startswith('https://'):
            query = 'http://' + query
        self.browser.load(QUrl(query))
        self.history_list.append(query)
        self.save_history_to_file()

    def show_history(self):
        self.history_dialog.set_history(self.history_list)
        self.history_dialog.exec_()

    def load_history_from_file(self):
        try:
            with open(history_file, 'r') as file:
                self.history_list = file.read().splitlines()
        except FileNotFoundError:
            self.history_list = []

    def save_history_to_file(self):
        with open(history_file, 'w') as file:
            file.write('\n'.join(self.history_list))


class HistoryDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("History")
        self.setWindowIcon(QIcon('icon.ico'))

        self.history_text_edit = QTextEdit()
        self.history_text_edit.setReadOnly(True)
        self.history_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout = QVBoxLayout()
        layout.addWidget(self.history_text_edit)

        self.setLayout(layout)

    def set_history(self, history_list):
        history_text = '\n'.join(history_list)
        self.history_text_edit.setPlainText(history_text)


if __name__ == '__main__':
    Thread(target=start_proxy).start()
    sleep(1)
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())

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

def clean_history():
    popen('.\phep.exe flush')

def stop_proxy():
    popen('.\phep.exe stop')

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
        back_button = QPushButton("Back")
        reload_button = QPushButton("Reload")
        search_button = QPushButton("Search")
        history_button = QPushButton("History")

        # Set rounded style with border color for input field and buttons
        style = '''
            border-radius: 15px;
            border: 2px groove #6565FF;
            padding: 8px;
        '''
        search_line.setStyleSheet(f'QLineEdit {{{style}}}')
        back_button.setStyleSheet(f'''
            QPushButton {{{style}}}
            QPushButton:hover {{
                background-color: #6666FF;
            }}
        ''')
        reload_button.setStyleSheet(f'''
            QPushButton {{{style}}}
            QPushButton:hover {{
                background-color: #6666FF;
            }}
        ''')
        search_button.setStyleSheet(f'''
            QPushButton {{{style}}}
            QPushButton:hover {{
                background-color: #6666FF;
            }}
        ''')
        history_button.setStyleSheet(f'''
            QPushButton {{{style}}}
            QPushButton:hover {{
                background-color: #6666FF;
            }}
        ''')

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

        clean_button = QPushButton("Clean History")
        stop_button = QPushButton("Stop Proxy")
        start_button = QPushButton("Start Proxy")

        layout = QVBoxLayout()
        layout.addWidget(self.history_text_edit)
        layout.addWidget(clean_button)
        layout.addWidget(stop_button)
        layout.addWidget(start_button)

        self.setLayout(layout)

        clean_button.clicked.connect(self.clean_history_and_close)
        stop_button.clicked.connect(self.stop_proxy_and_close)
        start_button.clicked.connect(self.start_proxy_in_thread)

    def set_history(self, history_list):
        history_text = '\n'.join(history_list)
        self.history_text_edit.setPlainText(history_text)

    def clean_history_and_close(self):
        Thread(target=clean_history).start()
        self.accept()

    def stop_proxy_and_close(self):
        Thread(target=stop_proxy).start()
        self.accept()

    def start_proxy_in_thread(self):
        Thread(target=start_proxy).start()
        self.accept()


if __name__ == '__main__':
    Thread(target=start_proxy).start()
    sleep(1)
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())

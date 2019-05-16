import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication, QSplitter, QTextEdit
from PyQt5 import QtCore
import threading

from chat_client_class import *

class Form(QDialog):

    def __init__(self):
        super().__init__()
        self.clientthread = clientthread()
        self.read_system_display = threading.Thread(target=self.read_system_display)
        self.read_peer = threading.Thread(target = self.read_peer_msg)
        self.read_me = threading.Thread(target = self.read_my_msg)
        self.read_me.daemon = True
        self.read_peer.daemon = True
        self.read_system_display.daemon = True
        # Create widgets
        self.TextField = QLineEdit("")

        self.TextField.resize(400, 400)
        self.button = QPushButton("Send")
        # Create layout and add widgets
        layout = QVBoxLayout()
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.chat)
        splitter.addWidget(self.TextField)
        splitter.setSizes([500, 200])
        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.button)
        splitter2.setSizes([480, 10])
        layout.addWidget(splitter2)
        self.setWindowTitle('BlackJack')
        # Set dialog layout
        self.setLayout(layout)
        self.resize(500, 500)
        for line in menu.split('\n'):
            self.chat.append('{:^90}'.format(line))
        # Add button signal to greetings slot
        print(type(self.clientthread.client.args))
        self.button.clicked.connect(self.send)
        self.init()



    # Greets the user
    def send(self):
        #print(self.TextField.text())
        text = self.TextField.text()
        if self.clientthread.client.state == S_OFFLINE:
            if " " in text:
              pass
            else:
              text += " where is your password??????"
        self.clientthread.client.text0 = text
        text3 = text[:]
        if "register" in text:
            text1 = text3.split()
            text = "Username: " + text1[1] + "\n" + "Password: " + "*" * len(text1[1])
        elif self.clientthread.client.state == S_OFFLINE:
            text1 = text3.split()
            text = "Username: " + text1[0] + "\n" + "Password: " + "*" * len(text1[1])
        self.chat.append(text)
        self.TextField.setText('')

    def init(self):
        self.show()
        self.clientthread.start()
        self.read_system_display.start()
        self.read_peer.start()
        self.read_me.start()

    def read_system_display(self):
        while 1:
              if self.clientthread.client.sm.system_display != '':
                   self.chat.append(self.clientthread.client.sm.system_display)
                   self.clientthread.client.sm.system_display = ''
    def read_peer_msg(self):
        while 1:
            if self.clientthread.client.sm.peer_to_me != '':
                l =  '{:>' + str(122 - len(self.clientthread.client.sm.peer_to_me)) + '}'

                self.chat.append(l.format(self.clientthread.client.sm.peer_to_me))

                self.clientthread.client.sm.peer_to_me = ''
    def read_my_msg(self):
        pass
        while 1:
            if self.clientthread.client.sm.me_to_peer != '':
                self.chat.append(self.clientthread.client.sm.me_to_peer)
                self.clientthread.client.sm.me_to_peer = ''




class clientthread(threading.Thread):
    def __init__(self):
        super().__init__()
        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()
        self.client = Client(args)


    def run(self):

        self.client.run_chat()



if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()


    # Run the main Qt loop
    sys.exit(app.exec_())

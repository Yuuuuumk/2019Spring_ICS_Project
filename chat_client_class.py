import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm # import client_state_machine_student as csm
import threading





class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        self.to_GUI = ''
        self.text0 = ''
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        
        
    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()

        
    

        
    
    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        
        if len(my_msg) > 0:
          print(my_msg)
          if "register" in my_msg:
            my_msg = my_msg.split(" ")
            msg = json.dumps({"action":"register", "name":my_msg[1], "password":my_msg[2]})
            print(msg)
            self.send(msg)
            response = json.loads(self.recv())
            print(response)
            if response["status"] == 'register_success':
                  self.system_msg += 'registeration successful, please login in'
                  self.sm.system_display = 'registeration successful, please login in'
            return False
          else:
            my_msg = my_msg.split(" ")
            self.name = my_msg[0]
            self.password = my_msg[1]
            msg = json.dumps({"action":"login", "name":self.name, "password":self.password})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'user login elsewhere, please contact administer if it is not your action.'
                self.sm.system_display = 'user login elsewhere, please contact administer if it is not your action.'
                return False
            elif response["status"] == 'wrong_password':
                self.system_msg += 'wrong_password, please try again'
                self.sm.system_display = 'wrong_password, please try again'
                return False
            elif response["status"] == 'user_nonexist':
                self.system_msg += 'username does not exist, please register'
                self.sm.system_display = 'username does not exist, please register'
                return False

        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            #text = sys.stdin.readline()[:-1]
            if self.text0 != '':
                self.console_input.append(self.text0) # no need for lock, append is thread safe
                self.text0 = ''



    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.sm.system_display = 'Welcome to ICS chat\n' + 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.sm.system_display = 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        msg = self.sm.proc(my_msg, peer_msg)
        
        self.system_msg += msg
        





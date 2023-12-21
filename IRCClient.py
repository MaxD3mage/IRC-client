import socket
import time


class IRCClient:
    def __init__(self, server, port, nickname):
        self.server = server
        self.port = port
        self.nickname = nickname

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channels = []

    def connect(self):
        self.sock.connect((self.server, self.port))
        self.auth()

    def join_channel(self, name_channel):
        self.send_data('JOIN', name_channel)

    def auth(self):
        time.sleep(1)
        self.send_data('NICK', self.nickname)
        time.sleep(1)
        self.send_data('USER', f"{self.nickname} 0 * :{self.nickname}")

    def send_message(self, message, channel):
        message_chunks = [message[i:i + 400] for i in
                          range(0, len(message), 400)]

        for chunk in message_chunks:
            self.send_data('PRIVMSG', f"{channel} :{chunk}")

    def receive_message(self):
        try:
            data = self.sock.recv(2048).decode('utf-8', errors='ignore')
            if data.startswith('PING'):
                ping_message = data.split('PING :')[1]
                self.send_data('PONG', ping_message)
            elif data.startswith('ERROR'):
                self.sock.close()
            return data
        except ConnectionAbortedError:
            pass

    def send_data(self, command, message=''):
        if message:
            full_message = f"{command} {message}\r\n"
        else:
            full_message = f"{command}\n"
        self.sock.send(full_message.encode('utf-8'))

    def disconnect(self, message=""):
        self.send_data('QUIT', f":{message}")
        self.sock.close()

    def get_channels(self):
        self.send_data('LIST')

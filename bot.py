import socket
import re
from threading import Thread

from config import HOST, PORT, PASS, NICK, COMMANDS


class Chat():
    '''
    Abstract class to work with twitch chat by irc protocol.

    Args:
        channel: str - twitch channel bot sould connect to
    '''
    def __init__(self, channel: str):
        self._channel = channel
        self._soc = socket.socket()

        self._chat_message = re.compile(
            r':(?P<name>\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(?P<message>.*)'
        )

        self._run()


    def send_message(self, message):
        '''
        send message to chat
        '''
        self._soc.send(f"PRIVMSG #{self._channel} :{message}\r\n".encode("utf-8"))

    def on_message(self, author, message):
        '''
        messages handler
        '''
        raise NotImplementedError()


    def _handler(self):
        while 1:
            resp = self._soc.recv(4096).decode("utf-8")
            if resp.startswith('PING :tmi.twitch.tv'):
                self._soc.send('PONG\r\n'.encode('utf-8'))
                continue
            re_result = self._chat_message.search(resp)
            if re_result is not None:
                self.on_message(re_result.group('name'), re_result.group('message').replace('\n', '').replace('\r', ''))

    def _run(self):
        self._soc.connect((HOST, PORT))
        self._soc.send(f'PASS {PASS}\r\n'.encode('utf-8'))
        self._soc.send(f'NICK {NICK}\r\n'.encode('utf-8'))
        self._soc.send(f'JOIN #{self._channel}\r\n'.encode('utf-8'))

        self.thread = Thread(target=self._handler)
        self.thread.start()


class Bot(Chat):
    def on_message(self, author, message):
        for command in COMMANDS:
            if re.search(command, message, flags=re.IGNORECASE|re.MULTILINE|re.UNICODE) is not None:
                response = COMMANDS[command].format(user=author)
                self.send_message(response)


def main():
    channel = input('channel: ')
    Bot(channel)


if __name__ == "__main__":
    main()

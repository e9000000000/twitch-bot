import time
import socket
import re
import os
import requests
import bs4

from threading import Thread

TWITCH = "irc.twitch.tv"
PORT = 6667
PASS = "" #irc token
NICK = "" #twitch nickname

class Chat():
    def __init__(self, channel, print_func):
        """print_func need to recive username and message args and print message"""
        self.__channel = channel
        self.__print_function = print_func
        self.__is_answers_started = False

        self.__chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

        self.__soc = socket.socket()
        self.__soc.connect((TWITCH, PORT))
        self.__soc.send(f"PASS {PASS}\r\n".encode("utf-8"))
        self.__soc.send(f"NICK {NICK}\r\n".encode("utf-8"))
        self.__soc.send(f"JOIN #{channel}\r\n".encode("utf-8"))

        self.thread = Thread(target=self.__active)
        self.thread.start()

    def send_message(self, message):
        self.__soc.send(f"PRIVMSG #{self.__channel} :{message}\r\n".encode("utf-8"))

    def __answers(self, message:str, username):
        lmes = message.lower()

        if "слава украине" in lmes:
            self.send_message("героям слава")
        elif "glory to ukraine" in lmes:
            self.send_message("glory to heroes")
        elif "botping\r\n" == lmes:
            self.send_message("botpong")
        elif "алло" in lmes:
            self.send_message(f"че аллокаешь @{username}")
        elif NICK in lmes:
            self.send_message(f"не разговаривай с ботом или про бота @{username}")
        elif "glory to ukraine" in lmes:
            self.send_message("glory to heroes")
        elif "украине\r\n" == lmes:
            self.send_message("СЛАВА")
        elif "ахмат" in lmes:
            self.send_message("ахмат сила")

    def __active(self):
        while "Ленин жив":
            responce = self.__soc.recv(4096).decode("utf-8")
            if responce == "PING :tmi.twitch.tv\r\n":
                self.__soc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                username = re.search(r"\w+", responce).group(0)
                message = self.__chat_message.sub("", responce)
                self.__print_function(username, message)
                if self.__is_answers_started:
                    self.__answers(message, username)

    def botrun(self):
        self.__is_answers_started = True

    def botstop(self):
        self.__is_answers_started = False

class StreamWatcher():
    def __init__(self, channel, print_func=print):
        self.__channel = channel
        self.chat = Chat(channel, print_func)
        self.session = requests.Session()

    def stream_time(self):
        self.session.get(f"https://www.twitch.tv/{self.__channel}/videos")
        return "00:00:00"
        

def print_message_from_chat(username, message):
     print(f"[ {username} ]")
     print(f"{message}", end="")

def clear(): 
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')


def main():
    channel = input("channel: ")
    stream = StreamWatcher(channel, print_message_from_chat)

    while "Ленин жив":
        inp = input()
        if inp == "/run":
            stream.chat.botrun()
        elif inp == "/stop":
            stream.chat.botstop()
        elif inp == "/clear":
            clear()
        elif inp == "/time":
            print("not work")
        else:
            stream.chat.send_message(inp)
    






if __name__ == "__main__":
    main()

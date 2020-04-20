import time
import socket
import re

import os
import shutil

from time import sleep
from threading import Thread

TWITCH = "irc.twitch.tv"
PORT = 6667
PASS = "" #irc token
NICK = "" #twitch nickname


class Answer():
    def __init__(self, is_need_send_message, get_answer):
        self.is_need_send_message = is_need_send_message
        self.get_answer = get_answer


class Chat():
    def __init__(self, channel, print_func):
        """print_func need to recive username and message args and print message"""
        self.__channel = channel
        self.__print_function = print_func
        self.__is_answers_started = False
        self.__answers = []

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

    def add_answer(self, answer):
        if type(answer) is Answer:
            self.__answers.append(answer)

    def __check_answers(self, message:str, username):
        lmes = message.lower()

        for answer in self.__answers:
            if answer.is_need_send_message(username, lmes):
                self.send_message(answer.get_answer(username))
                sleep(1)


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
                    self.__check_answers(message, username)

    def botrun(self):
        self.__is_answers_started = True

    def botstop(self):
        self.__is_answers_started = False


class StreamWatcher():
    def __init__(self, channel, print_func=print):
        self.__channel = channel
        self.chat = Chat(channel, print_func)
        

def print_message_from_chat(username, message):
    print(f"[ {username} ]")
    term_width = shutil.get_terminal_size().columns
    for x in range(0, len(message), term_width-4):
        print(f"    {message[x:x+term_width-4]}", end="")

def clear(): 
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')



def main():
    channel = input("channel: ")
    stream = StreamWatcher(channel, print_message_from_chat)
    stream.chat.add_answer(Answer(lambda username, message: "слава украине" in message, lambda username: "героям слава"))
    stream.chat.add_answer(Answer(lambda username, message: "ахмат" in message, lambda username: "ахмат сила"))
    stream.chat.add_answer(Answer(lambda username, message: "чечня" in message, lambda username: "чечня крута"))
    stream.chat.add_answer(Answer(lambda username, message: "алло" in message, lambda username: f"@{username}, че аллокаешь"))
    stream.chat.add_answer(Answer(lambda username, message: f"{NICK}" in message, lambda username: f"@{username}, не произноси моего имени"))
    stream.chat.add_answer(Answer(lambda username, message: "украине\r\n" == message, lambda username: "СЛАВА"))

    while "Ленин жив":
        inp = input()
        if inp == "/run":
            stream.chat.botrun()
        elif inp == "/stop":
            stream.chat.botstop()
        elif inp == "/clear":
            clear()
        elif len(inp) > 0 and inp[0] == "/":
            print("command ERROR")
        else:
            stream.chat.send_message(inp)
    






if __name__ == "__main__":
    main()

#!/bin/env python3
from textwrap import dedent
from time import time_ns
from typing import Callable
from Crypto.Util.number import long_to_bytes
from secret import flag


class MenuEntry:
    def __init__(self, description: str, callback: Callable):
        self.callback = callback
        self.description = description

    def __str__(self):
        return self.description


class Menu:
    def __init__(self, entries: list[MenuEntry]):
        self.entries = entries

    def __str__(self):
        return '\n'.join(f'{index}. {entry}' for index, entry in enumerate(self.entries, start=1))

    def show(self):
        print("What do you want to do?", self, sep='\n')

    def prompt(self):
        try:
            choice = int(input("> "))
            print(self.entries[choice - 1].callback())
        except (ValueError, IndexError) as error:
            print("Invalid choice")


class XORCryptographer:
    def __init__(self, key: bytes):
        self.key = bytes(key)

    @staticmethod
    def xor(a: bytes, b: bytes):
        a = bytes(a)
        b = bytes(b)
        return bytes(a[i % len(a)] ^ b[i] for i in range(len(b)))

    def encrypt(self, message: bytes):
        return XORCryptographer.xor(self.key, message).hex()

    def decrypt(self, message: bytes):
        return XORCryptographer.xor(self.key, message).decode()

key = 1
for _ in range(64):
    key *= time_ns()

cryptographer = XORCryptographer(long_to_bytes(key))

menu = Menu([
    MenuEntry("Encrypt a message",
              callback=lambda: cryptographer.encrypt(input("Message: ").encode())),
    MenuEntry("Encrypt flag",
              callback=lambda: cryptographer.encrypt(flag.encode()))
])

for _ in range(5):
    menu.show()
    menu.prompt()

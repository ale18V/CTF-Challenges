from Crypto.Util.number import long_to_bytes, bytes_to_long, getStrongPrime
import textwrap
import os
import secret


class NonMalleableRSA:
    def __init__(self):
        PRIMESIZE = 1024
        p, q = [getStrongPrime(PRIMESIZE) for _ in range(2)]
        p, q = max(p, q), min(p, q)
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = 2**16 + 1
        self.d = pow(self.e, -1, self.phi)
        self.obfuscator = (p + q) % (p - q)

    def encrypt(self, message: int):
        ciphertext = pow(message, self.e, self.n) ^ self.obfuscator
        return ciphertext

    def decrypt(self, ciphertext: int):
        plaintext = pow(ciphertext ^ self.obfuscator, self.d, self.n)
        return plaintext


class Menu:
    def __str__(self):
        return textwrap.dedent("""
            What do you want to do?
            1) Encrypt message
            2) Encrypt flag
            3) Decrypt message
            4) Quit
            """)

    def executeEntryOfNumber(self, entryNumber: int):
        match entryNumber:
            case 1: self.encryptMessageEntry()
            case 2: self.encryptFlagEntry()
            case 3: self.decryptMessageEntry()
            case 4: self.quitEntry()
            case _: print("Invalid choice")

    def encryptMessageEntry(self):
        print("Give me your message as an integer")
        try:
            message = abs(int(input("> ")))
            encryptedMessage = rsa.encrypt(message)
            print(encryptedMessage)
        except ValueError as e:
            print("The message must be an integer!")

    def encryptFlagEntry(self):
        encryptedFlag = rsa.encrypt(bytes_to_long(flag.encode()))
        print(encryptedFlag)

    def decryptMessageEntry(self):
        # I'm not yet so sure that
        # this implementation is not malleable
        # Better leave this not implemented...
        print("Not implemented")

    def quitEntry(self):
        exit()


rsa = NonMalleableRSA()
menu = Menu()
flag = secret.flag

if __name__ == "__main__":
    print("Welcome!")
    print(f"I can only tell you that p mod q = {rsa.p % rsa.q}")
    for _ in range(5):
        print(menu)
        try:
            choice = int(input("Choice: "))
            menu.executeEntryOfNumber(choice)
        except ValueError as e:
            continue

from typing import Callable
import secret
assert pow(secret.a_value, -1, secret.m_value)

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
        print("What do you want to do?", self, '', sep='\n')

    def prompt(self):
        print("Insert your choice")
        try:
            choice = int(input("> "))
            self.entries[choice - 1].callback()
        except (ValueError, IndexError) as error:
            print("Invalid choice")


def create_menu() -> Menu:
    def register():
        username = input("Username: ")
        password = input("Password: ")
        if db.get(username):
            print("User already registered")
            return

        token = str(lcg.next())
        db[username] = {"password": password, "token": token}
        print(f"Your password reset token is: {token}")

    def login():
        username = input("Username: ")
        password = input("Password: ")
        user = db.get(username)
        if user and user["password"] == password:
            print(f"\nWelcome {username}.")
            if username == "admin":
                print(secret.flag)
        else:
            print("Wrong credentials")

    def reset():
        username = input("Username: ")
        token = input("Token: ")
        user = db.get(username)
        if user and user["token"] == token:
            password = input("Give me the new password: ")
            user["password"] = password
        else:
            print("Wrong token or username")

    return Menu([
        MenuEntry("Register", callback=register),
        MenuEntry("Login", callback=login),
        MenuEntry("Reset password", callback=reset),
        MenuEntry("Quit", lambda: exit())
    ])


class LCG:
    # Linear Congruential Generator
    # X(n+1) = aX(n) + c mod m
    def __init__(self, seed, a, c, m):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def generate_sequence(self, length):
        sequence = []
        for _ in range(length):
            sequence.append(self.next())
        return sequence

# Example usage
lcg = LCG(
    secret.seed,
    secret.a_value,
    secret.c_value,
    secret.m_value)

db = {
    "admin": {
        "password": secret.password,
        "token": str(lcg.next())
    }
}

menu = create_menu()
print("Welcome.")
while True:
    menu.show()
    menu.prompt()

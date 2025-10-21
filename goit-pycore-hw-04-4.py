
# -----------------------------
# Консольний бот-помічник (CLI)
# -----------------------------
# Функціональність:
# - "hello"                  -> відповідає "How can I help you?"
# - "add <name> <phone>"     -> додає контакт
# - "change <name> <phone>"  -> змінює номер існуючого контакту
# - "phone <name>"           -> показує номер телефону
# - "all"                    -> показує всі контакти
# - "close" / "exit"         -> завершує роботу з повідомленням "Good bye!"
#
# Принципи:
# - Парсер команд виділяє команду та аргументи незалежно від регістру.
# - Уся взаємодія з користувачем (print/input) — лише у main().
# - Логіка команд — в окремих хендлерах (функціях), які повертають рядок-відповідь.
# -----------------------------

from typing import Tuple, List, Dict   # Підказки типів для кращої читабельності коду


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Парсер команд:
    - приймає сирий рядок від користувача;
    - прибирає зайві пробіли по краях;
    - розбиває на "команду" (перше слово) та "аргументи" (решта слів);
    - команду зводить до нижнього регістру, щоб не бути чутливим до регістру.
    Повертає кортеж: (command, args_list).
    """
    # .strip() — прибрати пробіли/табуляції/переноси на краях
    # .split() — розбити за пробілами на список слів
    parts = user_input.strip().split()

    # Якщо користувач натиснув Enter (порожній ввід) — повертаємо порожню команду
    if not parts:
        return "", []

    # Перше слово — команда; решта — аргументи
    cmd, *args = parts

    # Команду зводимо до нижнього регістру (HeLLo -> hello)
    return cmd.lower(), args


# -----------------------------
# ХЕНДЛЕРИ КОМАНД
# Кожен хендлер:
#  - приймає аргументи та словник контактів (де name -> phone)
#  - повертає текстову відповідь для друку
# -----------------------------

def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Додає новий контакт: очікує 2 аргументи (ім'я, телефон).
    Якщо формат невірний — повертає підказку з правильним використанням.
    """
    # Перевіряємо, що прийшло рівно 2 аргументи
    if len(args) != 2:
        return "Usage: add <name> <phone>"

    name, phone = args
    # Додаємо/оновлюємо запис у словнику (ім'я -> телефон)
    contacts[name] = phone
    return "Contact added."


def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Змінює номер існуючого контакту: очікує 2 аргументи (ім'я, новий телефон).
    Якщо контакту не існує — повертає повідомлення про помилку.
    """
    if len(args) != 2:
        return "Usage: change <name> <new_phone>"

    name, phone = args

    # Перевіряємо, що ім'я вже є у словнику
    if name not in contacts:
        return "Contact not found."

    # Оновлюємо номер телефону
    contacts[name] = phone
    return "Contact updated."


def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Показує номер телефону за ім'ям: очікує 1 аргумент (ім'я).
    Якщо контакту не існує — повертає повідомлення про помилку.
    """
    if len(args) != 1:
        return "Usage: phone <name>"

    name = args[0]

    # Якщо такого імені немає — інформуємо користувача
    if name not in contacts:
        return "Contact not found."

    # Повертаємо номер телефону
    return contacts[name]


def show_all(contacts: Dict[str, str]) -> str:
    """
    Виводить усі збережені контакти у форматі "name: phone".
    Якщо контактів немає — інформує користувача.
    """
    if not contacts:
        return "No contacts."

    # Перетворюємо словник на багаторядковий рядок
    # можна відсортувати
    # "\n".join(f"{name}: {phone}" for name, phone in sorted(contacts.items()))
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


# -----------------------------
# ГОЛОВНИЙ ЦИКЛ ПРОГРАМИ (CLI)
# -----------------------------
def main() -> None:
    # Сховище контактів: ключ — ім'я (str), значення — телефон (str)
    contacts: Dict[str, str] = {}

    # Привітання при старті
    print("Welcome to the assistant bot!")

    # Нескінченний цикл запит-відповідь
    while True:
        # Отримуємо рядок від користувача
        user_input = input("Enter a command: ")

        # Розбираємо на команду та аргументи
        command, args = parse_input(user_input)

        # Команди завершення роботи (незалежно від регістру, бо ми знизили його в parse_input)
        if command in ("close", "exit"):
            print("Good bye!")
            break

        # Проста відповідь-привітання
        elif command == "hello":
            print("How can I help you?")

        # Додавання контакту
        elif command == "add":
            print(add_contact(args, contacts))

        # Зміна телефону
        elif command == "change":
            print(change_contact(args, contacts))

        # Показ номера за ім'ям
        elif command == "phone":
            print(show_phone(args, contacts))

        # Показ усіх контактів
        elif command == "all":
            print(show_all(contacts))

        # Порожній ввід — нічого не робимо (можна ще раз показати підказку користувачу)
        elif command == "":
            continue

        # Невідома команда
        else:
            print("Invalid command.")


# Точка входу: запускаємо main() лише якщо скрипт виконують напряму
if __name__ == "__main__":
    main()

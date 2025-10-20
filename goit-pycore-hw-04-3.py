


import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)  # вмикає коректні кольори в терміналі (особливо на Windows)

def color_name(p: Path) -> str:
    """Повертає кольорове ім'я: синім для директорій, зеленим для файлів."""
    if p.is_dir():
        return Fore.BLUE + p.name + "/" + Style.RESET_ALL
    return Fore.GREEN + p.name + Style.RESET_ALL

def print_tree(root: Path, prefix: str = "") -> None:
    """Рекурсивно друкує дерево директорій із відступами та гілками."""
    try:
        entries = list(root.iterdir())
    except PermissionError:
        print(prefix + Fore.RED + "└── [Permission denied]" + Style.RESET_ALL)
        return

    # Директорії спочатку, потім файли; сортуємо за іменем без урахування регістру
    entries.sort(key=lambda p: (p.is_file(), p.name.casefold()))

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        branch = "└── " if is_last else "├── "
        print(prefix + branch + color_name(entry))

        # Рекурсія тільки в реальні директорії (не заходимо в symlink, щоб уникати циклів)
        if entry.is_dir() and not entry.is_symlink():
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(entry, next_prefix)

def main() -> int:
    # Отримуємо шлях із аргументів командного рядка (використовуємо sys, як вимагали)
    if len(sys.argv) != 2:
        print("Використання: python3 goit-pycore-hw-04-3.py <шлях/до/директорії>")
        return 1

    root = Path(sys.argv[1]).expanduser().resolve()

    if not root.exists():
        print(Fore.RED + f"Помилка: шлях не існує: {root}" + Style.RESET_ALL)
        return 2
    if not root.is_dir():
        print(Fore.RED + f"Помилка: це не директорія: {root}" + Style.RESET_ALL)
        return 3

    # Заголовок — друкуємо кореневу директорію
    print(Fore.BLUE + root.as_posix() + "/" + Style.RESET_ALL)
    print_tree(root)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

# Запуск
# у вже активованому віртуальному оточенні
# python3 goit-pycore-hw-04-3.py "/шлях/до/вашої/директорії"
# якщо в шляху є пробіли — обов'язково у лапках

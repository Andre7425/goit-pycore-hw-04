

from typing import List, Dict

def get_cats_info(path: str) -> List[Dict[str, str]]:
    """
    Зчитує файл формату:
        <id>,<name>,<age>
    та повертає список словників {"id": ..., "name": ..., "age": ...}.

    - Порожні рядки ігноруються.
    - Некоректні рядки (без трьох полів або з нечисловим age) пропускаються.
    - encoding='utf-8-sig' «з’їдає» можливий BOM на початку файлу.
    """
    cats: List[Dict[str, str]] = []

    try:
        with open(path, encoding="utf-8-sig") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line:
                    continue

                # Розбиваємо максимум на 3 частини (id, name, age).
                # Якщо раптом у name є коми — вони залишаться всередині name.
                parts = line.split(",", 2)
                if len(parts) != 3:
                    # некоректний рядок — пропускаємо
                    continue

                id_, name, age = (p.strip() for p in parts)
                if not id_ or not name or not age: # Після обрізання країв перевіряємо, що жодне поле не порожнє.
                    continue                       # Якщо якесь порожнє — пропускаємо рядок.   

                # Валідація віку: очікуємо число; у результаті все одно повертаємо як рядок
                if not age.isdigit():
                    # якщо потрібно — тут можна спробувати int(age) з обробкою,
                    # але в типових даних це має бути ціле число
                    continue

                cats.append({"id": id_, "name": name, "age": age})

    except FileNotFoundError:
        # повертаємо [] 
        return []

    return cats

cats_info = get_cats_info("cats.txt")
print(cats_info)
# [
#   {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
#   {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
#   {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": "2"},
#   {"id": "60b90c3b13067a15887e1ae4", "name": "Simon", "age": "12"},
#   {"id": "60b90c4613067a15887e1ae5", "name": "Tessi", "age": "5"},
# ]
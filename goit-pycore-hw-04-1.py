from typing import Tuple

def total_salary(path: str) -> Tuple[int, float]:
    """
    Повертає (сума_всіх_зарплат, середня_зарплата).
    Формат рядка: 'Прізвище Ім'я,число'. Порожні/биті рядки ігноруються.
    Якщо файл не знайдено або немає коректних рядків — (0, 0).
    """
    total = 0
    count = 0

    try:
        # utf-8-sig безпечно ковтає BOM, якщо він є
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    # беремо все праворуч від останньої коми як суму
                    _, salary_str = line.rsplit(",", 1)
                    salary = int(salary_str)
                except ValueError:
                    # якщо рядок пошкоджений — пропускаємо
                    continue
                total += salary
                count += 1
    except FileNotFoundError:  # якщо не існує файлу повертаємо 0 0
        return 0, 0

    if count == 0:
        return 0, 0    # якщо немає стрічок з інфо у файлі повертаємо 0 0

    average = round(total / count, 1)  # середня як float після . одна цифра
    return total, average
"""
вміст файлу list_workers.txt

Alex Tkachenko,2000
Andrii Sereda,1000
Maksym Doroba,3000
Petro Siryi,2000
Daryna Fedak,2000
Marta Goryn,3000
"""
total, average = total_salary("list_workers.txt") # 13000 2166.7
print(total, average)


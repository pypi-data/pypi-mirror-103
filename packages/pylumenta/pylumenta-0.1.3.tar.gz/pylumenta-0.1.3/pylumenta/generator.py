""" Polumenta generator """

import random

slova1 = (
    "Б",
    "В",
    "Г",
    "Д",
    "Ђ",
    "Ж",
    "З",
    "Ј",
    "К",
    "Л",
    "Љ",
    "М",
    "Н",
    "Њ",
    "П",
    "Р",
    "С",
    "Т",
    "Ћ",
    "Ф",
    "Х",
    "Ц",
    "Ч",
    "Џ",
    "Ш",
    "Б",
    "В",
    "Г",
    "Д",
    "Ђ",
    "Ж",
    "З",
    "Ј",
    "К",
    "Л",
    "Љ",
    "М",
    "Н",
    "Њ",
    "П",
    "Р",
    "С",
    "Т",
    "Ћ",
    "Ф",
    "Х",
    "Ц",
    "Ч",
    "Џ",
    "Ш",
    "Бл",
    "Бр",
    "Вл",
    "Вр",
    "Гл",
    "Гр",
    "Дл",
    "Др",
    "Жл",
    "Зл",
    "Зр",
    "Кр",
    "Кл",
    "Мр",
    "Мл",
    "Пј",
    "Пл",
    "Пљ",
    "Пњ",
    "Пр",
    "Св",
    "Сл",
    "См",
    "Сп",
    "Ст",
    "Тл",
    "Тр",
    "Фл",
    "Фљ",
    "Фњ",
    "Фр",
    "Хл",
    "Хр",
)

slova2 = ("а", "е", "и", "о", "у", "р")

slova3 = (
    "б",
    "в",
    "г",
    "д",
    "ђ",
    "ж",
    "з",
    "ј",
    "к",
    "л",
    "љ",
    "м",
    "н",
    "њ",
    "п",
    "р",
    "с",
    "т",
    "ћ",
    "ф",
    "х",
    "ц",
    "ч",
    "џ",
    "ш",
)


def jedanPolumenta():
    """Основна функција која генерише једног Полументу
    Args:

    Returns:
            string
    Raises:

    """
    poc = random.choice(slova1)
    srd = random.choice(slova2)
    kr = random.choice(slova3)
    while (
        list(poc[-1])
        in ["л", "р", "ј", "љ", "њ", "Ђ", "Ж", "Ј", "Л", "Љ", "Н", "Њ", "Р", "Ћ", "Ч", "Џ", "Ш"]
    ) and (kr == "р"):
        kr = random.choice(slova3)
    return f"{poc}{srd}{kr}o"


def Polumente(broj=1):
    """Функција која генерише једног или више полументи (до 100)
    и враћа их као листу
    Args:
            broj: број жељених Полумента
    Returns:
            list: листа генерисаних Полумента
    Raises:
            ValueError: if broj > 100
    """
    if broj < 1:
        broj = 1
    if broj > 100:
        raise ValueError("Највећи број Полумента је 100!")
    poliske = []
    while broj >= 1:
        pol = f"{jedanPolumenta()} Полумента"
        if pol in poliske:
            continue
        poliske.append(pol)
        broj -= 1
    return poliske


def rodiPolumentu(ime):
    """Функција која враћа да ли ће се у милион циклуса и
    у ком тачно родити дати Полумента
    Args:
            ime: име Полументе
    Returns:
            tuple: име из ime, бројач када је пронађено, да ли је пронађено или није
    Raises:
            ValueError: ако је унето више од једног имена/речи у ime
    """
    ime = ime.strip()
    if len(ime.split(" ")) > 1:
        raise ValueError("Дозвољен је унос само једног имена!")
    counter = 0
    status = False
    while True:
        counter += 1
        if jedanPolumenta() == ime:
            print(f"{ime} Полумента родио се у циклусу: {counter}")
            status = True
            break
        if counter % 10000 == 0:
            print(f"Прошло је {counter} циклуса...")
        if counter > 1000000:
            print(f"После {counter} циклуса није се родио {ime} Полумента")
            break
    return (ime, counter, status)


if __name__ == "__main__":
    print(Polumente(3))

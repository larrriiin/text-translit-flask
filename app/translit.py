from typing import Dict


# Базовая таблица транслитерации
TRANSLIT_MAP: Dict[str, str] = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def transliterate(text: str) -> str:
    """Перекодировка русского текста в транслит.
    Нерусские символы остаются без изменений.
    """
    result_chars = []

    for char in text:
        lower = char.lower()
        if lower in TRANSLIT_MAP:
            mapped = TRANSLIT_MAP[lower]
            # Сохраняем регистр: если исходная буква была заглавной
            if char.isupper():
                if mapped:
                    mapped = mapped[0].upper() + mapped[1:]
            result_chars.append(mapped)
        else:
            result_chars.append(char)

    return "".join(result_chars)

import re

def name_check(text: str) -> str:
    # Проверяем, что имя состоит только из букв и пробелов
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s]+$", text):
        raise ValueError("Имя должно содержать только буквы и пробелы.")
    
    # Проверяем длину имени
    if not (1 <= len(text) <= 50):
        raise ValueError("Имя должно содержать от 1 до 50 символов.")
    
    # Проверяем, что имя начинается с заглавной буквы
    if not text[0].isupper():
        raise ValueError("Имя должно начинаться с заглавной буквы.")
    
    return text


# Проверка текста на то, что он содержит число от 3 до 120 включительно
def age_check(text: str) -> str:
    if all(ch.isdigit() for ch in text) and 3 <= int(text) <= 120:
        return text
    raise ValueError
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



def phone_check(text: str) -> str:
    # Удаляем пробелы и лишние символы
    phone_number = text.strip()
    
    # Проверяем, что номер состоит только из цифр
    if not re.match(r"^\d+$", phone_number):
        raise ValueError("Номер телефона должен содержать только цифры.")
    
    # Проверяем длину номера телефона (опционально, например, не менее 10 цифр)
    if len(phone_number) < 10:
        raise ValueError("Номер телефона должен содержать как минимум 10 цифр.")
    
    return phone_number
    

def study_goal_check(text: str):
    # Удаляем лишние пробелы по краям строки
    description = text.strip()
    
    # Проверяем длину описания (например, минимум 10 символов, максимум 200)
    if not (5 <= len(description) <= 1000):
        raise ValueError("Описание должно содержать от 5 до 1000 символов.")
    
    return description
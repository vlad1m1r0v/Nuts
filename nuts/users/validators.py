import re
from django.core.exceptions import ValidationError

NAME_REGEX = re.compile(r'^[a-zA-Zа-яА-ЯёЁіІїЇєЄґҐ]+( [a-zA-Zа-яА-ЯёЁіІїЇєЄґҐ]+){1,2}$')

def full_name_validator(value):
    value = value.strip()
    if not NAME_REGEX.match(value):
        raise ValidationError(
            'Введите корректное ФИО (2 или 3 слова, без спецсимволов)'
        )


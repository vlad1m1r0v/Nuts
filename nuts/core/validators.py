import re
from django.core.exceptions import ValidationError

PHONE_REGEX = re.compile(r'^\+38 \(0\d{2}\) \d{3}-\d{2}-\d{2}$')

def ukrainian_phone_validator(value):
    if not PHONE_REGEX.match(value):
        raise ValidationError(
            'Мобильный телефон должен быть в формате +38 (0XX) XXX-XX-XX.'
        )


def validate_file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Файл слишком большой. Максимальный размер — 2 МБ.')
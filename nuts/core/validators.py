import re
from django.core.exceptions import ValidationError

PHONE_REGEX = re.compile(r'^\+38 \(0\d{2}\) \d{3}-\d{2}-\d{2}$')

def ukrainian_phone_validator(value):
    if not PHONE_REGEX.match(value):
        raise ValidationError(
            'Phone number must be in format +38 (0XX) XXX-XX-XX'
        )
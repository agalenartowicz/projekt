from django.core.validators import ValidationError
from django.contrib.auth import get_user_model

def validate_username(value):
    if get_user_model().objects.filter(username=value).exists():
        raise ValidationError("Użytkownik {} już istnieje!".format(value))

def validate_email(value):
    domain = value.split('@')[1]
    allowed_domain_list = ["lightcode.eu"]
    if domain not in allowed_domain_list:
        raise ValidationError("{} nie jest adresem mailowym w dozwolonej domenie".format(value))

from django import forms
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .validators import validate_username, validate_email

class BookSearchForm(forms.Form):
    name = forms.CharField(label="Podaj tytuł",
                           help_text="Wprowadź tytuł bądź jego fragment, by wyszukać książkę")

class BookAddForm(forms.Form):
    number = forms.CharField(label="Nr inw.",
                           help_text="Rok/numer: YYYY/num")
    name = forms.CharField(label="Tytuł",
                                help_text="Podaj tytuł")


class AddUserForm(forms.Form):
    username = forms.CharField(max_length=50, label="Nazwa użytkownika", validators=[validate_username])
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")
    first_name = forms.CharField(label="Imię")
    last_name = forms.CharField(label="Nazwisko")
    email = forms.EmailField(label="E-mail", validators=[validate_email])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            raise forms.ValidationError("Podane hasła nie są identyczne!")

class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
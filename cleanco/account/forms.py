from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


# registration form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = True
        self.fields[
            "username"
        ].help_text = "Використовуйте букви, цифри та знаки @/./+/-/_"
        self.fields["password1"].help_text = "Пароль має містити щонайменше 8 символів."
        self.fields["password2"].help_text = "Повторіть раніше введений пароль."

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з такою поштою вже зареєстрований!")

        if len(email) >= 350:
            raise forms.ValidationError("Пошта містить занадто багато символів!")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# updating info


class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ["password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = True
        self.fields[
            "username"
        ].help_text = "Використовуйте букви, цифри та знаки @/./+/-/_"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Користувач з такою поштою вже зареєстрований!")

        if len(email) >= 350:
            raise forms.ValidationError("Пошта містить занадто багато символів!")

        return email

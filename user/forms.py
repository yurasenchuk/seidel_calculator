from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from user.models import CustomUser

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


def validate_names(data: str):
    if not (data[0].isupper() and data.isalpha()):
        raise ValidationError("All symbols must be letters and first one must be uppercase")
    return data


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True, label="First name", validators=[validate_names],
                                 help_text="Enter first name")
    middle_name = forms.CharField(max_length=20, label="Middle name", validators=[validate_names], required=False,
                                  help_text="Enter middle name")
    last_name = forms.CharField(max_length=20, required=True, label="Last name", validators=[validate_names],
                                help_text="Enter last name")
    email = forms.EmailField(validators=[validate_email], required=True, max_length=100, label="Email",
                             help_text="Enter email")
    role = forms.ChoiceField(label="Role", choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "middle_name", "email", "password1", "password2", "role")

    def save(self, commit=True):
        return CustomUser.create(self.cleaned_data.get("email"), self.cleaned_data.get("password1"),
                                 self.cleaned_data.get("first_name"), self.cleaned_data.get("middle_name"),
                                 self.cleaned_data.get("last_name"))


class AuthoriseForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100, label="Email")
    password = forms.CharField(max_length=128, label="Password", required=True, widget=forms.PasswordInput)

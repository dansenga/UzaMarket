from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Téléphone (optionnel)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Mot de passe"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirmer le mot de passe"})


class SellerRegisterForm(RegisterForm):
    """Formulaire d'inscription vendeur."""

    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Adresse", "rows": 3}),
    )

    class Meta(RegisterForm.Meta):
        fields = ["username", "email", "phone", "address", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.SELLER
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Formulaire de connexion."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"})
    )


class ProfileForm(forms.ModelForm):
    """Formulaire de modification du profil."""

    class Meta:
        model = User
        fields = ["username", "email", "phone", "address", "avatar"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
        }

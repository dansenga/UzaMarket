from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """Formulaire d'envoi de message."""

    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Écrivez votre message...",
                "rows": 2,
                "id": "message-input",
            }),
        }
        labels = {"content": ""}

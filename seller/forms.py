from django import forms
from products.models import Product, Category


class ProductForm(forms.ModelForm):
    """Formulaire d'ajout/modification de produit par le vendeur."""

    class Meta:
        model = Product
        fields = [
            "name", "category", "description", "price",
            "quantity", "condition", "image", "image_url", "image_2", "image_3",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom du produit"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Description détaillée"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Prix en Francs Congolais (FC)"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://exemple.com/image.jpg"}),
            "image_2": forms.FileInput(attrs={"class": "form-control"}),
            "image_3": forms.FileInput(attrs={"class": "form-control"}),
        }

from django import forms


class CheckoutForm(forms.Form):
    """Formulaire de passage de commande."""

    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Adresse complète de livraison",
            "rows": 3,
        }),
        label="Adresse de livraison",
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Numéro de téléphone",
        }),
        label="Téléphone",
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("mobile_money", "Mobile Money (M-Pesa, Airtel Money, Orange Money…)"),
            ("cash_on_delivery", "Paiement à la livraison"),
        ],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Méthode de paiement",
    )
    mobile_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+243 XXX XXX XXX",
        }),
        label="Numéro Mobile Money",
        help_text="Requis pour le paiement par mobile money",
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Notes supplémentaires (optionnel)",
            "rows": 2,
        }),
        label="Notes",
    )

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get("payment_method")
        mobile = cleaned_data.get("mobile_number")
        if method == "mobile_money" and not mobile:
            self.add_error(
                "mobile_number",
                "Le numéro Mobile Money est requis pour le paiement mobile.",
            )
        return cleaned_data

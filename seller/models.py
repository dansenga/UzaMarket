from django.db import models

# Les modèles vendeur utilisent directement User (accounts) et Product (products).
# Ce fichier peut être étendu pour des fonctionnalités vendeur spécifiques.


class SellerProfile(models.Model):
    """Profil étendu du vendeur (optionnel)."""

    from django.conf import settings

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    shop_name = models.CharField(max_length=150, blank=True, verbose_name="Nom de la boutique")
    shop_description = models.TextField(blank=True, verbose_name="Description de la boutique")
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boutique de {self.user.username}"

    class Meta:
        verbose_name = "Profil vendeur"
        verbose_name_plural = "Profils vendeurs"

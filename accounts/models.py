from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé avec rôles."""

    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        SELLER = "seller", "Vendeur"
        ADMIN = "admin", "Administrateur"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name="Rôle",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Photo de profil"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """Catégorie de produits."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, help_text="Classe icône (ex: fas fa-laptop)")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]


class Product(models.Model):
    """Produit mis en vente."""

    class Condition(models.TextChoices):
        NEW = "new", "Neuf"
        LIKE_NEW = "like_new", "Comme neuf"
        GOOD = "good", "Bon état"
        FAIR = "fair", "État acceptable"

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Vendeur",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name="Catégorie",
    )
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix (FC)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité en stock")
    condition = models.CharField(
        max_length=10,
        choices=Condition.choices,
        default=Condition.NEW,
        verbose_name="État",
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Image principale")
    image_url = models.URLField(max_length=500, blank=True, verbose_name="URL de l'image (internet)")
    image_2 = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Image 2")
    image_3 = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Image 3")

    @property
    def display_image(self):
        """Retourne l'URL de l'image à afficher (upload ou URL internet)."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.quantity > 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

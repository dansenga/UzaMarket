"""
Script de création de données de démonstration pour UzaMarket.
Marketplace C2C en République Démocratique du Congo.
Monnaie : Franc Congolais (FC) — tous les prix sont en CDF.

Usage: python manage.py shell < seed_data.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uzashop.settings")
django.setup()

from accounts.models import User
from products.models import Category, Product
from seller.models import SellerProfile

print("\n🚀 === Initialisation des données UzaMarket (RDC) === \n")

# ─────────────────────────────────────────────
# 1. UTILISATEURS
# ─────────────────────────────────────────────

# Superadmin
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@uzamarket.cd",
        password="admin123",
        role="admin",
    )
    print("✅ Admin créé (admin / admin123)")

# Vendeur 1 — Kinshasa
seller1, created = User.objects.get_or_create(
    username="vendeur1",
    defaults={
        "email": "vendeur1@uzamarket.cd",
        "role": "seller",
        "phone": "+243 81 234 5678",
        "address": "Avenue du Commerce 45, Gombe, Kinshasa",
    },
)
if created:
    seller1.set_password("vendeur123")
    seller1.save()
    SellerProfile.objects.get_or_create(
        user=seller1,
        defaults={
            "shop_name": "Tech Kin Store",
            "shop_description": "Votre boutique tech de référence à Kinshasa. Smartphones, laptops et accessoires neufs et d'occasion.",
        },
    )
    print("✅ Vendeur 1 créé (vendeur1 / vendeur123) — Tech Kin Store")

# Vendeur 2 — Lubumbashi
seller2, created = User.objects.get_or_create(
    username="vendeur2",
    defaults={
        "email": "vendeur2@uzamarket.cd",
        "role": "seller",
        "phone": "+243 97 876 5432",
        "address": "Boulevard Lumumba 12, Lubumbashi",
    },
)
if created:
    seller2.set_password("vendeur123")
    seller2.save()
    SellerProfile.objects.get_or_create(
        user=seller2,
        defaults={
            "shop_name": "Maison Lushi",
            "shop_description": "Mode, maison et lifestyle. Les meilleurs produits du Katanga livrés chez vous.",
        },
    )
    print("✅ Vendeur 2 créé (vendeur2 / vendeur123) — Maison Lushi")

# Client
client, created = User.objects.get_or_create(
    username="client1",
    defaults={
        "email": "client1@uzamarket.cd",
        "role": "client",
        "phone": "+243 89 000 1234",
        "address": "Quartier Matonge, Commune de Kalamu, Kinshasa",
    },
)
if created:
    client.set_password("client123")
    client.save()
    print("✅ Client créé (client1 / client123)")

# ─────────────────────────────────────────────
# 2. CATÉGORIES
# ─────────────────────────────────────────────

categories_data = [
    {"name": "Électronique", "icon": "fas fa-laptop", "description": "Smartphones, ordinateurs, tablettes, accessoires tech"},
    {"name": "Vêtements & Mode", "icon": "fas fa-tshirt", "description": "Mode homme, femme, enfant — prêt-à-porter et accessoires"},
    {"name": "Maison & Jardin", "icon": "fas fa-home", "description": "Meubles, décoration, électroménager, jardinage"},
    {"name": "Véhicules & Motos", "icon": "fas fa-car", "description": "Voitures, motos, vélos, pièces détachées"},
    {"name": "Sports & Loisirs", "icon": "fas fa-futbol", "description": "Équipements sportifs, fitness, activités de plein air"},
    {"name": "Livres & Papeterie", "icon": "fas fa-book", "description": "Livres, manuels scolaires, fournitures de bureau"},
    {"name": "Beauté & Santé", "icon": "fas fa-spa", "description": "Cosmétiques, soins, parfums, bien-être"},
    {"name": "Alimentation", "icon": "fas fa-utensils", "description": "Produits alimentaires, boissons, épicerie fine"},
]

for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults=cat_data,
    )
    if created:
        print(f"✅ Catégorie créée : {cat.name}")

# ─────────────────────────────────────────────
# 3. PRODUITS — Prix en FC (Franc Congolais)
# ─────────────────────────────────────────────

# Récupérer les catégories
electronics = Category.objects.get(name="Électronique")
fashion = Category.objects.get(name="Vêtements & Mode")
home_cat = Category.objects.get(name="Maison & Jardin")
vehicles = Category.objects.get(name="Véhicules & Motos")
sports = Category.objects.get(name="Sports & Loisirs")
books = Category.objects.get(name="Livres & Papeterie")
beauty = Category.objects.get(name="Beauté & Santé")
food = Category.objects.get(name="Alimentation")

# Récupérer les vendeurs
s1 = User.objects.get(username="vendeur1")
s2 = User.objects.get(username="vendeur2")

products_data = [
    # ── ÉLECTRONIQUE (vendeur1 — Tech Kin Store) ──
    {
        "name": "iPhone 15 Pro Max 256GB",
        "category": electronics,
        "seller": s1,
        "description": "iPhone 15 Pro Max 256GB, titane naturel. Neuf sous emballage scellé avec garantie Apple 1 an. Double SIM (nano + eSIM). Livraison possible à Kinshasa.",
        "price": 2850000,
        "quantity": 3,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&h=600&fit=crop",
    },
    {
        "name": "MacBook Air M2 - Comme neuf",
        "category": electronics,
        "seller": s1,
        "description": "MacBook Air M2 2023, 8GB RAM, 256GB SSD, coloris Midnight. Utilisé 3 mois seulement, état impeccable. Chargeur et boîte d'origine inclus.",
        "price": 2200000,
        "quantity": 1,
        "condition": "like_new",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&h=600&fit=crop",
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "category": electronics,
        "seller": s1,
        "description": "Samsung Galaxy S24 Ultra 256GB, Titanium Gray. Neuf sous blister, double SIM physique. Stylet S Pen inclus. Garantie 1 an.",
        "price": 2500000,
        "quantity": 2,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&h=600&fit=crop",
    },
    {
        "name": "Écouteurs JBL Tune 770NC",
        "category": electronics,
        "seller": s1,
        "description": "Casque Bluetooth JBL Tune 770NC avec réduction de bruit active. Autonomie 44h. Neufs dans leur emballage.",
        "price": 95000,
        "quantity": 8,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=600&fit=crop",
    },
    {
        "name": "iPad Air 5ème génération",
        "category": electronics,
        "seller": s1,
        "description": "iPad Air M1, 64GB WiFi, coloris bleu. Écran Liquid Retina 10.9 pouces. Parfait pour études et travail. Très bon état.",
        "price": 1150000,
        "quantity": 1,
        "condition": "like_new",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&h=600&fit=crop",
    },
    {
        "name": "Chargeur solaire portable 20000mAh",
        "category": electronics,
        "seller": s1,
        "description": "Power bank solaire 20000mAh, 2 ports USB. Étanche, parfait pour les coupures de courant. Idéal pour Kinshasa !",
        "price": 45000,
        "quantity": 15,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&h=600&fit=crop",
    },

    # ── VÊTEMENTS & MODE (vendeur2 — Maison Lushi) ──
    {
        "name": "Costume homme slim fit - Bleu marine",
        "category": fashion,
        "seller": s2,
        "description": "Costume slim fit bleu marine, tissu italien. Tailles disponibles : M, L, XL. Parfait pour les occasions. Neuf avec étiquette.",
        "price": 185000,
        "quantity": 5,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=600&h=600&fit=crop",
    },
    {
        "name": "Sneakers Nike Air Max 90",
        "category": fashion,
        "seller": s2,
        "description": "Nike Air Max 90 blanches/noires, pointure 42. Portées 2 fois seulement, état quasi neuf. Authentiques avec boîte.",
        "price": 175000,
        "quantity": 1,
        "condition": "like_new",
        "image_url": "https://images.unsplash.com/photo-1543508282-6319a3e2621f?w=600&h=600&fit=crop",
    },
    {
        "name": "Robe wax africaine - Collection 2025",
        "category": fashion,
        "seller": s2,
        "description": "Magnifique robe en tissu wax authentique, coupe moderne. Fabriquée par des couturières congolaises. Taille M/L ajustable.",
        "price": 65000,
        "quantity": 4,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1590735213920-68192a487bc2?w=600&h=600&fit=crop",
    },
    {
        "name": "Sac à main cuir véritable",
        "category": fashion,
        "seller": s2,
        "description": "Sac à main en cuir véritable marron, design élégant. Plusieurs compartiments. Bandoulière ajustable.",
        "price": 120000,
        "quantity": 3,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&h=600&fit=crop",
    },

    # ── MAISON & JARDIN (vendeur2) ──
    {
        "name": "Canapé d'angle moderne gris",
        "category": home_cat,
        "seller": s2,
        "description": "Canapé d'angle en tissu gris, 5 places. Design contemporain, très confortable. Livraison à Lubumbashi et Kinshasa.",
        "price": 850000,
        "quantity": 2,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&h=600&fit=crop",
    },
    {
        "name": "Ventilateur sur pied - 3 vitesses",
        "category": home_cat,
        "seller": s2,
        "description": "Grand ventilateur sur pied 18 pouces, 3 vitesses, oscillant. Silencieux et puissant. Indispensable à Kinshasa !",
        "price": 75000,
        "quantity": 10,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1607400201889-565b1ee75f8e?w=600&h=600&fit=crop",
    },
    {
        "name": "Lot de 6 casseroles antiadhésives",
        "category": home_cat,
        "seller": s2,
        "description": "Set de 6 casseroles antiadhésives avec couvercles. Tous feux y compris induction. Neuves dans coffret cadeau.",
        "price": 135000,
        "quantity": 6,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=600&fit=crop",
    },

    # ── VÉHICULES (vendeur1) ──
    {
        "name": "Moto TVS Apache RTR 160",
        "category": vehicles,
        "seller": s1,
        "description": "Moto TVS Apache RTR 160cc, année 2024. Kilométrage 2500km. Excellent état, papiers en règle. Idéale pour Kinshasa.",
        "price": 3200000,
        "quantity": 1,
        "condition": "like_new",
        "image_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=600&h=600&fit=crop",
    },
    {
        "name": "Casque moto intégral - Noir mat",
        "category": vehicles,
        "seller": s1,
        "description": "Casque moto intégral homologué, visière anti-rayures, intérieur amovible et lavable. Taille L.",
        "price": 85000,
        "quantity": 5,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=600&h=600&fit=crop",
    },

    # ── SPORTS & LOISIRS (vendeur1) ──
    {
        "name": "Ballon de football Adidas Pro",
        "category": sports,
        "seller": s1,
        "description": "Ballon de football Adidas officiel, taille 5. Cousu main, qualité match. Idéal pour les terrains de Kinshasa.",
        "price": 55000,
        "quantity": 12,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1614632537190-23e4146777db?w=600&h=600&fit=crop",
    },
    {
        "name": "Tapis de yoga + accessoires",
        "category": sports,
        "seller": s2,
        "description": "Kit complet : tapis de yoga antidérapant 6mm, sangle de transport, 2 blocs en mousse. Parfait pour débuter.",
        "price": 42000,
        "quantity": 7,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&h=600&fit=crop",
    },

    # ── LIVRES & PAPETERIE (vendeur2) ──
    {
        "name": "Manuel de mathématiques - Terminale",
        "category": books,
        "seller": s2,
        "description": "Manuel complet de mathématiques pour la classe de Terminale, programme congolais. État neuf, aucune annotation.",
        "price": 25000,
        "quantity": 20,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&h=600&fit=crop",
    },
    {
        "name": "Pack fournitures scolaires complet",
        "category": books,
        "seller": s2,
        "description": "Pack rentrée : 10 cahiers 200 pages, stylos, crayons, gomme, règle, compas. Tout pour bien démarrer l'année scolaire.",
        "price": 35000,
        "quantity": 30,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=600&h=600&fit=crop",
    },

    # ── BEAUTÉ & SANTÉ (vendeur2) ──
    {
        "name": "Coffret parfum homme - Eau de toilette",
        "category": beauty,
        "seller": s2,
        "description": "Coffret cadeau : eau de toilette 100ml + déodorant + gel douche. Fragrance boisée et élégante. Neuf scellé.",
        "price": 78000,
        "quantity": 6,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=600&h=600&fit=crop",
    },
    {
        "name": "Kit soins visage naturel",
        "category": beauty,
        "seller": s2,
        "description": "Kit de soins naturels : crème hydratante, sérum, nettoyant. Ingrédients bio, adapté peaux africaines. Fabriqué au Congo.",
        "price": 52000,
        "quantity": 8,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=600&fit=crop",
    },

    # ── ALIMENTATION (vendeur1) ──
    {
        "name": "Café du Kivu - Premium 500g",
        "category": food,
        "seller": s1,
        "description": "Café arabica premium du Kivu, torréfaction artisanale. 500g de grains entiers. Saveur douce et fruitée, fierté congolaise !",
        "price": 28000,
        "quantity": 25,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&h=600&fit=crop",
    },
    {
        "name": "Chocolat artisanal congolais - Lot de 5",
        "category": food,
        "seller": s1,
        "description": "Lot de 5 tablettes de chocolat noir 70% cacao, fabriqué avec du cacao congolais premium. 100g chaque. Un délice !",
        "price": 35000,
        "quantity": 15,
        "condition": "new",
        "image_url": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=600&h=600&fit=crop",
    },
]

for prod_data in products_data:
    prod, created = Product.objects.get_or_create(
        name=prod_data["name"],
        defaults=prod_data,
    )
    if created:
        print(f"✅ Produit créé : {prod.name} — {prod.price:,.0f} FC")

print(f"\n📊 Résumé :")
print(f"   👤 Utilisateurs : {User.objects.count()}")
print(f"   📂 Catégories   : {Category.objects.count()}")
print(f"   📦 Produits      : {Product.objects.count()}")
print(f"\n🎉 Données de démonstration chargées avec succès !")
print(f"🔗 Comptes : admin/admin123 | vendeur1/vendeur123 | vendeur2/vendeur123 | client1/client123\n")

print("\n🎉 Données de démonstration chargées avec succès !")
print("   - Admin : admin / admin123")
print("   - Vendeur : vendeur1 / vendeur123")
print("   - Client : client1 / client123")

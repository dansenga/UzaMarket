# 🛒 UzaMarket — Marketplace C2C pour la RDC

**UzaMarket** est une plateforme e-commerce C2C (Consumer-to-Consumer) conçue pour la République Démocratique du Congo. Elle permet aux particuliers d'acheter et de vendre des produits neufs ou d'occasion, avec paiement sécurisé via Mobile Money et Monero (XMR).

## ✨ Fonctionnalités

- **Catalogue produits** — Navigation par catégories, recherche, filtres (prix, état, catégorie)
- **Système vendeur** — Inscription vendeur, tableau de bord, gestion des produits et commandes
- **Panier & commandes** — Ajout au panier, checkout, historique des commandes
- **Paiement Mobile Money** — M-Pesa, Airtel Money, Orange Money, Afri Money
- **Paiement Monero (XMR)** — Option crypto décentralisée et privée
- **Messagerie client ↔ vendeur** — Conversations en temps réel liées aux produits
- **Panneau d'administration** — Gestion utilisateurs, modération produits, suivi commandes
- **Design Indigo & Amber** — Interface moderne avec animations et preloader
- **Responsive** — Optimisé mobile, tablette et desktop
- **Monnaie locale** — Tous les prix en Franc Congolais (FC / CDF)

## 🛠️ Technologies

| Technologie | Version |
|---|---|
| Python | 3.12+ |
| Django | 6.0.2 |
| Bootstrap | 5.3.2 |
| HTMX | 1.9.10 |
| Font Awesome | 6.5.1 |
| SQLite | 3 (dev) |

## 🚀 Installation

```bash
# Cloner le repo
git clone git@github.com:dansenga/UzaShop.git
cd UzaShop

# Installer les dépendances
pip install django django-htmx pillow

# Appliquer les migrations
python manage.py migrate

# Charger les données de démo
python manage.py shell < seed_data.py

# Lancer le serveur
python manage.py runserver
```

## 👤 Comptes de démonstration

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Admin | `admin` | `admin123` |
| Vendeur | `vendeur1` | `vendeur123` |
| Vendeur | `vendeur2` | `vendeur123` |
| Client | `client1` | `client123` |

## 📁 Structure du projet

```
UzaShop/
├── accounts/       # Auth, profil, rôles (client/vendeur/admin)
├── products/       # Catalogue, catégories, produits
├── cart/           # Panier d'achat
├── orders/         # Commandes, checkout, paiements
├── seller/         # Espace vendeur
├── messaging/      # Messagerie client ↔ vendeur
├── core/           # Pages statiques + panneau admin
├── templates/      # Templates Django
├── static/         # CSS, JS, images
└── uzashop/        # Config Django (settings, urls)
```

## 🎨 Design System

- **Palette** : Indigo (`#6366F1`) & Amber (`#F59E0B`)
- **Typographies** : Inter (corps) + Playfair Display (titres)
- **Animations** : Preloader, scroll reveal, hover transitions
- **Icônes** : Font Awesome 6

## 📍 Contexte

Projet conçu pour le marché congolais (RDC) :
- Fuseau horaire : `Africa/Kinshasa`
- Langue : Français
- Monnaie : Franc Congolais (FC)
- Adresses : Kinshasa, Lubumbashi, etc.

---

🇨🇩 Fait avec ❤️ en RD Congo

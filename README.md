<p align="center">
  <img src="static/img/favicon.svg" alt="UzaMarket Logo" width="80" height="80" style="border-radius: 16px;">
</p>

<h1 align="center">UzaMarket</h1>
<p align="center"><strong>Marketplace C2C pour la République Démocratique du Congo</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.0.2-success?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Bootstrap-5.3.2-purple?logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Licence-Académique-orange" alt="Licence">
</p>

---

## 📋 À propos

**UzaMarket** est une plateforme e-commerce C2C (Consumer-to-Consumer) développée dans le cadre d'un projet académique. Elle permet aux particuliers d'acheter et de vendre des produits neufs ou d'occasion en RDC, avec paiement sécurisé via **Mobile Money (Moneroo)** et **paiement à la livraison**.

## 👥 Équipe du projet

| Nom | Matricule |
|---|---|
| **SENGA KABEYA Dan** | 2023021017 |
| **KABOLE SHIMUBANGA Blessing** | 2023021056 |
| **KABANGU MULAPA Gloria** | 2023021108 |
| **MAJIVUNO MASUDI Cesar** | 2023021120 |
| **MONGA WA NGOY Elohim** | 2023021035 |

## ✨ Fonctionnalités

### 🛍️ Marketplace
- **Catalogue produits** — Navigation par catégories, recherche, filtres (prix, état, catégorie)
- **Fiches produits détaillées** — Images, descriptions, état, vendeur
- **Panier & checkout** — Ajout au panier, gestion des quantités, commande

### 💳 Paiement
- **Mobile Money via Moneroo** — M-Pesa, Airtel Money, Orange Money (intégration API sécurisée)
- **Paiement à la livraison** — Option cash pour les clients
- **Mode sandbox** — Simulation de paiement pour le développement

### 👤 Utilisateurs & Vendeurs
- **Système de rôles** — Client, Vendeur, Administrateur
- **Espace vendeur** — Tableau de bord, gestion des produits et commandes
- **Profil utilisateur** — Avatar, statistiques, historique

### 💬 Communication
- **Messagerie intégrée** — Conversations client ↔ vendeur liées aux produits
- **Notifications** — Badge temps réel pour les messages non lus
- **Bouton "Contacter le vendeur"** — Accessible depuis chaque produit

### 🛡️ Administration
- **Panneau d'administration** — Gestion utilisateurs, modération produits, suivi commandes
- **Dashboard statistiques** — Vue d'ensemble de l'activité

### 🎨 Design & UX
- **Design Indigo & Amber** — Interface premium avec identité visuelle forte
- **Pages auth split-screen** — Connexion, inscription avec branding
- **Page profil structurée** — Bannière, stats, sidebar, formulaire
- **Footer moderne** — Sections structurées, icônes sociales
- **Responsive** — Optimisé mobile, tablette et desktop
- **Animations** — Preloader, scroll reveal, hover transitions

## 🛠️ Technologies

| Technologie | Version | Rôle |
|---|---|---|
| Python | 3.12+ | Langage backend |
| Django | 6.0.2 | Framework web |
| Bootstrap | 5.3.2 | Framework CSS |
| HTMX | 1.9.10 | Interactions dynamiques |
| Font Awesome | 6.5.1 | Icônes |
| Moneroo API | v1 | Paiement Mobile Money |
| SQLite | 3 | Base de données (dev) |

## 🚀 Installation

```bash
# Cloner le repo
git clone git@github.com:dansenga/UzaMarket.git
cd UzaMarket

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install django django-htmx pillow requests

# Appliquer les migrations
python manage.py migrate

# Charger les données de démo
python manage.py shell < seed_data.py

# Lancer le serveur
python manage.py runserver
```

Accédez à l'application sur **http://localhost:8000**

## 👤 Comptes de démonstration

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Administrateur | `admin` | `admin123` |
| Vendeur | `vendeur1` | `vendeur123` |
| Vendeur | `vendeur2` | `vendeur123` |
| Client | `client1` | `client123` |

## 📁 Structure du projet

```
UzaShop/
├── accounts/          # Auth, profil, rôles (client/vendeur/admin)
├── products/          # Catalogue, catégories, produits
├── cart/              # Panier d'achat
├── orders/            # Commandes, checkout, paiements Moneroo
│   └── payments.py    # Service Moneroo (sandbox + production)
├── seller/            # Espace vendeur (dashboard, gestion)
├── messaging/         # Messagerie client ↔ vendeur
│   └── templatetags/  # Tag unread_messages_count
├── core/              # Pages statiques + panneau admin
├── templates/         # Templates Django (auth, profil, produits…)
├── static/
│   ├── css/style.css  # Design system complet
│   ├── js/main.js     # Animations, preloader, HTMX
│   └── img/           # Favicon SVG, images
└── uzashop/           # Config Django (settings, urls)
```

## 🎨 Design System

| Élément | Valeur |
|---|---|
| Couleur primaire | Indigo `#6366F1` |
| Couleur accent | Amber `#F59E0B` |
| Typo corps | Inter |
| Typo titres | Playfair Display |
| Icônes | Font Awesome 6 |
| Border radius | 8px — 24px |

## ⚙️ Configuration Moneroo

Pour activer les paiements en production, modifiez `uzashop/settings.py` :

```python
MONEROO_SECRET_KEY = "votre_clé_secrète_moneroo"
MONEROO_WEBHOOK_SECRET = "votre_secret_webhook"
```

> En mode développement, le système fonctionne automatiquement en **sandbox** (simulation locale).

## 📍 Contexte

Projet académique conçu pour le marché congolais (RDC) :
- 🏫 Projet universitaire
- 🌍 Fuseau horaire : `Africa/Kinshasa`
- 🇫🇷 Langue : Français
- 💰 Monnaie : Franc Congolais (FC / CDF)
- 📍 Localisation : Kinshasa, Lubumbashi, etc.

---

<p align="center">🇨🇩 Fait avec ❤️ en RD Congo</p>
<p align="center"><sub>© 2026 UzaMarket — Projet académique</sub></p>

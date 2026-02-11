# UzaShop - Plateforme E-commerce C2C

UzaShop est une application e-commerce C2C (Consumer to Consumer) développée avec Django, permettant aux particuliers de vendre et d'acheter des produits neufs ou d'occasion.

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/UzaShop.git
cd UzaShop

# 2. Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superutilisateur
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

L'application est accessible sur http://127.0.0.1:8000

## 📁 Structure du projet

```
UzaShop/
├── accounts/       # Gestion des utilisateurs et rôles
├── products/       # Catalogue et produits
├── cart/           # Panier d'achat
├── orders/         # Commandes et paiements
├── seller/         # Espace vendeur
├── core/           # Pages générales (accueil, about, contact)
├── templates/      # Templates HTML
├── static/         # Fichiers statiques (CSS, JS, images)
├── media/          # Fichiers uploadés
└── uzashop/        # Configuration Django
```

## 👥 Rôles utilisateurs

- **Client** : consulter, acheter des produits
- **Vendeur** : ajouter/gérer des produits, gérer les commandes reçues
- **Admin** : accès au panel d'administration Django

## 🛠 Technologies

- **Backend** : Django, SQLite
- **Frontend** : Bootstrap 5, HTMX, Font Awesome
- **Auth** : Django Authentication System

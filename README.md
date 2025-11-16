"# Système de Réservation d'Hôtel

Application web complète de gestion de réservations d'hôtel avec Django (backend) et Vue.js (frontend).

## 📋 Prérequis

- Python 3.13 ou supérieur
- Node.js 24 ou supérieur
- npm ou yarn
- Git

## 🚀 Installation et Lancement en Local

### Backend Django

1. **Naviguer vers le dossier backend**
   ```bash
   cd backend
   ```

2. **Créer un environnement virtuel Python**
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

3. **Activer l'environnement virtuel**
   ```bash
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

5. **Appliquer les migrations de base de données**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur (optionnel)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement Django**
   ```bash
   python manage.py runserver
   ```
   
   Le backend sera accessible sur : http://localhost:8000

### Frontend Vue.js

1. **Ouvrir un nouveau terminal et naviguer vers le dossier frontend**
   ```bash
   cd frontend
   ```

2. **Installer les dépendances Node.js**
   ```bash
   npm install
   # ou avec yarn
   yarn install
   ```

3. **Builder l'application pour la production**
   ```bash
   npm run build
   # ou avec yarn
   yarn build
   ```

4. **Installer serve (si ce n'est pas déjà fait)**
   ```bash
   npm install -g serve
   ```

5. **Lancer l'application**
   ```bash
   serve -s dist
   ```
   
   Le frontend sera accessible sur : http://localhost:3000

### Mode Développement (optionnel)

Si vous souhaitez travailler en mode développement avec hot-reload :

```bash
npm run dev
# ou avec yarn
yarn dev
```


## 🔐 Système de Permissions

L'application utilise un système de permissions basé sur les rôles :

### Rôles Disponibles

- **Receptionniste** : Accès de base pour la réception
  - ✅ Voir les chambres
  - ✅ Créer des réservations
  - ✅ Ajouter des paiements
  - ✅ Échanger des chambres
  - ❌ Annuler des réservations
  - ❌ Gérer la configuration
  - ❌ Accès au dashboard

- **Manager** : Accès complet sauf dashboard
  - ✅ Toutes les permissions du Receptionniste
  - ✅ Créer/Modifier/Supprimer des chambres
  - ✅ Annuler des réservations
  - ✅ Gérer la configuration de l'hôtel
  - ❌ Accès au dashboard statistiques

- **Superviseur** : Accès complet
  - ✅ Toutes les permissions
  - ✅ Accès au dashboard avec statistiques

## 📁 Structure du Projet

```
hotel_reservation/
├── backend/                 # Application Django
│   ├── accounts/           # Gestion des utilisateurs et profils
│   ├── core/               # Configuration principale et permissions
│   ├── dashboard/          # Dashboard et statistiques
│   ├── entity/             # Informations de l'entreprise
│   ├── reservation/        # Gestion des réservations
│   ├── rooms/              # Gestion des chambres
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/               # Application Vue.js
    ├── src/
    │   ├── assets/         # Images et styles
    │   ├── components/     # Composants Vue réutilisables
    │   ├── composables/    # Fonctions composables (permissions, currency)
    │   ├── directives/     # Directives personnalisées (v-permission)
    │   ├── router/         # Configuration des routes
    │   ├── services/       # Services API
    │   ├── stores/         # State management (Pinia)
    │   └── views/          # Pages de l'application
    ├── package.json
    └── vite.config.js

```

## 🔧 Configuration

### Variables d'environnement Backend

Créez un fichier `.env` dans le dossier `backend/` (optionnel) :

```env
DEBUG=True
SECRET_KEY=votre-clé-secrète
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuration Frontend

Le fichier `frontend/src/config/api.js` contient la configuration de l'API :

```javascript
export const API_BASE_URL = 'http://localhost:8000'
```

## 📚 Fonctionnalités Principales

- ✅ Gestion des chambres (types, étages, statuts)
- ✅ Réservations multiples (plusieurs chambres pour un client)
- ✅ Gestion des paiements (cash, mobile money, carte, etc.)
- ✅ Échange de chambres
- ✅ Système de permissions par rôle
- ✅ Facturation et impression
- ✅ Dashboard avec statistiques (Superviseur uniquement)
- ✅ Support multi-devises (13 devises disponibles)
- ✅ Gestion des invités
- ✅ Historique des paiements

## 🛠️ Technologies Utilisées

### Backend
- Django 5.x
- Django REST Framework
- SQLite (dev) / PostgreSQL (prod recommandé)
- JWT Authentication

### Frontend
- Vue.js 3 (Composition API)
- Vue Router
- Pinia (State Management)
- Vite (Build tool)
- Tailwind CSS
- Notivue (Notifications)

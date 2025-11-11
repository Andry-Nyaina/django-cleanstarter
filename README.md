# 🧩 Django CleanStarter

**Django CleanStarter** est une base de projet Django propre, modulaire et prête pour le développement professionnel.  
Il s’agit du socle de départ que j’utilise pour mes projets **Fullstack (Django + React)** et **IA / Data Automation**.

---

## 🚀 Objectif du projet

L’objectif est de disposer d’une structure **scalable**, **sécurisée** et **simple à maintenir**, adaptée :
- aux projets Django modernes (API REST, intégration React, automatisation IA)
- aux bonnes pratiques de configuration (environnements, `.env`, séparation `base/dev/prod`)
- aux workflows GitHub professionnels (commits clairs, README complet, push régulier)

---

## 🛠️ Stack & outils utilisés

- **Python 3.11+**
- **Django 5+**
- **python-decouple** (gestion des variables d’environnement)
- **Git & GitHub**
- **pipenv / venv** pour l’environnement virtuel

---

## ⚙️ Structure du projet
django-cleanstarter/<br>
├── config/<br>
│ ├── settings/<br>
│ │ ├── base.py<br>
│ │ ├── dev.py<br>
│ │ ├── prod.py<br>
│ └── urls.py<br>
│<br>
├── core/<br>
│ ├── templates/<br>
│ │ └── core/<br>
│ │ └── home.html<br>
│ ├── static/<br>
│ │ └── core/<br>
│ │ └── style.css<br>
│ ├── views.py<br>
│ └── urls.py<br>
│<br>
├── manage.py<br>
├── .env<br>
└── .gitignore<br>

---

## 🔐 Variables d’environnement (.env)

Exemple de configuration :

SECRET_KEY=django-insecure-1234567890

DB_NAME=cleanstarter

DB_USER=postgres

DB_PASSWORD=password

DB_HOST=localhost

DB_PORT=5432

DJANGO_SETTINGS_MODULE=config.settings.dev


---

## ▶️ Démarrage rapide

1️⃣ **Cloner le dépôt**
```bash
git clone https://github.com/Andry-Nyaina/django-cleanstarter.git
cd django-cleanstarter
```

2️⃣  **Créer et activer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate
```

3️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4️⃣ **Lancer le serveur**
```bash
python manage.py runserver --settings=config.settings.dev
```
➡️ Accès à l’application : http://127.0.0.1:8000




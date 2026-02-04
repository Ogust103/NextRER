# NextRER

Application web Flask pour afficher les prochains horaires de RER en temps réel, conçue pour fonctionner sur un Raspberry Pi.

## Description

NextRER récupère les horaires en temps réel des trains RER depuis l'API Île-de-France Mobilités et les affiche dans une interface web pour un affichage permanent sur un Raspberry Pi avec écran.

## Fonctionnalités

- Affichage des prochains trains RER en temps réel
- Indication de la destination et du quai
- Heures d'arrivée prévues et réelles
- API REST pour récupérer les données
- Configuration flexible des stations et directions
- Interface web responsive

## 🛠️ Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)
- Une clé API Île-de-France Mobilités

### Étapes d'installation

1. **Cloner le dépôt** (ou télécharger les fichiers)
   ```bash
   git clone <url-du-repo>
   cd NextRER
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer l'API key**
   
   Créer un fichier `.env` à la racine du projet (vous pouvez copier `.env.example`) :
   ```bash
   cp .env.example .env
   ```
   
   Éditer le fichier `.env` et ajouter votre clé API :
   ```
   API_KEY=votre_cle_api_ici
   ```

4. **Configurer votre station** (optionnel)
   
   Modifier [config.py](config.py) pour personnaliser :
   - La station par défaut (`DEFAULT_STATION_ID`)
   - Les correspondances quai/direction (`PLATFORM_DIRECTIONS`)
   - Les noms de stations (`STATION_NAMES`)

## 🚀 Utilisation

### Lancer l'application

```bash
py app.py
ou
flask --app app.py --debug run
```

L'application sera accessible sur `http://localhost:5000`

### Sur Raspberry Pi

Pour lancer automatiquement au démarrage, créer un service systemd ou ajouter au crontab :

```bash
@reboot cd /chemin/vers/NextRER && python app.py
```

## 📡 API

### GET `/`
Page d'accueil affichant les prochains trains

### GET `/api/next_rers`
Récupère les données JSON des prochains trains

**Paramètres :**
- `station_id` (optionnel) : ID de la station à interroger

**Exemple :**
```bash
curl http://localhost:5000/api/next_rers?station_id=53783
```

**Réponse :**
```json
[
  {
    "destinationName": "Paris Saint-Lazare",
    "vehicleJourneyName": "TOLA",
    "vehicleAtStop": false,
    "expectedArrivalTime": "2026-01-31T14:23:00+01:00",
    "expectedDepartureTime": "2026-01-31T14:23:00+01:00",
    "aimedArrivalTime": "2026-01-31T14:23:00+01:00",
    "aimedDepartureTime": "2026-01-31T14:23:00+01:00",
    "platform": "1"
  }
]
```

## 📁 Structure du projet

```
NextRER/
├── app.py                 # Application Flask principale
├── config.py              # Configuration (stations, quais, directions)
├── .env                   # Variables d'environnement (API key) - NON VERSIONNÉ
├── .env.example           # Template pour .env
├── requirements.txt       # Dépendances Python
├── .gitignore            # Fichiers à ignorer par Git
├── README.md             # Ce fichier
├── static/
│   └── style.css         # Styles CSS
└── templates/
    └── index.html        # Template HTML
```

## 🔧 Configuration

### Obtenir une clé API

1. Aller sur [Île-de-France Mobilités](https://prim.iledefrance-mobilites.fr/)
2. Créer un compte 
4. Récupérer votre clé API

### Trouver l'ID de votre station

L'ID de station suit le format STIF. Vous pouvez le trouver en consultant la documentation de l'API Île-de-France Mobilités :[Référentiel des arrêts : Zones d'arrêts](https://prim.iledefrance-mobilites.fr/fr/jeux-de-donnees/zones-d-arrets)

Exemple : `53783` pour Chatou-Croissy

### Configuration des quais

Dans [config.py](config.py), vous pouvez configurer les correspondances entre numéros de quai et directions

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

Ce projet est libre d'utilisation.

## Remerciements

- API fournie par [Île-de-France Mobilités](https://prim.iledefrance-mobilites.fr/)
- Conçu pour fonctionner sur Raspberry Pi

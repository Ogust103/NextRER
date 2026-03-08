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

- Python 3.8 ou supérieur
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

  Sous Linux / macOS :
   ```bash
   cp .env.example .env
   ```

  Sous Windows (PowerShell) :
  ```powershell
  Copy-Item .env.example .env
  ```
   
   Éditer le fichier `.env` et ajouter votre clé API :
   ```
   API_KEY=votre_cle_api_ici
   ```

   Spécifier votre environnement (production/development):
   ```
   FLASK_ENV=production
   ```

4. **Configurer votre station** (optionnel)
   
   Modifier [config.py](config.py) pour personnaliser :
   - La station par défaut (`STATION_ID`) — ex: `"53783"` (Chatou‑Croissy) en utilisant le [Référentiel des arrêts : Zones d'arrêts](https://prim.iledefrance-mobilites.fr/fr/jeux-de-donnees/zones-d-arrets)
   - Les correspondances quais/directions (`DIRECTIONS`) :
     - `platform` (ex: `"1"` / `"2"`)
     - `quayRef` en utilisant le [Référentiel des arrêts : Arrêts](https://prim.iledefrance-mobilites.fr/fr/jeux-de-donnees/arrets?staticDataSlug=arrets)
     - `directionNames`
     - `directionCodes` en utilisant le [Référentiel des arrêts : Zones d'arrêts](https://prim.iledefrance-mobilites.fr/fr/jeux-de-donnees/zones-d-arrets)
   - Les noms de stations (`STATION_NAMES`) pour l’affichage
   - Les coordonnées météo (`WEATHER_INFO` : `latitude`, `longitude`)

## 🚀 Utilisation

### Lancer l'application

```bash
py app.py
ou
python3 app.py
ou
python app.py
```

Mode développement (optionnel) :

```bash
flask --app app.py --debug run
```

L'application sera accessible sur `http://localhost:5000`

### Sur Raspberry Pi

#### Lancement au démarrage (Optionnel)

Pour lancer automatiquement au démarrage, créer un fichier start_app.sh :

```bash
#!/bin/bash

fuser -k 5000/tcp 2>/dev/null

cd /home/path/to/NextRER
python3 app.py &
sleep 10
chromium --no-sandbox --kiosk http://127.0.0.1:5000/
```

Le rendre exécutable :
```bash
chmod +x start_app.sh
```

Puis créer un service systemd ou ajouter au crontab :
```bash
crontab -e
```

```bash
@reboot export DISPLAY=:0 && export XAUTHORITY=/home/user/.Xauthority && /home/path/to/NextRER/start_app.sh
```

#### Economie d'énergie (Optionnel)

Il est aussi possible de gérer la mise en veille de l'écran en fonction des heures avec swayidle :

Prérequis :
- `swayidle`
- `wlopm`

Créer un fichier update_idle_time_hour.sh :

```bash
#!/bin/bash

CURRENT_HOUR=$(date +%-H)

ACTIVE_HOURS=(6 7 8)
INACTIVE_HOURS=(0 1 2 3 4 5 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23)

# Définit le délai en fonction de l'heure
if [[ " ${ACTIVE_HOURS[*]} " =~ " $CURRENT_HOUR " ]]; then
  NEW_TIMEOUT=4200
elif [[ " ${INACTIVE_HOURS[*]} " =~ " $CURRENT_HOUR " ]]; then
  NEW_TIMEOUT=1200
  if pgrep -f "swayidle.*timeout $NEW_TIMEOUT" > /dev/null; then
    exit 0
  fi
else
  exit 0 
fi

# Tue le processus swayidle existant (s'il existe)
pkill swayidle

# Relance swayidle avec le nouveau délai (en secondes)
swayidle -w timeout "$NEW_TIMEOUT" 'wlopm --off \*' resume 'wlopm --on \*' &

echo "Délai avant mise en veille mis à $NEW_TIMEOUT secondes"
```

Définir les heures actives (où l'écran reste allumé en permanence), et les heures inactives où l'écran reste allumé 1200 secondes (à définir) jusqu'à action avec l'écran.

Le rendre exécutable :
```bash
chmod +x update_idle_time_hour.sh
```

Puis créer un service systemd ou ajouter au crontab :
```bash
crontab -e
```

```bash
1 * * * * export WAYLAND_DISPLAY=wayland-0 && export XDG_RUNTIME_DIR=/run/user/1000 && /home/user/Documents/NextRER/update_idle_time_hour.sh >> /home/user/cron_debug.log 2>&1
```
Le timeout sera ainsi actualisé à la première minute de chaque heure.

## 📡 API

### GET `/`
Page d'accueil affichant les prochains trains

### GET `/api/next_rers`
Récupère les données JSON des prochains trains pour la station configurée.

**Réponse :**
```json
[
  {
    "destinationName": "Paris Saint-Lazare",
    "destinationCode": "STIF:StopArea:SP:43094:",
    "vehicleJourneyName": "TOLA",
    "vehicleAtStop": false,
    "expectedArrivalTime": "2026-01-31T14:23:00+01:00",
    "expectedDepartureTime": "2026-01-31T14:23:00+01:00",
    "aimedArrivalTime": "2026-01-31T14:23:00+01:00",
    "aimedDepartureTime": "2026-01-31T14:23:00+01:00",
    "platform": "1",
    "quayRef": "STIF:StopPoint:Q:473964:"
  }
]
```

**Champs retournés :**
- `destinationName` : Nom de la destination (ex: "Paris Saint-Lazare")
- `destinationCode` : Code STIF de la destination
- `vehicleJourneyName` : Identification du train (ex: "TOLA")
- `vehicleAtStop` : Indique si le véhicule est en gare (booléen)
- `expectedArrivalTime` : Heure d'arrivée attendue (ISO 8601)
- `expectedDepartureTime` : Heure de départ attendue (ISO 8601)
- `aimedArrivalTime` : Heure d'arrivée prévue initiale (ISO 8601)
- `aimedDepartureTime` : Heure de départ prévue initiale (ISO 8601)
- `platform` : Numéro du quai
- `quayRef` : Référence STIF du quai

### GET `/api/weather`
Récupère les données météorologiques pour les coordonnées configurées (prévisions actuelles, horaires et quotidiennes).

**Réponse :**
```json
{
  "current": {
    "temperature": 12.5,
    "is_day": 1,
    "weather_code": 45
  },
  "hourly": {
    "2026-02-05T15:00:00": {
      "temperature": 12.3,
      "is_day": 1,
      "weather_code": 3
    },
  },
  "daily": {
    "2026-02-05": {
      "temperature_max": 14.2,
      "temperature_min": 8.5,
      "sunrise": "2026-02-05T07:45:00",
      "sunset": "2026-02-05T18:20:00",
      "weather_code": 51
    },
  }
}
```

**Champs retournés - `current` (données actuelles) :**
- `temperature` : Température actuelle (°C)
- `is_day` : Indique si c'est le jour (1) ou la nuit (0)
- `weather_code` : Code météo WMO

**Champs retournés - `hourly` (données horaires) :**
- `temperature` : Température horaire (°C)
- `is_day` : Indique si c'est le jour (1) ou la nuit (0)
- `weather_code` : Code météo WMO

**Champs retournés - `daily` (prévisions quotidiennes) :**
- `temperature_max` : Température maximale (°C)
- `temperature_min` : Température minimale (°C)
- `sunrise` : Heure du lever du soleil (ISO 8601)
- `sunset` : Heure du coucher du soleil (ISO 8601)
- `weather_code` : Code météo WMO

## 📁 Structure du projet

```
NextRER/
├── app.py                 # Application Flask principale
├── config.py              # Configuration (stations, quais, directions)
├── .env                   # Variables d'environnement (API key) - NON VERSIONNÉ
├── .env.example           # Template pour .env
├── requirements.txt       # Dépendances Python
├── .gitignore             # Fichiers à ignorer par Git
├── README.md              # Ce fichier
├── static/
│   ├── Logo RERA.png     # Logo RERA
│   ├── style.css         # Styles CSS
│   ├── js/
│   │   ├── api.js        # Appels API frontend
│   │   ├── main.js       # Logique principale frontend
│   │   ├── ui.js         # Rendu de l'interface
│   │   └── utils.js      # Fonctions utilitaires frontend
│   ├── weather_icons/    # Icônes météo
│   └── weather_images/   # Images météo
├── templates/
│   └── index.html        # Template HTML principal
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

## Ressources et sources

### Transport en Île-de-France
- [Île-de-France Mobilités](https://prim.iledefrance-mobilites.fr/) - API officielle pour les horaires de transport en région Île-de-France

### API Météorologique
- [Open-Meteo API](https://open-meteo.com/en/docs/meteofrance-api) - API météorologique gratuite utilisée pour les prévisions
  - Modèle : Météo-France Seamless
  - Documentation des paramètres utilisés dans le projet

### Icônes et Emojis Météo
- [Google Weather Icons](https://github.com/mrdarrengriffin/google-weather-icons) - Ensemble d'icônes météo utilisées dans l'interface
- [WMO Weather Code Reference](https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c) - Référentiel des codes météo WMO utilisés pour mapper les conditions météorologiques aux icônes appropriées

## Licence

Ce projet est libre d'utilisation.

## Remerciements

- API RER fournie par [Île-de-France Mobilités](https://prim.iledefrance-mobilites.fr/)
- Données météorologiques par [Open-Meteo](https://open-meteo.com/)
- Icônes météo par [Google Weather Icons](https://github.com/mrdarrengriffin/google-weather-icons)
- Codes météo WMO par [stellasphere](https://gist.github.com/stellasphere)
- Conçu pour fonctionner sur Raspberry Pi

# Configuration pour NextRER

# URL de l'API Île-de-France Mobilités
RATP_API_URL = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"
# URL de l'API Open-Meteo
OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"


# Station
STATION_ID = "53783" # Chatou-Croissy

DIRECTIONS = {
    "main":  {
        "platform" : ["1"],
        "quayRef" : ["STIF:StopPoint:Q:473964:"],
        "directionNames" : ["Paris", "Boissy-Saint-Léger", "Marne-la-Vallée - Chessy"],
        "directionCodes": ["STIF:StopArea:SP:43094:", "STIF:StopArea:SP:43239:"],
    },
    "secondary":  {
        "platform" : ["2"],
        "quayRef" : ["STIF:StopPoint:Q:473965:"],
        "directionNames" : ["St-Germain-en-Laye"],
        "directionCodes": ["STIF:StopArea:SP:43198:"],
    }
}

# Noms de stations pour affichage
STATION_NAMES = {
    "53783": "Chatou-Croissy",
    # Ajouter d'autres stations ici
}

# Info météo
WEATHER_INFO = {
    "latitude": 48.8898,
    "longitude": 2.1586,
}
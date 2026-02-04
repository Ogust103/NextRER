# Configuration pour NextRER

# URL de l'API Île-de-France Mobilités
API_URL = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"

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

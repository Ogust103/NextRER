from flask import Flask, render_template, jsonify, request
from flask_livereload import LiveReload
import requests
from dotenv import load_dotenv
import os
from config import RATP_API_URL, STATION_ID, DIRECTIONS, OPEN_METEO_API_URL, WEATHER_INFO

# Charger les variables d'environnement depuis .env
load_dotenv()

class NextRer:
    def __init__(self, destinationName, destinationCode, vehicleJourneyName, vehicleAtStop, expectedArrivalTime, expectedDepartureTime, aimedArrivalTime, aimedDepartureTime, platform, quayRef):
        self.destinationName = destinationName
        self.destinationCode = destinationCode
        self.vehicleJourneyName = vehicleJourneyName
        self.vehicleAtStop = vehicleAtStop
        self.expectedArrivalTime = expectedArrivalTime
        self.expectedDepartureTime = expectedDepartureTime
        self.aimedArrivalTime = aimedArrivalTime
        self.aimedDepartureTime = aimedDepartureTime
        self.platform = platform
        self.quayRef = quayRef

    def __repr__(self):
        return f"NextRer(destinationName={self.destinationName}, vehicleJourneyName={self.vehicleJourneyName}, vehicleAtStop={self.vehicleAtStop}, expectedArrivalTime={self.expectedArrivalTime}, expectedDepartureTime={self.expectedDepartureTime}, aimedArrivalTime={self.aimedArrivalTime}, aimedDepartureTime={self.aimedDepartureTime})"
        
def fetch_next_rers():    
    try:
        url = f"{RATP_API_URL}?MonitoringRef=STIF:StopArea:SP:{STATION_ID}:"
        headers = {"apikey": os.getenv("API_KEY")}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        useful_data = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']

        next_rers = []
        for rer in useful_data:
            try:
                rerInfo = rer['MonitoredVehicleJourney']
                rerMonitored = rerInfo['MonitoredCall']
                next_rer = NextRer(
                    destinationName=rerInfo.get('DestinationName', [{"value": "Unknown destination"}])[0].get("value", "Unknown destination"),
                    destinationCode=rerInfo.get('DestinationRef', {}).get('value', "Unknown code"),
                    vehicleJourneyName=rerInfo.get('VehicleJourneyName', [{"value": "N/A"}])[0].get("value", "N/A"),
                    vehicleAtStop=rerMonitored.get('VehicleAtStop', False),
                    expectedArrivalTime=rerMonitored.get('ExpectedArrivalTime', rerMonitored.get('AimedArrivalTime', '')),
                    expectedDepartureTime=rerMonitored.get('ExpectedDepartureTime', rerMonitored.get('AimedDepartureTime', '')),
                    aimedArrivalTime=rerMonitored.get('AimedArrivalTime', ''),
                    aimedDepartureTime=rerMonitored.get('AimedDepartureTime', ''),
                    platform=rerMonitored.get('DeparturePlatformName', {}).get('value', 'N/A'),
                    quayRef=rerMonitored.get('DepartureStopAssignment', {}).get('ExpectedQuayRef', {}).get('value') if rerMonitored.get('DepartureStopAssignment') else None,
                )
                next_rers.append(next_rer)
            except (KeyError, TypeError, IndexError) as e:
                print(f"Error processing RER: {e}")
                continue
        
        return next_rers
    except requests.exceptions.Timeout:
        print("Timeout connecting to RATP API")
        return []
    except requests.exceptions.RequestException as e:
        print(f"RATP API request error: {e}")
        return []
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error processing RATP data: {e}")
        return []

def fetch_weather():
    try:
        params = {
            "latitude": WEATHER_INFO["latitude"],
            "longitude": WEATHER_INFO["longitude"],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "sunrise",
                "sunset",
                "weather_code"
            ],
            "hourly": [
                "temperature_2m",
                # "precipitation",
                # "rain",
                # "snowfall",
                # "cloud_cover",
                "is_day",
                "weather_code"
            ],
            "models": "meteofrance_seamless",
            "current": [
                "temperature_2m",
                # "precipitation",
                # "cloud_cover",
                # "rain",
                # "showers",
                # "snowfall",
                "is_day",
                "weather_code"
            ],
            "timezone": "Europe/Paris",
            "forecast_days": 3,
        }
        response = requests.get(OPEN_METEO_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        meteo_prevision = {
            "current": {},
            "daily": {},
            "hourly": {}
        }
        
        # Traitement des données actuelles avec gestion d'erreurs
        try:
            meteo_prevision["current"] = {
                "temperature": data.get('current', {}).get('temperature_2m', 0),
                # "precipitation": data.get('current', {}).get('precipitation', 0),            
                # "cloud_cover": data.get('current', {}).get('cloud_cover', 0),
                # "rain": data.get('current', {}).get('rain', 0),
                # "showers": data.get('current', {}).get('showers', 0),
                # "snowfall": data.get('current', {}).get('snowfall', 0),
                "is_day": data.get('current', {}).get('is_day', 0),
                "weather_code": data.get('current', {}).get('weather_code', 0),
            }
        except (KeyError, TypeError):
            print("Error processing current weather data")
            meteo_prevision["current"] = {}

        # Traitement des données quotidiennes
        try:
            daily_times = data.get('daily', {}).get('time', [])
            for i in range(len(daily_times)):
                date = daily_times[i]
                meteo_prevision['daily'][date] = {
                    "temperature_max": data['daily']['temperature_2m_max'][i],
                    "temperature_min": data['daily']['temperature_2m_min'][i],
                    "sunrise": data['daily']['sunrise'][i],
                    "sunset": data['daily']['sunset'][i],
                    "weather_code": data['daily']['weather_code'][i],
                }
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error processing daily weather data: {e}")

        # Traitement des données horaires
        try:
            hourly_times = data.get('hourly', {}).get('time', [])
            for i in range(len(hourly_times)):
                time = hourly_times[i]
                meteo_prevision['hourly'][time] = {
                    "temperature": data['hourly']['temperature_2m'][i],
                    # "precipitation": data['hourly']['precipitation'][i],
                    # "rain": data['hourly']['rain'][i],
                    # "snowfall": data['hourly']['snowfall'][i],
                    # "cloud_cover": data['hourly']['cloud_cover'][i],
                    "is_day": data['hourly']['is_day'][i],
                    "weather_code": data['hourly']['weather_code'][i],
                }
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error processing hourly weather data: {e}")
        
        return meteo_prevision
    except requests.exceptions.Timeout:
        print("Timeout connecting to Open-Meteo API")
        return {"current": {}, "daily": {}, "hourly": {}}
    except requests.exceptions.RequestException as e:
        print(f"Open-Meteo API request error: {e}")
        return {"current": {}, "daily": {}, "hourly": {}}
    except (KeyError, TypeError, ValueError) as e:
        print(f"Error processing weather data: {e}")
        return {"current": {}, "daily": {}, "hourly": {}}

app = Flask(__name__)
app.config['DEBUG'] = True
livereload = LiveReload(app)

@app.route("/api/next_rers")
def get_next_rers():
    try:
        next_rers = fetch_next_rers()
        next_rers_dict = [rer.__dict__ for rer in next_rers]
        return jsonify(next_rers_dict), 200
    except Exception as e:
        print(f"Error fetching RER data: {e}")
        return jsonify({"error": "Error fetching RER data", "details": str(e)}), 500

@app.route("/api/weather")
def get_weather():
    try:
        weather = fetch_weather()
        return jsonify(weather), 200
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return jsonify({"error": "Error fetching weather data", "details": str(e)}), 500

@app.route("/")
def home():
    return render_template("index.html", directions=DIRECTIONS)

if __name__ == "__main__":
    app.run(debug=True)

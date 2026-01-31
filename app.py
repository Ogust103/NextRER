from flask import Flask, render_template, jsonify, request
import requests
from dotenv import load_dotenv
import os
from config import STATION_ID, API_URL, PLATFORM_DIRECTIONS

# Charger les variables d'environnement depuis .env
load_dotenv()

class NextRer:
    def __init__(self, destinationName, vehicleJourneyName, vehicleAtStop, expectedArrivalTime, expectedDepartureTime, aimedArrivalTime, aimedDepartureTime, platform):
        self.destinationName = destinationName
        self.vehicleJourneyName = vehicleJourneyName
        self.vehicleAtStop = vehicleAtStop
        self.expectedArrivalTime = expectedArrivalTime
        self.expectedDepartureTime = expectedDepartureTime
        self.aimedArrivalTime = aimedArrivalTime
        self.aimedDepartureTime = aimedDepartureTime
        self.platform = platform

    def __repr__(self):
        return f"NextRer(destinationName={self.destinationName}, vehicleJourneyName={self.vehicleJourneyName}, vehicleAtStop={self.vehicleAtStop}, expectedArrivalTime={self.expectedArrivalTime}, expectedDepartureTime={self.expectedDepartureTime}, aimedArrivalTime={self.aimedArrivalTime}, aimedDepartureTime={self.aimedDepartureTime})"
        
def fetch_next_rers():    
    url = f"{API_URL}?MonitoringRef=STIF:StopArea:SP:{STATION_ID}:"
    headers = {"apikey": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    useful_data = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']

    next_rers = []
    for rer in useful_data:
        rerInfo = rer['MonitoredVehicleJourney']
        rerMonitored = rerInfo['MonitoredCall']
        next_rer = NextRer(
            destinationName=rerInfo['DestinationName'][0]["value"],
            vehicleJourneyName=rerInfo['VehicleJourneyName'][0]["value"],
            vehicleAtStop=rerMonitored['VehicleAtStop'],
            expectedArrivalTime=rerMonitored['ExpectedArrivalTime'],
            expectedDepartureTime=rerMonitored['ExpectedDepartureTime'],
            aimedArrivalTime=rerMonitored['AimedArrivalTime'],
            aimedDepartureTime=rerMonitored['AimedDepartureTime'],
            platform=rerMonitored['DeparturePlatformName']['value'],
        )
        next_rers.append(next_rer)
    
    return next_rers


app = Flask(__name__)

@app.route("/api/next_rers")
def get_next_rers():
    next_rers = fetch_next_rers()

    next_rers_dict = [rer.__dict__ for rer in next_rers]
    return jsonify(next_rers_dict)

@app.route("/")
def home():
    return render_template("index.html", platform_directions=PLATFORM_DIRECTIONS)

if __name__ == "__main__":
    app.run(debug=True)

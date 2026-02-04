from flask import Flask, render_template, jsonify, request
from flask_livereload import LiveReload
import requests
from dotenv import load_dotenv
import os
from config import STATION_ID, API_URL, DIRECTIONS

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
            destinationCode=rerInfo['DestinationRef']['value'],
            vehicleJourneyName=rerInfo['VehicleJourneyName'][0]["value"],
            vehicleAtStop=rerMonitored['VehicleAtStop'],
            expectedArrivalTime=rerMonitored['ExpectedArrivalTime'],
            expectedDepartureTime=rerMonitored['ExpectedDepartureTime'],
            aimedArrivalTime=rerMonitored['AimedArrivalTime'],
            aimedDepartureTime=rerMonitored['AimedDepartureTime'],
            platform=rerMonitored['DeparturePlatformName']['value'],
            quayRef=rerMonitored['DepartureStopAssignment']['ExpectedQuayRef']['value'] if 'DepartureStopAssignment' in rerMonitored else None,
        )
        next_rers.append(next_rer)
    
    return next_rers


app = Flask(__name__)
app.config['DEBUG'] = True
livereload = LiveReload(app)

@app.route("/api/next_rers")
def get_next_rers():
    next_rers = fetch_next_rers()

    next_rers_dict = [rer.__dict__ for rer in next_rers]
    return jsonify(next_rers_dict)

@app.route("/")
def home():
    return render_template("index.html", directions=DIRECTIONS)

if __name__ == "__main__":
    app.run(debug=True)

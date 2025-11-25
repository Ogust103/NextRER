from flask import Flask, render_template, jsonify
import requests

class NextRer:
    def __init__(self, destinationName, vehicleJourneyName, vehicleAtStop, expectedArrivalTime, expectedDepartureTime, aimedArrivalTime, aimedDepartureTime):
        self.destinationName = destinationName
        self.vehicleJourneyName = vehicleJourneyName
        self.vehicleAtStop = vehicleAtStop
        self.expectedArrivalTime = expectedArrivalTime
        self.expectedDepartureTime = expectedDepartureTime
        self.aimedArrivalTime = aimedArrivalTime
        self.aimedDepartureTime = aimedDepartureTime

    def __repr__(self):
        return f"NextRer(destinationName={self.destinationName}, vehicleJourneyName={self.vehicleJourneyName}, vehicleAtStop={self.vehicleAtStop}, expectedArrivalTime={self.expectedArrivalTime}, expectedDepartureTime={self.expectedDepartureTime}, aimedArrivalTime={self.aimedArrivalTime}, aimedDepartureTime={self.aimedDepartureTime})"
        
def fetch_next_rers(station_id="473964", api_key="TBvQ8qqqyjExp6GFdR9IBaONxbLUL8K0"):
    url = f"https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF:StopPoint:Q:{station_id}:"
    headers = {"apikey": api_key}
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
            aimedDepartureTime=rerMonitored['AimedDepartureTime']
        )
        next_rers.append(next_rer)
    
    return next_rers



app = Flask(__name__)

@app.route("/api/next_rers")
def get_next_rers():
    station_id = "473922"
    api_key = "TBvQ8qqqyjExp6GFdR9IBaONxbLUL8K0"
    next_rers = fetch_next_rers(station_id, api_key)

    next_rers_dict = [rer.__dict__ for rer in next_rers]
    return jsonify(next_rers_dict)

@app.route("/")
def home():
    nextRers = fetch_next_rers()
    return render_template("index.html", nextRers=nextRers)

if __name__ == "__main__":
    app.run(debug=True)

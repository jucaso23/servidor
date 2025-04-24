from flask import Flask, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

from cargar_credenciales import cargar_credenciales_firebase
cred = cargar_credenciales_firebase()

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gpsrastrear-default-rtdb.firebaseio.com/'
})

GOOGLE_API_KEY = 'AIzaSyBS_dZkX--0zxab4Gv4J2JzhBp1auFQSIA'

@app.route('/ubicacion', methods=['POST'])
def obtener_ubicacion():
    try:
        data = request.json

        # 🚀 Si recibimos datos GPS directamente
        if "lat" in data and "lng" in data:
            print(f"[GPS] Lat: {data['lat']}, Lng: {data['lng']}")
            ref = db.reference('GPS/ubicaciones/ultima')
            ref.set({
                'lat': data['lat'],
                'lng': data['lng'],
                'accuracy': 5  # Asumimos buena precisión GPS
            })
            return jsonify({"status": "GPS data saved"}), 200

        # 🌐 Si recibimos datos WPS (WiFi)
        elif "wifiAccessPoints" in data:
            google_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}'
            google_response = requests.post(google_url, json={
                "wifiAccessPoints": data["wifiAccessPoints"]
            })

            geo = google_response.json()
            lat = geo["location"]["lat"]
            lng = geo["location"]["lng"]
            accuracy = geo.get("accuracy")

            print(f"[WPS] Lat: {lat}, Lng: {lng}, Accuracy: {accuracy}m")

            ref = db.reference('/GPS/ubicaciones/ultima')
            ref.set({
                'lat': lat,
                'lng': lng,
                'accuracy': accuracy
            })

            return jsonify({"lat": lat, "lng": lng, "accuracy": accuracy}), 200

        else:
            return jsonify({"error": "Datos no válidos"}), 400

    except Exception as e:
        print("[✘] Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



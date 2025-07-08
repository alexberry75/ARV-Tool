from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

RAPIDAPI_KEY = "40a5b86b02msh1873ae2efb2df19p19a161jsn415c1952d48c"
ZILLOW_API_HOST = "zillow-com1.p.rapidapi.com"

@app.route('/')
def home():
    return "ARV Tool is running!"

@app.route('/arv', methods=['POST'])
def arv():
    data = request.get_json()
    address = data.get("address")
    print("📩 Received address:", address)

    # Step 1: Get property info
    res = requests.get(
        "https://zillow-com1.p.rapidapi.com/property",
        headers={...},
        params={"address": address}
    )
    print("📡 Property API Status:", res.status_code)
    print("🧾 Property Response:", res.text)

    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch property data"}), 500

    prop = res.json()
    zpid = prop.get("zpid")
    print("🏷 ZPID:", zpid)

    # Step 2: Get comps
    comps_res = requests.get(
        "https://zillow-com1.p.rapidapi.com/similar-properties",
        headers={...},
        params={"zpid": zpid}
    )
    print("📡 Comps API Status:", comps_res.status_code)
    print("🧾 Comps Response:", comps_res.text)


{
  "address": "1600 Pennsylvania Ave NW, Washington, DC 20500"
}


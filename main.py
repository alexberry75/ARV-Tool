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
    if not address:
        return jsonify({"error": "Address is required."}), 400

    # Get property info
    res = requests.get(
        "https://zillow-com1.p.rapidapi.com/property",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": ZILLOW_API_HOST
        },
        params={"address": address}
    )
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch property data"}), 500

    prop = res.json()
    zpid = prop.get("zpid")
    sqft = prop.get("livingArea", 2000)

    comps_res = requests.get(
        "https://zillow-com1.p.rapidapi.com/similar-properties",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": ZILLOW_API_HOST
        },
        params={"zpid": zpid}
    )

    if comps_res.status_code != 200:
        return jsonify({"error": "Failed to fetch comps"}), 500

    comps = comps_res.json().get("comps", [])[:5]
    total_ppsqft = 0
    used = []
    for comp in comps:
        price = comp.get("price")
        area = comp.get("livingArea")
        if price and area:
            ppsqft = price / area
            total_ppsqft += ppsqft
            used.append({
                "address": comp.get("address", {}).get("streetAddress", "N/A"),
                "price": price,
                "sqft": area,
                "ppsqft": round(ppsqft, 2)
            })

    if not used:
        return jsonify({"error": "No valid comps found"}), 404

    avg_ppsqft = total_ppsqft / len(used)
    arv_estimate = round(avg_ppsqft * sqft, 2)

    return jsonify({
        "input_address": address,
        "estimated_arv": arv_estimate,
        "price_per_sqft": round(avg_ppsqft, 2),
        "subject_sqft": sqft,
        "comps_used": used
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

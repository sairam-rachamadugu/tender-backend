from flask import Flask, jsonify
import json
import os

from scrapper import scrape_and_save
app = Flask(__name__)

@app.route("/tenders", methods=["GET"])
def get_tenders():
    with open("docs/data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)
@app.route("/")
def hello():
    print("[INFO] home route")
    return "Flask API is running!"
@app.route("/refresh")
def refresh():
    try:
        scrape_and_save()
        return jsonify({"message": "Scraping completed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run( host="0.0.0.0", port=port)

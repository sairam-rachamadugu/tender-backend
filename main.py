from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/tenders", methods=["GET"])
def get_tenders():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)
@app.route("/")
def hello():
    return "Flask API is running!"

if __name__ == "__main__":
    app.run()

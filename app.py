from flask import Flask, request, jsonify
from utils.predict import safe_predict

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    result = safe_predict(data)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request

from service.predictor import Predictor


predictor = Predictor()
app = Flask(__name__)


@app.route('/', methods=['POST'])
def predict():
    payload = request.json
    out = predictor.predict(payload)
    return out


@app.route('/healthcheck', methods=['GET'])
def predict():
    if predictor.healthcheck:
        return {"True", "ok"}
    return {"False", 400}

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route("/score", methods=["POST"])
def score():
    features = request.json["X"]
    response = make_response(jsonify({"score": features}))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

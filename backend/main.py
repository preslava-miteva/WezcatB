from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
    print("hey")
    return jsonify({'message':'Heeyy'}), 200



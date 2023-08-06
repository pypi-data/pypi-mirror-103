from flask import Flask, jsonify
from flask_cors import CORS
from DisplayHelper import system, cec
from waitress import serve

app = Flask(__name__)
CORS(app)
app.config["CEC"] = cec.CEC()

@app.route('/systemInfo')
def system_info():
    return jsonify(system.load_system_properties()), 200

@app.route('/tv/status')
def tv_status():
    return jsonify(app.config["CEC"].get_state()), 200

@app.route("/tv/on")
def tv_on():
    return jsonify(app.config["CEC"].on()), 200

@app.route("/tv/off")
def tv_off():
    return jsonify(app.config["CEC"].off()), 200

@app.route('/')
def index():
    return jsonify({"status": "online"}), 200

def main():
    # app.run(host='127.0.0.1', port=5000)
    serve(app, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()

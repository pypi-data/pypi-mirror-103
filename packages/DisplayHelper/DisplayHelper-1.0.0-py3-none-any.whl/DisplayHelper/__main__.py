from flask import Flask
from DisplayHelper import system, cec
from waitress import serve

app = Flask(__name__)
app.config["CEC"] = cec.CEC()

@app.route('/systemInfo')
def system_info():
    return system.load_system_properties()

@app.route('/tv/status')
def tv_status():
    return app.config["CEC"].get_state()

@app.route("/tv/on")
def tv_on():
    return app.config["CEC"].on()

@app.route("/tv/off")
def tv_off():
    return app.config["CEC"].off()

@app.route('/')
def index():
    return {"status": "online"}

def main():
    # app.run(host='127.0.0.1', port=5000)
    serve(app, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()

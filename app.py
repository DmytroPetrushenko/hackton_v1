from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
system_running = False
logs = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    global system_running, logs
    if not system_running:
        system_running = True
        logs.append("System started.")
        return jsonify({"status": "Running"})
    return jsonify({"status": "Already running"})


@app.route('/stop', methods=['POST'])
def stop():
    global system_running, logs
    if system_running:
        system_running = False
        logs.append("System stopped.")
        return jsonify({"status": "Stopped"})
    return jsonify({"status": "Already stopped"})


@app.route('/logs', methods=['GET'])
def get_logs():
    global logs
    return jsonify({"logs": logs[-50:]})


if __name__ == '__main__':
    app.run(debug=True)

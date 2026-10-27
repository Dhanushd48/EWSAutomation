from flask import Flask, request, render_template
import threading

from Utilities.driver_store import drivers
from Utilities.user_context import set_user_ip
from main import main

app = Flask(__name__)

# Global log storage
user_logs = {}
job_status = {}


@app.route("/")
def home():
    return render_template("index.html")

def run_automation(params, logs, user_ip):
    set_user_ip(user_ip)

    try:

        main(
            **params,
            logs=logs
        )

        job_status[user_ip] = "COMPLETED"

    except Exception as e:

        print(e)

        if 'Connection aborted' in str(e):
            logs.append("Execution Stopped By User")
        else:
            logs.append(
                "ERROR: Runtime error. Please refresh and resubmit"
            )

        job_status[user_ip] = "COMPLETED"


@app.route("/run", methods=["POST"])
def run():

    user_ip = request.remote_addr

    logs = []
    user_logs[user_ip] = logs
    job_status[user_ip] = "RUNNING"

    params = {
        "choice": int(request.form["choice"]),
        "printer_ip": request.form["printer_ip"],
        "password": request.form["password"],
        "domain": request.form.get("domain", ""),
        "ip1": request.form.get("ip1", ""),
        "fax_number": request.form.get("fax_number", ""),
        "old_password": request.form.get("old_password", ""),
        "new_password": request.form.get("new_password", "")
    }

    threading.Thread(
        target=run_automation,
        args=(params, logs, user_ip),
        daemon=True
    ).start()

    return render_template("logs.html")


@app.route("/logs")
def get_logs():

    user_ip = request.remote_addr

    return "".join(
        user_logs.get(user_ip, [])
    )


@app.route("/status")
def get_status():

    user_ip = request.remote_addr

    return job_status.get(
        user_ip,
        "RUNNING"
    )

@app.route("/stop", methods=["POST"])
def stop():
    user_ip = request.remote_addr

    user_logs[user_ip].append(
        "Execution stopped by user."
    )

    job_status[user_ip] = "COMPLETED"

    driver = drivers.get(user_ip)

    if driver:
        try:
            driver.quit()
        except:
            pass

    return "Stopped"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=6767,
        threaded=True,
        debug=True
    )
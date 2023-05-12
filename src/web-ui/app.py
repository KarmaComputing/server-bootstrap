import os
import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)

ip_address = os.getenv("IP_ADDRESS", "192.168.0.120")
username = os.getenv("IDRAC_USERNAME", "root")
password = os.getenv("IDRAC_PASSWORD", "calvin")

IDRAC_SCRIPTS_BASE_PATH = os.getenv("IDRAC_SCRIPTS_BASE_PATH", "./iDRAC-Redfish-Scripting/Redfish\ Python/")


@app.route("/")
def index():
    return render_template("index.html")


def execute_redfish_command(action):
    if action == 'GetPowerState':
        breakpoint()
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {ip_address} -u {username} -p {password} --get"
        result = subprocess.run(command, capture_output=True, shell=True)
    if action == 'ChangeBiosBootOrderREDFISH':
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}ChangeBiosBootOrderREDFISH.py -ip {ip_address} -u {username} -p {password} --get"
        result = subprocess.run(command, capture_output=True, shell=True)

    else:
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {ip_address} -u {username} -p {password} --set {action}"
        result = subprocess.run(command, capture_output=True, shell=True)
    return (
        jsonify(
            {
                "output": result.stdout.decode("utf-8"),
                "error": result.stderr.decode("utf-8"),
            }
        ),
        result.returncode,
    )


@app.route("/api/v1/On", methods=["POST"])
def set_power_on():
    return execute_redfish_command("On")


@app.route("/api/v1/GracefulShutdown", methods=["POST"])
def set_power_graceful_shutdown():
    return execute_redfish_command("GracefulShutdown")

@app.route("/api/v1/GetPowerState", methods=["POST"])
def get_power_state():
    return execute_redfish_command("GetPowerState")

@app.route("/api/v1/ChangeBiosBootOrderREDFISH", methods=["POST"])
def get_bios_boot_order():
    return execute_redfish_command("ChangeBiosBootOrderREDFISH")


if __name__ == "__main__":
    app.run()

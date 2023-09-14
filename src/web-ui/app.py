import os
import subprocess
from flask import Flask, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

ip_address = os.getenv("IP_ADDRESS", "192.168.0.120")
username = os.getenv("IDRAC_USERNAME", "root")
password = os.getenv("IDRAC_PASSWORD", "calvin")

IDRAC_SCRIPTS_BASE_PATH = os.getenv(
    "IDRAC_SCRIPTS_BASE_PATH", "./iDRAC-Redfish-Scripting/Redfish Python/"
)


@app.route("/")
def index():
    return render_template("index.html")


def execute_redfish_command(action):
    if action == "ForceRestart":
        url = f"https://{ip_address}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
        headers = {"Content-Type": "application/json"}
        payload = {"ResetType": "ForceRestart"}
        auth = (username, password)

        req = requests.post(
            url, headers=headers, json=payload, auth=auth, verify=False
        )  # noqa: E501
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "MountiPXE":
        command = (
            f'curl -v -H "Content-Type: application/json" -X POST -u {username}:{password} '
            f"-k https://{ip_address}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia "
            f'-d \'{{"Image": "http://138.201.59.208/sites/default/files/ipxe.iso"}}\''
        )

        # URL
        url = f"https://{ip_address}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia"

        # Headers
        headers = {"Content-Type": "application/json"}

        # Data
        data = {"Image": "http://138.201.59.208/sites/default/files/ipxe.iso"}

        # Making the request
        req = requests.post(
            url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "UnMountiPXE":

        # URL
        url = f"https://{ip_address}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia"

        # Headers
        headers = {"Content-Type": "application/json"}

        # Data
        data = {}

        # Making the request
        req = requests.post(
            url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "SetOnetimeBootValueVirtualCD":

        # URL
        url = f"https://{ip_address}/redfish/v1/Systems/System.Embedded.1"

        # Headers
        headers = {"Content-Type": "application/json"}

        # Data
        data = {"Boot": {"BootSourceOverrideTarget": "None"}}

        # Making the request
        req = requests.patch(
            url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "GetOnetimeBootValue":

        # URL
        url = f"https://{ip_address}/redfish/v1/Systems/System.Embedded.1"

        # Making the request
        req = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "GetPowerState":
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {ip_address} -u {username} -p {password} --get"  # noqa: E501
        result = subprocess.run(command, capture_output=True, shell=True)
    if action == "ChangeBiosBootOrderREDFISH":
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}ChangeBiosBootOrderREDFISH.py -ip {ip_address} -u {username} -p {password} --get"  # noqa: E501
        result = subprocess.run(command, capture_output=True, shell=True)

    if action == "On":
        # URL
        url = f"https://{ip_address}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"

        # Headers
        headers = {"Content-Type": "application/json"}

        # Data
        data = {"ResetType": "On"}

        # Making the request
        req = requests.post(
            url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    if action == "ForceOff":
        # URL
        url = f"https://{ip_address}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"

        # Headers
        headers = {"Content-Type": "application/json"}

        # Data
        data = {"ResetType": "ForceOff"}

        # Making the request
        req = requests.post(
            url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return (
            jsonify(
                {
                    "output": req.text,
                    "error": req.text,
                }
            ),
            req.status_code,
        )

    else:
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {ip_address} -u {username} -p {password} --set {action}"  # noqa: E501
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


@app.route("/api/v1/ForceOff", methods=["POST"])
def set_power_off():
    return execute_redfish_command("ForceOff")


@app.route("/api/v1/ForceRestart", methods=["POST"])
def force_restart():
    return execute_redfish_command("ForceRestart")


@app.route("/api/v1/GracefulShutdown", methods=["POST"])
def set_power_graceful_shutdown():
    return execute_redfish_command("GracefulShutdown")


@app.route("/api/v1/GetPowerState", methods=["POST"])
def get_power_state():
    return execute_redfish_command("GetPowerState")


@app.route("/api/v1/ChangeBiosBootOrderREDFISH", methods=["POST"])
def get_bios_boot_order():
    return execute_redfish_command("ChangeBiosBootOrderREDFISH")


@app.route("/api/v1/MountiPXE", methods=["POST"])
def mount_iPXE_iso():
    return execute_redfish_command("MountiPXE")


@app.route("/api/v1/UnmountISO", methods=["POST"])
def unmount_iPXE_iso():
    return execute_redfish_command("UnMountiPXE")


@app.route("/api/v1/GetOnetimeBootValue", methods=["POST"])
def get_current_onetime_boot_order():
    return execute_redfish_command("GetOnetimeBootValue")


@app.route("/api/v1/SetOnetimeBootValueVirtualCD", methods=["POST"])
def get_boot_from_virtual_cd():
    return execute_redfish_command("SetOnetimeBootValueVirtualCD")


if __name__ == "__main__":
    app.run()

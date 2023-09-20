import os
import subprocess
from flask import Flask, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth
from types import SimpleNamespace

app = Flask(__name__)

idrac_host = os.getenv("IDRAC_HOST", "192.168.0.120")
username = os.getenv("IDRAC_USERNAME", "root")
password = os.getenv("IDRAC_PASSWORD", "calvin")
playwright_working_dir = os.getenv("PLAYWRIGHT_WORKING_DIR", "../playwright-boostrap/")  # noqa: E501
PWDEBUG = os.getenv("PWDEBUG", False)
playwright_headed = "--headed" if "PWDEBUG" in os.environ else ''

IDRAC_SCRIPTS_BASE_PATH = os.getenv(
    "IDRAC_SCRIPTS_BASE_PATH", "./iDRAC-Redfish-Scripting/Redfish Python/"
)


def api_response(req):
    error = None
    if req.status_code not in range(200, 299):
        error = req.text
    return jsonify({"output": req.text, "error": error}), req.status_code


@app.route("/")
def index():
    return render_template("index.html")


def execute_redfish_command(action):
    if action == "Bootstrap":
        VerifyiDRACAccess()
        ForceOff()
        sleepSecconds = 10
        print(f"Sleeping for {sleepSecconds}")
        iDRACSetVirtualTerminalHTML5()
        UnmountISO()
        UnmountISO()
        MountISO()
        MountISO()
        GetPowerState()
        from time import sleep
        sleepSecconds = 10
        print(f"Sleeping for {sleepSecconds}")
        sleep(sleepSecconds)
        return PowerOn()

    if action == "ForceRestart":
        url = f"https://{idrac_host}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"  # noqa: E501
        headers = {"Content-Type": "application/json"}
        payload = {"ResetType": "ForceRestart"}
        auth = (username, password)

        req = requests.post(
            url, headers=headers, json=payload, auth=auth, verify=False
        )  # noqa: E501
        return api_response(req)

    if action == "GetOnetimeBootValue":

        # URL
        url = f"https://{idrac_host}/redfish/v1/Systems/System.Embedded.1"

        # Making the request
        req = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            verify=False,
        )
        return api_response(req)

    if action == "ChangeBiosBootOrderREDFISH":
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}ChangeBiosBootOrderREDFISH.py -ip {idrac_host} -u {username} -p {password} --get"  # noqa: E501
        result = subprocess.run(command, capture_output=True, shell=True)

    else:
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {idrac_host} -u {username} -p {password} --set {action}"  # noqa: E501
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


@app.route("/api/v1/Bootstrap", methods=["POST"])
def bootstrap():
    return execute_redfish_command("Bootstrap")


@app.route("/api/v1/VerifyiDRACAccess", methods=["POST"])
def VerifyiDRACAccess():
    url = f"https://{idrac_host}/redfish/v1/Systems/"
    headers = {"Content-Type": "application/json"}
    payload = {"ResetType": "ForceRestart"}
    auth = (username, password)
    req = requests.get(
        url, headers=headers, json=payload, auth=auth, verify=False
    )  # noqa: E501
    return api_response(req)


@app.route("/api/v1/iDRACSetVirtualTerminalHTML5", methods=["POST"])
def iDRACSetVirtualTerminalHTML5():
    command = (
        f"IDRAC_HOST=http://{idrac_host} IDRAC_USERNAME={username} "
        f"IDRAC_PASSWORD={password} npx playwright test scripts/iDRAC-set-virtual-terminal-html5.spec.ts "  # noqa: E501
        f" {playwright_headed}"
    )
    result = subprocess.run(command, cwd=playwright_working_dir, env=os.environ, capture_output=True, shell=True)  # noqa: E501
    return (
        jsonify(
            {
                "output": result.stdout.decode("utf-8"),
                "error": result.stderr.decode("utf-8"),
            }
        ),
        result.returncode,
    )


@app.route("/api/v1/PowerOn", methods=["POST"])
def PowerOn():
    print("PowerOn")
    # URL
    url = f"https://{idrac_host}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"  # noqa: E501

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
    return api_response(req)


@app.route("/api/v1/ForceOff", methods=["POST"])
def ForceOff():
    print("ForceOff")
    # URL
    url = f"https://{idrac_host}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"  # noqa: E501

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
    return api_response(req)


@app.route("/api/v1/ForceRestart", methods=["POST"])
def force_restart():
    return execute_redfish_command("ForceRestart")


@app.route("/api/v1/GracefulShutdown", methods=["POST"])
def set_power_graceful_shutdown():
    return execute_redfish_command("GracefulShutdown")


@app.route("/api/v1/GetPowerState", methods=["POST"])
def GetPowerState():
    print("GetPowerState")
    # URL
    url = f"https://{idrac_host}/redfish/v1/Systems/System.Embedded.1"

    # Making the request
    req = requests.get(
        url,
        auth=HTTPBasicAuth(username, password),
        verify=False,
    )
    if req.status_code == 200:
        response_text = (
            f"Current server power state: {req.json()['PowerState']}"  # noqa: E501
        )
        req = SimpleNamespace()
        req.status_code = 200
        req.text = response_text
    return api_response(req)


@app.route("/api/v1/ChangeBiosBootOrderREDFISH", methods=["POST"])
def get_bios_boot_order():
    return execute_redfish_command("ChangeBiosBootOrderREDFISH")


@app.route("/api/v1/MountISO", methods=["POST"])
def MountISO():
    print("MountISO")
    # URL
    url = f"https://{idrac_host}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia"  # noqa: E501

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

    if req.status_code == '500':
        try:
            message = req.json()['error']['@Message.ExtendedInfo'][0]['Message']  # noqa: E501
            if message == "The Virtual Media image server is already connected.":  # noqa: E501
                print("The Virtual Media image server is already connected.")
            else:
                breakpoint()
        except Exception as e:
            print(e)

    return api_response(req)

@app.route("/api/v1/UnmountISO", methods=["POST"])
def UnmountISO():
    print(UnmountISO)
    # URL
    url = f"https://{idrac_host}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia"  # noqa: E501

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
    return api_response(req)


@app.route("/api/v1/GetOnetimeBootValue", methods=["POST"])
def get_current_onetime_boot_order():
    return execute_redfish_command("GetOnetimeBootValue")


if __name__ == "__main__":
    app.run()

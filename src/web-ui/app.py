import os
import subprocess
from flask import jsonify, render_template, request, session
from apiflask import APIFlask
import requests
from requests.auth import HTTPBasicAuth
from types import SimpleNamespace

app = APIFlask(__name__)
app.config.update(TESTING=True, SECRET_KEY=os.getenv("SECRET_KEY"))
IDRAC_HOST = None  # noqa: F841
IDRAC_USERNAME = None  # noqa: F841
IDRAC_PASSWORD = None  # noqa: F841

playwright_working_dir = os.getenv(
    "PLAYWRIGHT_WORKING_DIR", "../playwright-boostrap/"
)  # noqa: E501
PWDEBUG = os.getenv("PWDEBUG", False)
playwright_headed = "--headed" if "PWDEBUG" in os.environ else ""

IDRAC_SCRIPTS_BASE_PATH = os.getenv(
    "IDRAC_SCRIPTS_BASE_PATH", "./iDRAC-Redfish-Scripting/Redfish Python/"
)

session_requests = requests.Session()
session_requests.verify = False


def api_response(req):
    error = None
    if req.status_code not in range(200, 299):
        error = req.text
    return jsonify({"output": req.text, "error": error}), req.status_code


def api_call(path=None, method=None, payload=None):
    breakpoint()
    assert method is not None
    url = f"https://{session.get('IDRAC_HOST')}/redfish/v1/{path}"
    authHeaders = HTTPBasicAuth(
        session.get("IDRAC_USERNAME"), session.get("IDRAC_PASSWORD")
    )  # noqa: E501

    # Making the request
    if method == "GET":
        req = requests.get(
            url,
            auth=authHeaders,
            verify=False,
        )
    elif method == "POST":
        req = requests.post(
            url,
            auth=authHeaders,
            verify=False,
            json=payload,
            headers={"Content-Type": "application/json"},
        )

    return req


@app.before_request
def load_idrac_settings():
    """
    Load settings in following order of presidence:
    - environment variable
    - session variable (from url GET paramenter)
    - default fallback

    """
    settings = ["IDRAC_HOST", "IDRAC_USERNAME", "IDRAC_PASSWORD"]

    for setting in settings:
        # Default setting to None (meaning unset)
        exec(f"{setting}=None")
        # Check if setting is set in environment variable
        if os.getenv(setting, None):
            exec(f"{setting}={os.getenv(setting)}")
        # Check if setting is set in url get parameter
        if request.args.get(setting, None):
            session[setting] = request.args.get(setting)
        exec(f"{setting}='{request.args.get(setting)}'")

    breakpoint()


@app.context_processor
def inject_settings():
    return dict(IDRAC_HOST=os.getenv("IDRAC_HOST"))


@app.route("/")
def index():
    load_idrac_settings()
    return render_template("index.html")


@app.route("/wipefs")
def wipefs():
    """Wipe the entire server"""
    # Power off server
    # Mount & Boot into fedora live CD (there must be a better way...)
    # SSH into server
    # Run 'wip-all-disks.sh'
    #  See https://github.com/KarmaComputing/server-bootstrap/blob/d9faddb3138d4ddb733dd9890d35a7c1296cdee7/src/playbooks/scripts/wipe-all-disks.sh#L1 # noqa: E501

    return {"message": "Server has been wiped"}


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
        url = f"https://{IDRAC_HOST}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"  # noqa: E501
        headers = {"Content-Type": "application/json"}
        payload = {"ResetType": "ForceRestart"}
        auth = (IDRAC_USERNAME, IDRAC_PASSWORD)

        req = requests.post(
            url, headers=headers, json=payload, auth=auth, verify=False
        )  # noqa: E501
        return api_response(req)

    if action == "GetOnetimeBootValue":
        # URL
        url = f"https://{IDRAC_HOST}/redfish/v1/Systems/System.Embedded.1"

        # Making the request
        req = requests.get(
            url,
            auth=HTTPBasicAuth(IDRAC_USERNAME, IDRAC_PASSWORD),
            verify=False,
        )
        return api_response(req)

    if action == "ChangeBiosBootOrderREDFISH":
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}ChangeBiosBootOrderREDFISH.py -ip {IDRAC_HOST} -u {IDRAC_USERNAME} -p {IDRAC_PASSWORD} --get"  # noqa: E501
        result = subprocess.run(command, capture_output=True, shell=True)

    else:
        command = f"python {IDRAC_SCRIPTS_BASE_PATH}GetSetPowerStateREDFISH.py -ip {IDRAC_HOST} -u {IDRAC_USERNAME} -p {IDRAC_PASSWORD} --set {action}"  # noqa: E501
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
    url = f"https://{IDRAC_HOST}/redfish/v1/Systems/"
    headers = {"Content-Type": "application/json"}
    payload = {"ResetType": "ForceRestart"}
    auth = (IDRAC_USERNAME, IDRAC_PASSWORD)
    req = requests.get(
        url, headers=headers, json=payload, auth=auth, verify=False
    )  # noqa: E501
    return api_response(req)


@app.route("/api/v1/ResetiDRAC", methods=["POST"])
def ResetiDRAC():
    return api_response("Not implemented")


@app.route("/api/v1/iDRACSetVirtualTerminalHTML5", methods=["POST"])
def iDRACSetVirtualTerminalHTML5():
    command = (
        f"IDRAC_HOST=http://{IDRAC_HOST} IDRAC_USERNAME={IDRAC_USERNAME} "
        f"IDRAC_PASSWORD={IDRAC_PASSWORD} npx playwright test scripts/iDRAC-set-virtual-terminal-html5.spec.ts "  # noqa: E501
        f" {playwright_headed}"
    )
    result = subprocess.run(
        command,
        cwd=playwright_working_dir,
        env=os.environ,
        capture_output=True,
        shell=True,
    )  # noqa: E501
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
    breakpoint()
    data = {"ResetType": "On"}
    req = api_call(
        path="Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        method="POST",  # noqa: E501
        payload=data,
    )

    return api_response(req)


@app.route("/api/v1/ForceOff", methods=["POST"])
@app.route("/api/v1/PowerOff", methods=["POST"])
def ForceOff():
    print("ForceOff")
    # URL
    url = f"https://{IDRAC_HOST}/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"  # noqa: E501

    # Headers
    headers = {"Content-Type": "application/json"}

    # Data
    data = {"ResetType": "ForceOff"}

    # Making the request
    req = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(IDRAC_USERNAME, IDRAC_PASSWORD),
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
    req = api_call(path="Systems/System.Embedded.1")

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
    url = f"https://{IDRAC_HOST}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia"  # noqa: E501

    # Headers
    headers = {"Content-Type": "application/json"}

    # Data
    data = {"Image": "http://138.201.59.208/sites/default/files/ipxe.iso"}

    # Making the request
    req = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(IDRAC_USERNAME, IDRAC_PASSWORD),
        verify=False,
    )

    if req.status_code == "500":
        try:
            message = req.json()["error"]["@Message.ExtendedInfo"][0][
                "Message"
            ]  # noqa: E501
            if (
                message
                == "The Virtual Media image server is already connected."  # noqa: E501
            ):  # noqa: E501
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
    url = f"https://{IDRAC_HOST}/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia"  # noqa: E501

    # Headers
    headers = {"Content-Type": "application/json"}

    # Data
    data = {}

    # Making the request
    req = requests.post(
        url,
        headers=headers,
        json=data,
        auth=HTTPBasicAuth(IDRAC_USERNAME, IDRAC_PASSWORD),
        verify=False,
    )
    return api_response(req)


@app.route("/api/v1/GetOnetimeBootValue", methods=["POST"])
def get_current_onetime_boot_order():
    return execute_redfish_command("GetOnetimeBootValue")

import os
import subprocess
from flask import jsonify, render_template, request, session
from apiflask import APIFlask
import requests
from requests.auth import HTTPBasicAuth
import json
from time import sleep
import platform

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

HOST_HEALTHCHECK_POLL_IP = os.getenv("HOST_HEALTHCHECK_POLL_IP")

session_requests = requests.Session()
session_requests.verify = False


def api_response(req):
    return (
        jsonify({"resp": req.text, "status_code": req.status_code}),
        req.status_code,
    )


def api_call(path=None, method=None, payload=None, raw_payload=False):
    assert method is not None
    url = f"https://{os.getenv('IDRAC_HOST')}/redfish/v1/{path}"
    authHeaders = HTTPBasicAuth(
        os.getenv("IDRAC_USERNAME"), os.getenv("IDRAC_PASSWORD")
    )  # noqa: E501

    # Making the request
    if method == "GET":
        req = requests.get(
            url,
            auth=authHeaders,
            verify=False,
        )
    elif method == "POST":
        if raw_payload:
            req = requests.post(
                url,
                auth=authHeaders,
                verify=False,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
        else:
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


def PollPingHostOSOnline(
    ip=HOST_HEALTHCHECK_POLL_IP, interval=1, max_attempts=35
):  # noqa: E501
    """ "
    Keep polling max_attempts until host os responds
    """

    def ping(ip):
        """
        Ping the IP address to check for a response.
        Returns True if the IP is reachable, False otherwise.
        """
        # Determine the ping command based on the operating system
        ping_command = (
            "ping -c 1 " + ip
            if platform.system().lower() != "windows"
            else "ping -n 1 " + ip
        )

        # Execute the ping command and check the response
        response = os.system(ping_command)

        return response == 0  # Return True if ping was successful

    print(f"Polling IP address {ip}...")

    attempt = 0
    while attempt < max_attempts:
        if ping(ip):
            print(f"IP address {ip} is now reachable.")
            return True

        attempt += 1
        print(
            f"Attempt {attempt}/{max_attempts}: "
            "No response from {ip}. "
            "Retrying in {interval} seconds..."
        )
        sleep(interval)

    print(
        f"Reached maximum attempts ({max_attempts}). "
        "IP address {ip} is not reachable."
    )
    return False


def justKeepRedeploying(max_repeated_deploys=-1, delayBetweenRedeploy=10):
    print("Starting justKeepRedeploying")

    execute_redfish_command("Bootstrap")
    deploy_count = 0

    while deploy_count < max_repeated_deploys or max_repeated_deploys == -1:
        print(f"Deployment #{deploy_count + 1}")
        print(f"Sleeping for {delayBetweenRedeploy} seconds")
        sleep(delayBetweenRedeploy)

        execute_redfish_command("Bootstrap")

        deploy_count += 1
        if max_repeated_deploys != -1 and deploy_count >= max_repeated_deploys:
            break

    print("Deployment loop finished")


def execute_redfish_command(action):
    if action == "Bootstrap":
        VerifyiDRACAccess()
        ForceOff()
        sleepSecconds = 15
        print(f"Sleeping for {sleepSecconds}")
        sleep(sleepSecconds)
        # iDRACSetVirtualTerminalHTML5()
        UnmountISO()
        MountISO()
        SetBootFromVirtualMedia()
        GetPowerState()
        sleepSecconds = 10
        print(f"Sleeping for {sleepSecconds}")
        sleep(sleepSecconds)
        PowerOn()
        # Setup host disks
        # Run install
        # HealthCheckBootedHost
        return PollPingHostOSOnline()

    if action == "ForceRestart":
        payload = {"ResetType": "ForceRestart"}
        req = api_call(
            path="Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
            method="POST",
            payload=payload,
        )
        return api_response(req)

    if action == "GetOnetimeBootValue":
        req = api_call(path="Systems/System.Embedded.1", method="GET")
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


def VerifyiDRACAccess():
    req = api_call(path="Systems/", method="GET")
    return req


@app.route("/api/v1/VerifyiDRACAccess", methods=["POST"])
def route_VerifyiDRACAccess():
    req = VerifyiDRACAccess()
    return api_response(req)


@app.route("/api/v1/ResetiDRAC", methods=["POST"])
def ResetiDRAC():
    return api_response("Not implemented")


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


@app.route("/api/v1/iDRACSetVirtualTerminalHTML5", methods=["POST"])
def route_iDRACSetVirtualTerminalHTML5():
    resp = iDRACSetVirtualTerminalHTML5()
    return resp


def PowerOn():
    print("PowerOn")
    print("Ensuring PowerState is 'Off' before attempting power On")
    req = GetPowerState()
    power_state = req.json()["PowerState"]
    if power_state != "Off":
        print(f"PowerState is currently {power_state}")
        Exception(
            "PowerState is not 'Off' "
            f"(it's {power_state}). Refusing to Power on"  # noqa: E501
        )
    data = {"ResetType": "On"}
    req = api_call(
        path="Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        method="POST",  # noqa: E501
        payload=data,
    )
    return req


@app.route("/api/v1/PowerOn", methods=["POST"])
def route_PowerOn():
    req = PowerOn()
    return api_response(req)


def PowerOff():
    print("Power OFF (GracefulShutdown)")
    data = {"ResetType": "GracefulShutdown"}
    req = api_call(
        path="Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        method="POST",  # noqa: E501
        payload=data,
    )
    return req


def ForceOff():
    print("ForceOff")
    req = GetPowerState()
    power_state = req.json()["PowerState"]
    if power_state != "On":
        print(f"PowerState is currently {power_state}")
        Exception(f"PowerState is {power_state}. Refusing to Power off")
    data = {"ResetType": "ForceOff"}

    req = api_call(
        path="Systems/System.Embedded.1/Actions/ComputerSystem.Reset",
        method="POST",  # noqa: E501
        payload=data,
    )
    return req


@app.route("/api/v1/ForceOff", methods=["POST"])
@app.route("/api/v1/PowerOff", methods=["POST"])
def route_ForceOff():
    req = ForceOff()
    return api_response(req)


@app.route("/api/v1/ForceRestart", methods=["POST"])
def force_restart():
    return execute_redfish_command("ForceRestart")


@app.route("/api/v1/GracefulShutdown", methods=["POST"])
def set_power_graceful_shutdown():
    return execute_redfish_command("GracefulShutdown")


def GetPowerState():
    print("GetPowerState")
    req = api_call(path="Systems/System.Embedded.1", method="GET")

    if req.status_code == 200:
        power_state = req.json().get("PowerState")
        print(f"PowerState is {power_state}")
    return req


@app.route("/api/v1/GetPowerState", methods=["POST"])
def route_GetPowerState():
    req = GetPowerState()
    return api_response(req)


@app.route("/api/v1/ChangeBiosBootOrderREDFISH", methods=["POST"])
def get_bios_boot_order():
    return execute_redfish_command("ChangeBiosBootOrderREDFISH")


def MountISO():
    print("MountISO")
    data = {"Image": "http://138.201.59.208/sites/default/files/ipxe.iso"}
    req = api_call(
        path="Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.InsertMedia",  # noqa: E501
        method="POST",  # noqa: E501
        payload=data,
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
                print(f"req.status_code: {req.status_code}")
                pass
        except Exception as e:
            print(e)
    elif req.status_code == 204:
        print("http 204 No Content successful - (ISO mounted)")
    return req


@app.route("/api/v1/MountISO", methods=["POST"])
def route_MountISO():
    req = MountISO()
    return api_response(req)


def UnmountISO():
    print(UnmountISO)
    req = api_call(
        path="Managers/iDRAC.Embedded.1/VirtualMedia/CD/Actions/VirtualMedia.EjectMedia",  # noqa: E501
        method="POST",
        payload={},
    )
    return req


@app.route("/api/v1/UnmountISO", methods=["POST"])
def route_UnmountISO():
    req = UnmountISO()
    return api_response(req)


def SetBootFromVirtualMedia():
    payload = {
        "ShareParameters": {"Target": "ALL"},
        "ImportBuffer": '<SystemConfiguration><Component FQDD="iDRAC.Embedded.1"><Attribute Name="ServerBoot.1#BootOnce">Enabled</Attribute><Attribute Name="ServerBoot.1#FirstBootDevice">VCD-DVD</Attribute></Component></SystemConfiguration>',  # noqa: E501
    }

    req = api_call(
        path="Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration",  # noqa: E501
        method="POST",
        payload=json.dumps(payload),
        raw_payload=True,
    )
    if req.status_code == 202:
        print("HTTP 202 Accepted - Boot device set/setting to VirtualMedia")
    return req


@app.route("/api/v1/SetBootFromVirtualMedia", methods=["POST"])
def route_SetBootFromVirtualMedia():
    req = SetBootFromVirtualMedia()
    return api_response(req)


@app.route("/api/v1/GetOnetimeBootValue", methods=["POST"])
def get_current_onetime_boot_order():
    return execute_redfish_command("GetOnetimeBootValue")

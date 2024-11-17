import os
import subprocess
from flask import jsonify, render_template, request, session
from apiflask import APIFlask
import requests
from requests.auth import HTTPBasicAuth
import json
from time import sleep
import platform
from settings import load_settings
from tenacity import retry, wait_exponential, before_log, stop_after_attempt
import logging
import sys
import time
from functools import wraps


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger(__name__)


app = APIFlask(__name__)
app.config.update(TESTING=True, SECRET_KEY=os.getenv("SECRET_KEY"))
settings = load_settings()
IDRAC_HOST = None  # noqa: F841
IDRAC_USERNAME = None  # noqa: F841
IDRAC_PASSWORD = None  # noqa: F841
HOST_HEALTHCHECK_POLL_IP = None
DEFAULT_HTTP_REQ_TIMEOUT = os.getenv("DEFAULT_HTTP_REQ_TIMEOUT", 60)
IDRAC_HTTP_REQ_TIMEOUT = os.getenv("IDRAC_HTTP_REQ_TIMEOUT", 15)
IDRAC_SLEEP_AFTER_RESET_REQUEST_REQ = os.getenv(
    "IDRAC_SLEEP_AFTER_RESET_REQUEST_REQ", 3
)

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


def countdown(seconds):
    log.info(f"Sleeping for {seconds} seconds")
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rTime left: {remaining} seconds")
        sys.stdout.flush()
        time.sleep(1)
    # Clear the line after countdown ends
    sys.stdout.write("\rCountdown finished!\n")


def ConnectToVPN():
    """
    Attempt to connect to VPN
    Assumptions:
    - Any existing VPN connection will be torn down
    - Credentials for VPN will be fetched using secret(s)
      required to fetch them
    - VPN tunnel (wireguard) will be started
    """
    log.info(
        "Tear down any existing VPN connection "
        "(assumes wg-quick is used for WireGuard"
    )
    subprocess.run(["wg-quick", "down", "wg0"], check=False)

    log.info("Download the psonoci tool")
    subprocess.run(
        [
            "curl",
            "https://get.psono.com/psono/psono-ci/x86_64-linux/psonoci",
            "--output",
            "./psonoci",
        ],
        check=True,
    )

    log.info("Mark psonoci as executable")
    subprocess.run(["chmod", "+x", "./psonoci"], check=True)

    # Fetch credentials using the psonoci tool
    PSONO_CI_VPN_SECRET_NOTE_ID = settings.get(
        "PSONO_CI_VPN_SECRET_NOTE_ID"
    ).value  # noqa: E501

    try:
        os.environ["PSONO_CI_API_KEY_ID"] = settings.get(
            "PSONO_CI_API_KEY_ID"
        ).value  # noqa: E501
        os.environ["PSONO_CI_API_SECRET_KEY_HEX"] = settings.get(
            "PSONO_CI_API_SECRET_KEY_HEX"
        ).value
        os.environ["PSONO_CI_SERVER_URL"] = settings.get(
            "PSONO_CI_SERVER_URL"
        ).value  # noqa: E501
        result = subprocess.run(
            [
                "./psonoci",
                "secret",
                "get",
                PSONO_CI_VPN_SECRET_NOTE_ID,
                "notes",
            ],  # noqa: E501
            check=True,
            capture_output=True,
            text=True,
            env=os.environ,
        )
        log.info(result)
    except Exception as e:
        log.error(e)

    vpn_config = result.stdout.strip()

    log.debug("Write the VPN configuration to /etc/wireguard/wg0.conf")
    with open("/etc/wireguard/wg0.conf", "w") as vpn_file:
        vpn_file.write(vpn_config)

    try:
        log.debug("Start the VPN tunnel")
        sleep(3)
        subprocess.run(["wg-quick", "up", "wg0"], check=False)
        print("VPN connected successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing a command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def recover_from_error_vpn_not_active(retry_state):
    """Attempt to recover from error VPN
    not active.
    """
    log.debug(retry_state)
    ConnectToVPN()


@retry(
    wait=wait_exponential(multiplier=1, min=5, max=10),
    before=before_log(log, logging.DEBUG),
    stop=stop_after_attempt(4),
    retry_error_callback=recover_from_error_vpn_not_active,
)
def vpn_must_be_up(f):
    """
    Checks for a route to the IDRAC_HOST
    The/a valid VPN connection
    must be up for the majority of the server
    bootstrap process to work.

    If the VPN is *up*, then the IDRAC_HOST
    will be reachable (there will be a route to
    that host/IP).
    If the VPN is *down* then the IDRAC_HOST will
    likely be 'no route to host'.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        log.info("Calling wrapper vpn_must_be_up")
        try:
            url = f"https://{settings.get('IDRAC_HOST')}/start.html"
            log.info(f"Contacting: {url}")
            requests.get(url, verify=False, timeout=DEFAULT_HTTP_REQ_TIMEOUT)
        except Exception as e:
            log.error(f"Verify VPN connection is up & functioning. {e}")
            log.debug("Attempting reconnect of VPN")
            ConnectToVPN()
        return f(*args, **kwds)

    return wrapper


def api_response(req):
    try:
        resp = req.json()
    except Exception:
        resp = req.text
    return (
        jsonify({"resp": resp, "status_code": req.status_code}),
        req.status_code,
    )


def api_call(
    path=None, method=None, payload=None, raw_payload=False, timeout=60
):  # noqa: E501
    assert method is not None
    if "redfish" not in path and "http" not in path:
        url = f"https://{os.getenv('IDRAC_HOST')}/redfish/v1/{path}"
    if "redfish" in path:
        url = f"https://{os.getenv('IDRAC_HOST')}/{path}"
    authHeaders = HTTPBasicAuth(
        os.getenv("IDRAC_USERNAME"), os.getenv("IDRAC_PASSWORD")
    )  # noqa: E501

    # Making the request
    if method == "GET":
        req = requests.get(
            url,
            auth=authHeaders,
            verify=False,
            timeout=timeout,  # noqa: E501
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
    elif method == "PATCH":
        req = requests.patch(
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
            exec(f"{setting}='{os.getenv(setting)}'")
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
            f"No response from {ip}. "
            f"Retrying in {interval} seconds..."
        )
        sleep(interval)

    print(
        f"Reached maximum attempts ({max_attempts}). "
        "IP address {ip} is not reachable."
    )
    return False


def justKeepRedeploying(max_repeated_deploys=-1, delayBetweenRedeploy=180):
    print("Starting justKeepRedeploying")

    execute_redfish_command("Bootstrap")
    deploy_count = 0

    while deploy_count < max_repeated_deploys or max_repeated_deploys == -1:
        print(f"Deployment #{deploy_count + 1}")
        countdown(delayBetweenRedeploy)

        execute_redfish_command("Bootstrap")

        deploy_count += 1
        if max_repeated_deploys != -1 and deploy_count >= max_repeated_deploys:
            break

    print("Deployment loop finished")


def execute_redfish_command(action, redfish_uri=None):
    if action == "Bootstrap":
        VerifyVPNAccess()
        VerifyiDRACAccess()
        ForceOff()
        sleepSecconds = 15
        countdown(sleepSecconds)
        # iDRACSetVirtualTerminalHTML5()
        UnmountISO()
        MountISO()
        SetBootFromVirtualMedia()
        GetPowerState()
        sleepSecconds = 10
        countdown(sleepSecconds)
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

    if action == "RawRequest":
        req = api_call(
            path=redfish_uri,
            method="GET",
        )
        return req
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


@vpn_must_be_up
def VerifyVPNAccess():
    pass


# NOTE "max" does not think what you may think it
# means - you probably want "stop_after_attempt"
# See:
# https://tenacity.readthedocs.io/en/latest/index.html?highlight=max_attempts
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=20),
    before=before_log(log, logging.DEBUG),
    stop=stop_after_attempt(20),
)
@vpn_must_be_up
def VerifyiDRACAccess():
    try:
        req = api_call(
            path="Systems/", method="GET", timeout=IDRAC_HTTP_REQ_TIMEOUT
        )  # noqa: E501
        if req.status_code == 200:
            log.info(f"iDRACAccess is OK. Got status code {req.status_code}")
        if req.status_code == 401:
            msg = f"VerifyiDRACAccess returned 401 {req.text}"
            log.error(msg)
            raise Exception(msg)

    except requests.exceptions.ConnectionError as e:
        log.error(f"Connection error occurred: {e}")
        raise
    except requests.exceptions.RequestException as e:
        log.error(f"An HTTP error occurred: {e}")
        raise
    return req


@app.route("/api/v1/VerifyiDRACAccess", methods=["POST"])
def route_VerifyiDRACAccess():
    req = VerifyiDRACAccess()
    return api_response(req)


def ResetiDRAC():
    """
    Soft reset the iDRAC.
    Since Dell iDRACs can easily get into a 'bad' state
    the iDRAC reset often overcomes these bad states.

    For example, mounting virual media, even after unmounting
    media and terminating sessions can leave the iDRAC is a
    'operations busy' state with no way to mount new media.

    Dell documents this behaviour as:
    "Sometimes, iDRAC may become unresponsive due to various reasons."
    https://www.dell.com/support/kbdoc/en-uk/000126703/how-to-reset-the-internal-dell-remote-access-controller-idrac-on-a-poweredge-server

    See also Rigor: https://oxide.computer/principles

    """
    print("ResetiDRAC")
    data = {"ResetType": "GracefulRestart"}
    req = api_call(
        path="Managers/iDRAC.Embedded.1/Actions/Manager.Reset/",
        method="POST",  # noqa: E501
        payload=data,
    )
    msg = (
        f"Sleeping {IDRAC_SLEEP_AFTER_RESET_REQUEST_REQ} "
        "secconds to give iDRAC time to commence the reset "
        "without sleeping, subsequent iDRAC api request may appear to "
        "succeed before the iDRAC actually starts performing it's reset, "
        "causing confusing.\n"
        "Note this sleep has nothing to do with verifying the iDRAC has "
        "completed it's reset. For that, calls to VerifyiDRACAccess may be "
        "made."
    )
    log.info(msg)
    sleep(IDRAC_SLEEP_AFTER_RESET_REQUEST_REQ)
    return req


@app.route("/api/v1/ResetiDRAC", methods=["POST"])
def route_ResetiDRAC():
    req = ResetiDRAC()
    return req


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


@vpn_must_be_up
def GetPowerState():
    print("GetPowerState")
    req = api_call(path="Systems/System.Embedded.1", method="GET")
    req.raise_for_status()
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


@vpn_must_be_up
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
                log.error(f"req.status_code: {req.status_code}")
                log.error(
                    "Performing ResetiDRAC to attempt VirtualMedia state fix"
                )  # noqa: E501
                ResetiDRAC()
                VerifyiDRACAccess()
        except Exception as e:
            print(e)
    elif req.status_code == 204:
        print("http 204 No Content successful - (ISO mounted)")
    return req


@app.route("/api/v1/MountISO", methods=["POST"])
def route_MountISO():
    req = MountISO()
    return api_response(req)


@vpn_must_be_up
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


@vpn_must_be_up
def EnableHostWatchdogTimer():
    req = api_call(
        path="/redfish/v1/Systems/System.Embedded.1",  # noqa: E501
        method="PATCH",
        payload={"HostWatchdogTimer": {"FunctionEnabled": True}},
    )
    return req


@app.route("/api/v1/EnableHostWatchdogTimer", methods=["POST"])
def route_EnableHostWatchdogTimer():
    req = EnableHostWatchdogTimer()
    return api_response(req)


@vpn_must_be_up
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


@vpn_must_be_up
def RawRequest(redfish_uri: str):
    """
    Pass any valid Redfish api url and the response is returned
    e.g.
    https://192.168.1.1/redfish/v1/Systems/System.Embedded.1?$select=BootProgress/LastState

    """
    return execute_redfish_command("RawRequest", redfish_uri=redfish_uri)


@app.route("/api/v1/RawRequest", methods=["POST"])
def route_RawRequest():
    redfish_uri = request.json.get("data")
    req = RawRequest(redfish_uri)
    return api_response(req)

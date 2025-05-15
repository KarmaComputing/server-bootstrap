# Performing an action
import sys
import redfish

# When running remotely connect using the address, account name,
# and password to send https requests
login_host = "http://192.168.0.230"
login_account = "Administrator"
login_password = "A0F7HKUU"

## Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host, \
                                     username=login_account, \
                                     password=login_password, default_prefix='/redfish/v1/')

# Login into the server and create a session
REDFISH_OBJ.login(auth="basic")

# Do a GET on a given path
#


# Print out the response


# Logout of the current session
# REDFISH_OBJ.logout()

def togglePower():
    body = dict()
    body["ResetType"] = "PushPowerButton"
    response = REDFISH_OBJ.post("/redfish/v1/systems/1/Actions/ComputerSystem.Reset/", body=body)
    sys.stdout.write("%s\n" % response.text)

def forceOff():
    body = dict()
    body["ResetType"] = "ForceOff"
    response = REDFISH_OBJ.post("/redfish/v1/systems/1/Actions/ComputerSystem.Reset/", body=body)
    sys.stdout.write("%s\n" % response.text)

def getStatus():
    response = REDFISH_OBJ.get("/redfish/v1/Systems/1")
    sys.stdout.write(response.json().get("PowerState"))
    sys.stdout.write("%s\n" % response.text)

def getPowerStatus():
    response = REDFISH_OBJ.post("/api/v1/GetPowerState/Systems/1")
    sys.stdout.write("%s\n" % response.text)

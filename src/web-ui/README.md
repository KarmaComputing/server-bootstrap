# Setup

- (dependency) Clone https://github.com/dell/iDRAC-Redfish-Scripting

Install
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

# Run
```
./run.sh
```

# Running from shell
```
source ../../venv/bin/activate
sudo -E env PATH=$PATH python  # See https://askubuntu.com/a/1342154
```
```

# Visit

http://127.0.0.1:5000/

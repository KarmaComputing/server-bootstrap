# VPN Client

Setup/deploy a IPsec VPN tunnel client on Ubuntu server

## Configure
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Run

- Update inventory

```
python3 -m venv venv
. venv/bin/activate
ansible-playbook --ask-vault-pass -i inventory.ini playbooks/deploy-vpn-client.yml
```

## Verify

```
# on the server
curl -v -k -L --compressed https://10.100.49.2
```

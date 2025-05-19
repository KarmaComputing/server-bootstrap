# Table of Contents

[API Docs](api/README.md)

# Example Command for Debugging

```sh
URL=https://192.168.0.230 USERNAME=Administrator PASSWORD=A0F7HKUU VALIDCERT=false WIPEINTERVAL=300 go run .
```

# Logical Flow

![diagram](docs/diagram.drawio.png)

# How to Use This

1. Ensure appropriate `build/build.sh` configs
  - Building ipxe.iso image
    - Use new/existing iPXE config file in `build/ipxe/input`
    - Input its name as FILE variable in `build/build.sh`
  - Building alpine-netboot image
    - TBD
  - ssh-keys
    - Place intended public SSH key into `build/ssh-key`
2. `cd build && bash ./build.sh`
  - ipxe.iso and alpine image will be ready in `www`
3. `podman compose up -d`
  - apache web server will expose `www` at port 8080

# Bazinga

```
 ____            _                   
| __ )  __ _ ___(_)_ __   __ _  __ _ 
|  _ \ / _` |_  / | '_ \ / _` |/ _` |
| |_) | (_| |/ /| | | | | (_| | (_| |
|____/ \__,_/___|_|_| |_|\__, |\__,_|
                        |___/       
```
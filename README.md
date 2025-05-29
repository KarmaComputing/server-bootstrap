# Overview

![diagram](docs/diagram.drawio.png)


## TOC

- [Alpine Mirroring](./deploy/alpine-mirror/README.md)



## Run for debugging

- In `internal/runner`

    ```sh
    URL=https://192.168.0.230 USERNAME=Administrator PASSWORD=A0F7HKUU VALIDCERT=false WIPEINTERVAL=300 go run .
    ```

## Full deploy

1. Build
  - Building ipxe.iso image
    - Use new/existing iPXE config file in `deploy/build/ipxe/scripts`
    - Input its name as FILE variable in `deploy/scripts/build-ipxe-iso.sh`
    - Run `deploy/scripts/build-ipxe-iso.sh`
    - `ipxe.iso` is placed in `deploy/serve/www`
  - Building alpine-netboot image
    - Run `deploy/scripts/build-alpine.sh`
    - Files are placed in `deploy/serve/www/iso`
  - SSH keys
    - An SSH keypair is automatically generated upon building an `ipxe.iso` image with the above command
      - The **private** key is placed at `deploy/ssh/key`
      - The **public** key is placed at `deploy/serve/www/ssh/key.pub`
    - Up **re**building the `ipxe.iso`, the script will prompt to replace these keys or not

2. Run stack
  - Ensure the files are correctly placed from step 1
  - `podman compose up -d` in repository root

3. !! VM FOR TESTING !!
  - Ensure `qemu` is installed and runnable
  - Ensure web server is accessible at whatever address is defined in the iPXE boot script
  - `qemu-system-x86_64 -cdrom <ipxe.iso> -net nic -net user,hostfwd=tcp::2223-:22 -m 3072 -smp $(nproc)`
  - VM can be accessed over SSH at `localhost:2223`
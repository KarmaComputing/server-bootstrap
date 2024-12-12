# v0.0.117 (Thu Dec 12 2024)

#### ⚠️ Pushed to `main`

- Update release.yml add issues: write permission ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.116 (Thu Dec 12 2024)

#### 🐛 Bug Fix

- Fix #23 build UEFI iPXE image [#24](https://github.com/KarmaComputing/server-bootstrap/pull/24) ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### ⚠️ Pushed to `main`

- Update release.yml add mtools ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.115 (Thu Nov 28 2024)

#### ⚠️ Pushed to `main`

- Update deploy-vpn-server.yml disable automated tmate debugging ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.114 (Sun Nov 24 2024)

#### ⚠️ Pushed to `main`

- Create feature_request.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.113 (Sun Nov 24 2024)

#### 🐛 Bug Fix

- wip update servers playbook to fedora [#8](https://github.com/KarmaComputing/server-bootstrap/pull/8) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #16 cron rotate wireguard vpn user config every 2 hrs [#17](https://github.com/KarmaComputing/server-bootstrap/pull/17) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #16 remove uneeded inputs.PSONO_SECRET_ID from workflow rotate-wireguard-vpn-user-configs.yml [#17](https://github.com/KarmaComputing/server-bootstrap/pull/17) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #16 update WIREGUARD_VPN_PSONO_SECRET_IDS group_vars/all [#17](https://github.com/KarmaComputing/server-bootstrap/pull/17) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip Fix #16 continually bootstrap vpn users [#17](https://github.com/KarmaComputing/server-bootstrap/pull/17) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 update manual readme steps [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 ensure ansible-galaxy collection install --requirements-file ./src/vpn/requirements.yml [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 use checkout v4 [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip Fix #14 automatically rebuild vpn servers [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip #14 deploy-vpn-server.yml improve [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 added localhost.yml group_vars [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip #14 create/rebuild vpn server [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip #14 naming vpn_clients -> vpn_servers [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- rename/mv folder vpn-client -> src/vpn [#15](https://github.com/KarmaComputing/server-bootstrap/pull/15) ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### ⚠️ Pushed to `main`

- Update release.yml bump ipxe iso artifact action to v4 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 build & publish zfs netbook image every 2 hrs build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #13 apk install zfs in servers play ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip #13 pin to alpine v3.20 rather than edge ([@chrisjsimpson](https://github.com/chrisjsimpson))
- build-alpine-netboot-image-zfs.yml can pass branch name ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 bump webfactory/ssh-agent@v0.9.0 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 bump actions to v4 for build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 correct path scp netboot image to boot server ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 stick to naming alpine-zfsnetboot.tar.gz ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 exact path in workflow to publish alpine-zfsnetboot-patched-init.tar.gz ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #20 use settings.py properly ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 update comments patch-alpine-netboot-image-with-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #20 tidy up init netboot patching tar between runs ([@chrisjsimpson](https://github.com/chrisjsimpson))
- WIP Fix #18 As operator I can continually boostrap physical server ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #13 DEFAULT_HTTP_REQ_TIMEOUT to 20 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #13 wip add bootstap-server.sh helper script ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #13 template minimal /etc/network/interfaces during bootstrap (interfaces are already configured with global ips at this point) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- downgrade zfs flags ([@chrisjsimpson](https://github.com/chrisjsimpson))
- ensure ZPOOL_VDEV_NAME_PATH set within chroot environment ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #13 more reliable udev disk identify & ensure packages present ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip fedora ([@chrisjsimpson](https://github.com/chrisjsimpson))
- correct shebang to ash shell for wipe-all-disks ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #13 ensure zfs package installed during play ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #13 more reliable udev disk identify & ensure packages present ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added .gitignore ([@chrisjsimpson](https://github.com/chrisjsimpson))
- add get-first-disk-id.sh create-tank-zpool.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #13 ensure python present on target (alpine) during bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- update requirements.txt ([@chrisjsimpson](https://github.com/chrisjsimpson))
- update servers play description ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added create-tank-zpool.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added install-fedora-root-on-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip update servers playbook to fedora ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added wipe-all-disks.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip #20 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update README.md add Build netboot image bade to readme ([@chrisjsimpson](https://github.com/chrisjsimpson))
- refactor app.py & introduce justKeepRedeploying, HOST_HEALTHCHECK_POLL_IP, PollPingHostOSOnline ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update deploy-vpn-server.yml redeploy every 2->3 hours ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update deploy-vpn-server.yml concurrency 1 prevent concurrent runs #14 #16 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #16 after rebuilding VPN, always rotate & publish user wireguard vpn entries #14 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update README.md add deploy VPN server status badge ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 deploy VPN server every 2 hrs deploy-vpn-server.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 correct ansible-playbook --extra_vars -> --extra-vars ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 ansibleise Add-vpn-user ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 add-vpn-user force collections-path ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 generate-user-vpn-config pip3 install -r src/vpn/requirements.txt ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 only tmate if Update deploy-vpn-server.yml fails ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 Update deploy-vpn-server.yml job name build -> deploy-vpn-server ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 move tmate to last Update deploy-vpn-server.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 update server_bootstrap_private_ssh_key ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 bump runner to ubuntu-24.04 Update deploy-vpn-server.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 Update deploy-vpn-server.yml debug ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 ensure mode 600 for ansible_ssh_private_key_file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 ensure ~/ssh dir exists on local/runner host ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 added missing templates/ssh/ssh_private_key_server_bootstrap.j2 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 don't gather facts on vpn_servers before keys places & put ansible_ssh_private_key_file in all group_vars ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 correct delegate from 127.0.01 -> localhost ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 place ssh_private_key_server_bootstrap and server_bootstrap_public_ssh_key in localhost groupvars ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 template early Template ssh_private_key_server_bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 delegate correctly Template ssh_private_key_server_bootstrap to the runner ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 disable host_key_checking during boostrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 Template ssh_private_key_server_bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 give _vault_hetzner_cloud_token vault secret via cli ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Revert "Ref #14 fix workflow deploy-vpn-server.yml dynamic inventory inventory-vpn-servers-hcloud.yml not needed at that stage (its references via playbook imported later)" ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 fix workflow deploy-vpn-server.yml dynamic inventory inventory-vpn-servers-hcloud.yml not needed at that stage (its references via playbook imported later) ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 debug tmate always ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 force install of hcloud ansible collection ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 remove uneeded vpn_servers from inventory.ini since dynamic inventory ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 add missing pip install -r ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 reinstate use of trap to rm ansible TMPFILE@Q ([@chrisjsimpson](https://github.com/chrisjsimpson))
- remove clunky use of add-mask feature ([@chrisjsimpson](https://github.com/chrisjsimpson))
- #14 debug ansible vault ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 masking inputs ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 masking inputs.ansible_vault_password ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ref #14 remove dead code PSONO_SECRET_ID ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.112 (Sun Apr 07 2024)

#### ⚠️ Pushed to `main`

- bump auto from 10.32.1 -> 11.1.6 ([@chrisjsimpson](https://github.com/chrisjsimpson))
- enable NET_PROTO_IPV6 ipxe ([@chrisjsimpson](https://github.com/chrisjsimpson))
- fix enable NET_PROTO_IPV6 ipxe ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.111 (Sun Nov 12 2023)

#### ⚠️ Pushed to `main`

- set APP_SECRET during web-ui run.sh helper script ([@chrisjsimpson](https://github.com/chrisjsimpson))
- update bootstrap app.py ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.110 (Sat Nov 11 2023)

#### ⚠️ Pushed to `main`

- add SetBootFromVirtualMedia ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- add /api/v1/SetBootFromVirtualMedia ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.109 (Mon Nov 06 2023)

#### ⚠️ Pushed to `main`

- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- poll for server powerstate ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip more generic api call ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.108 (Fri Nov 03 2023)

#### ⚠️ Pushed to `main`

- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- get settings from url params ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.107 (Thu Nov 02 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.106 (Sat Oct 28 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update README.md mermaid web-ui ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update README.md link to web-ui docs ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.105 (Sat Oct 28 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.104 (Sun Sep 24 2023)

#### ⚠️ Pushed to `main`

- update get-first-two-disks-install-openzfs-fedora-root.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.103 (Sun Sep 24 2023)

#### ⚠️ Pushed to `main`

- add get-first-two-disks.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.102 (Sat Sep 23 2023)

#### ⚠️ Pushed to `main`

- add python3 to build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.101 (Sat Sep 23 2023)

#### ⚠️ Pushed to `main`

- Update release.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.100 (Wed Sep 20 2023)

#### ⚠️ Pushed to `main`

- bootstrap step tie all togeather & name tidy ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.99 (Tue Sep 19 2023)

#### ⚠️ Pushed to `main`

- Update release.yml net1->net3 ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.98 (Sat Sep 16 2023)

#### ⚠️ Pushed to `main`

- add api_reponse ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.97 (Fri Sep 15 2023)

:tada: This release contains work from a new contributor! :tada:

Thank you, null[@joeltejeda](https://github.com/joeltejeda), for all your work!

#### ⚠️ Pushed to `main`

- changing add vpn user workflow name vpn_ip_address ([@joeltejeda](https://github.com/joeltejeda))

#### Authors: 1

- [@joeltejeda](https://github.com/joeltejeda)

---

# v0.0.96 (Thu Sep 14 2023)

#### ⚠️ Pushed to `main`

- wip remove dependency on DRAC-Redfish-Scripting ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.95 (Wed Sep 13 2023)

#### ⚠️ Pushed to `main`

- utils iDRAC-login iDRAC-logout ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.94 (Wed Sep 13 2023)

#### ⚠️ Pushed to `main`

- reduce flakeyness of idrag browser automation ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.93 (Sat Sep 09 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.92 (Sat Sep 09 2023)

#### ⚠️ Pushed to `main`

- Update README.md added mermaid diagram how works ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.91 (Fri Sep 08 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.90 (Fri Sep 08 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update patch-alpine-netboot-image-with-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.89 (Fri Sep 08 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.88 (Thu Sep 07 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.87 (Thu Sep 07 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.86 (Thu Sep 07 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))
- mkimg.zfsnetboot.sh Update build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.85 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.84 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-zfs.sh zfs kernel options ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.83 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- zfs kernel module build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.82 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.81 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- scp boot image to boot server ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.80 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.79 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- verify boot server ssh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.78 (Tue Sep 05 2023)

#### ⚠️ Pushed to `main`

- enable zfs kernel module in build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.77 (Tue Sep 05 2023)

#### 🐛 Bug Fix

- Update README.md [#12](https://github.com/KarmaComputing/server-bootstrap/pull/12) ([@jimmyedagawa78](https://github.com/jimmyedagawa78))

#### Authors: 1

- [@jimmyedagawa78](https://github.com/jimmyedagawa78)

---

# v0.0.76 (Mon Sep 04 2023)

#### ⚠️ Pushed to `main`

- dir patch-alpine-netboot-image-with-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.75 (Mon Sep 04 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml Patch alpine image ([@chrisjsimpson](https://github.com/chrisjsimpson))
- add patch-alpine-netboot-image-with-zfs.sh PatchFile-init-ping ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.74 (Sun Sep 03 2023)

#### ⚠️ Pushed to `main`

- re-key vpn_user vpn_pass ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.73 (Sun Sep 03 2023)

#### ⚠️ Pushed to `main`

- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- re-key vpn_clients.yml vault ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.72 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.71 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update add-vpn-user.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.70 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.69 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Publish alpine netboot image artifact ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.68 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Create build-alpine-netboot-image-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.67 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- added build-alpine-netboot-zfs.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.66 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Delete .github/workflows/alpine-netboot-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.65 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.64 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Smoke test wg0 interface by pinging it internally ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.63 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.62 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- port ([@chrisjsimpson](https://github.com/chrisjsimpson))
- set AllowedIPs ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.61 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- use shell for psonocli install ([@chrisjsimpson](https://github.com/chrisjsimpson))
- set owner/mode of save-vpn-credentials-to-password-vault.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.60 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- install psonoci ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.59 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- Update add-vpn-user.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.58 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- added templates/save-vpn-credentials-to-password-vault.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.57 (Sat Sep 02 2023)

#### ⚠️ Pushed to `main`

- template save-vpn-credentials-to-password-vault.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.56 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- save last generated client config to pw manager ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.55 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Generate new vpn peer config & Add save client config to password manager ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.54 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- add Generate new vpn peer config ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.53 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Update add-vpn-user.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.52 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Create add-vpn-user.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.51 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Update add-vpn-user.sh reload wg0 after ([@chrisjsimpson](https://github.com/chrisjsimpson))
- port ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.50 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Update add-vpn-user.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.49 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- dont waste cycles on tmate Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- update add-vpn-user ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.48 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- added add-vpn-user.sh ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.47 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Reload sysctl to apply changes ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.46 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- wg-quick up wg0 ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.45 (Fri Sep 01 2023)

#### ⚠️ Pushed to `main`

- Ensure IP forwarding is enabled permanently ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.44 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.43 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.42 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.41 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.40 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Ensure {{ wireguard_dir }} directory exists Update deploy-vpn-client.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.39 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.38 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- set dns and Ensure {{ wireguard_dir }} directory exists ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.37 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.36 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.35 (Thu Aug 31 2023)

#### 🐛 Bug Fix

- Fix #9 vpn ipsec client ubuntu server [#10](https://github.com/KarmaComputing/server-bootstrap/pull/10) ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.34 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.33 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- Update deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Create deploy-vpn.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.32 (Thu Aug 31 2023)

#### ⚠️ Pushed to `main`

- retry ping until interface up ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.31 (Sat Aug 26 2023)

#### ⚠️ Pushed to `main`

- Create alpine-netboot-zfs.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.30 (Fri Aug 18 2023)

#### ⚠️ Pushed to `main`

- addressing release.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.29 (Fri Aug 18 2023)

#### ⚠️ Pushed to `main`

- remove dhcp ipxe release.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.28 (Tue Aug 15 2023)

#### ⚠️ Pushed to `main`

- Update qemu.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.27 (Tue Aug 15 2023)

#### ⚠️ Pushed to `main`

- Update qemu.yml add bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.26 (Tue Aug 15 2023)

#### ⚠️ Pushed to `main`

- Update qemu.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.25 (Tue Aug 15 2023)

#### ⚠️ Pushed to `main`

- Create qemu.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.24 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Delete test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- remove ipxe-iso.yml because combined in release.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.23 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update .gitignore ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update .autorc ([@chrisjsimpson](https://github.com/chrisjsimpson))
- publish ipxe/src/bin/ipxe.iso with release ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.22 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.21 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.20 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.19 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.18 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.17 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Update ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.16 (Sun Aug 13 2023)

#### ⚠️ Pushed to `main`

- Create ipxe-iso.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.15 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update README.md ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.14 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- https if not enabled ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.13 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- iPXE enable ping command by default ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.12 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added ipxe step by step ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.11 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.10 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.9 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.8 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.7 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.6 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.5 (Sat Aug 05 2023)

#### ⚠️ Pushed to `main`

- Update test.yml install qemu ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.4 (Fri Aug 04 2023)

#### ⚠️ Pushed to `main`

- Update test.yml run qemu-system-x86_64 ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.3 (Fri Aug 04 2023)

#### ⚠️ Pushed to `main`

- Create test.yml qemu ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.2 (Fri May 12 2023)

#### ⚠️ Pushed to `main`

- Update container to enable web console ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

---

# v0.0.1 (Fri May 12 2023)

:tada: This release contains work from a new contributor! :tada:

Thank you, null[@chrisjsimpson](https://github.com/chrisjsimpson), for all your work!

#### ⚠️ Pushed to `main`

- Added deploy.yml file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Added release.yml file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Added deploy.sh file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Added .autorc file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Added amber.yaml secrets file ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Added flask quickstart ([@chrisjsimpson](https://github.com/chrisjsimpson))
- create .docker-compose.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added basic webui ([@chrisjsimpson](https://github.com/chrisjsimpson))
- add idrac boostrap basics ([@chrisjsimpson](https://github.com/chrisjsimpson))
- tidy up action git-auto-issue-branch-creation.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- sanitize branch name creation ([@chrisjsimpson](https://github.com/chrisjsimpson))
- correct actions syntax ([@chrisjsimpson](https://github.com/chrisjsimpson))
- sanitize issue title ([@chrisjsimpson](https://github.com/chrisjsimpson))
- .github/workflows/auto-branches.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- removeo ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Merge branch 'main' of github.com:KarmaComputing/server-bootstrap ([@chrisjsimpson](https://github.com/chrisjsimpson))
- rm workflows ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Create .github/workflows/blank.yml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- Update auto-branches.yaml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- auto branches ([@chrisjsimpson](https://github.com/chrisjsimpson))
- install zfs utils ([@chrisjsimpson](https://github.com/chrisjsimpson))
- wip zfs root setup ([@chrisjsimpson](https://github.com/chrisjsimpson))
- added inital playbook servers.yaml ([@chrisjsimpson](https://github.com/chrisjsimpson))
- update readme ([@chrisjsimpson](https://github.com/chrisjsimpson))
- formatting readme ([@chrisjsimpson](https://github.com/chrisjsimpson))
- initial readme ([@chrisjsimpson](https://github.com/chrisjsimpson))

#### Authors: 1

- [@chrisjsimpson](https://github.com/chrisjsimpson)

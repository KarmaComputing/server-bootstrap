# Setup from blank server

1. iDrac to server for inital user set-up

> The rest will be done via playbook, this manual step is sadly needed to create the inital user (TODO perform via RedfishAPI + playwright see https://blog.karmacomputing.co.uk/devops-with-physical-servers-redfish-python-api-idrac/ and also https://github.com/microsoft/playwright/issues/21786#issuecomment-1481488488)
	set boot device to virtual cd
	launch virtual console
	attach virtual media (debian 11 live cd)
	wait for debian live to load
	create non-root user called debian
	
	Install ssh
	
	```
	apt install openssh-server
	```
	Create debian user (a non-root user)
	```
	adduser debian
	# set password
	```
	
	Add `debian` user to sudo group
	```
	usermod -aG sudo debian
	```
	
	Allow password authentication
	```
	vim /etc/ssh/sshd_config
	# set
	PasswordAuthentication yes
	```
	Restart sshd
	```
	systemctl restart sshd
	```
	
	Exit iDrac and attemp to connect over SSH to debian live running on server from your laptop/server.
	```
	ssh debian@<server-ip> # Not the iDRAC ip, your servers ethernet assigned ip
	```
	> If you don't know the up address of the server, check `ip -c a` and look at the links address(es)
	
	Verify you can become root after SSH'ing into the server.
	e.g.:
	```
	user@laptop ~ $ ssh debian@<ip>
	Warning: Permanently added '<ip>' (ED25519) to the list of known hosts.
	debian@<ip>'s password: 
	Linux debian 5.10.0-20-amd64 #1 SMP Debian 5.10.158-2 (2022-12-13) x86_64

	The programs included with the Debian GNU/Linux system are free software;
	the exact distribution terms for each program are described in the
	individual files in /usr/share/doc/*/copyright.

	Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
	permitted by applicable law.
	Last login: Fri Mar 24 23:49:21 2023 from x
	debian@debian:~$ sudo -i
	[sudo] password for debian: 
	root@debian:~# whoami 
	root
	```
	
2. Run playbook against server
	

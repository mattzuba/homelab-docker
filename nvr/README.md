## NVR Setup Instructions

This folder has all the instructions for settings up Frigate, Double-take and Compreface.  As usual, this is all based on docker containers.

### Server Info

This is run on an older Dell Precision 5300 with an Nvidia Quadro P2000 and a Coral TPU, running Ubuntu 24.04.  There are a few extra steps to get the server running.

Fix console size on a 4k screen

```shell
sed -i 's/FONTSIZE=.*/FONTSIZE="16x32"/g' /etc/default/console-setup
```

Set up some stuff for sudo

```shell
echo '%sudo  ALL=(ALL) NOPASSWD: ALL' | tee /etc/sudoers.d/00-sudo-group
chmod 0660 /etc/sudoers.d/00-sudo-group
```

After initial install, install acpi support and set up some stuff to allow closing the laptop but leaving the machine running.

```shell
echo 'HandleLidSwitch=ignore' | sudo tee -a /etc/systemd/logind.conf
echo 'LidSwitchIgnoreInhibited=no' | sudo tee -a /etc/systemd/logind.conf
cd /tmp
wget http://mirrors.kernel.org/ubuntu/pool/main/a/acpi-support/acpi-support_0.144_amd64.deb
sudo apt install ./acpi-support_0.144_amd64.deb
echo "event=button/lid.*" | sudo tee /etc/acpi/events/lid-button
echo "action=/etc/acpi/lid.sh" | sudo tee -a /etc/acpi/events/lid-button
sudo tee /etc/acpi/lid.sh > /dev/null <<'EOF'
#!/bin/bash

grep -q close /proc/acpi/button/lid/*/state

if [ $? = 0 ]; then
    sleep 0.2 && vbetool dpms off
fi

grep -q open /proc/acpi/button/lid/*/state

if [ $? = 0 ]; then
    vbetool dpms on
fi
EOF
chmod +x /etc/acpi/lid.sh
```

Prep the Coral TPU packages

```shell
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg -o /etc/apt/keyrings/google.asc
sudo chmod a+r /etc/apt/keyrings/google.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/google.asc] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
  sudo tee /etc/apt/sources.list.d/coral.list > /dev/null
sudo apt update
sudo apt install -y libedgetpu1-std
```

Now set up docker stuff

```shell
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Prepare the Nvidia stuff for containers

```shell
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey -o /etc/apt/keyrings/nvidia-container.asc
sudo chmod a+r /etc/apt/keyrings/nvidia-container.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/nvidia-container.asc] https://nvidia.github.io/libnvidia-container/stable/deb/\$(ARCH) /" | \
  sudo tee /etc/apt/sources.list.d/nvidia-container.list > /dev/null
sudo apt update
sudo apt install -y nvidia-container-toolkit nvidia-utils-535-server linux-modules-nvidia-535-server-generic libnvidia-decode-535-server
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Give it a reboot for good measure

```shell
sudo reboot
``` 

### To-Do List with Instructions

#### 1. Ensure Raspberry Pi and Program Run After Power Outage

1. **Create a systemd service file for your Python script:**
    - Open a terminal on your Raspberry Pi.
    - Create a new service file:
      ```sh
      sudo nano /etc/systemd/system/relay_control.service
      ```
    - Add the following content to the file:
      ```ini
      [Unit]
      Description=Relay Control Service
      After=network.target

      [Service]
      ExecStart=/usr/bin/python3 /path/to/your/main.py
      WorkingDirectory=/path/to/your/
      StandardOutput=inherit
      StandardError=inherit
      Restart=always
      User=pi

      [Install]
      WantedBy=multi-user.target
      ```
    - Replace `/path/to/your/main.py` with the actual path to your Python script.
    - Save and exit the editor (press `Ctrl+X`, then `Y`, and `Enter`).

2. **Enable the service to start on boot:**
    - Reload the systemd daemon:
      ```sh
      sudo systemctl daemon-reload
      ```
    - Enable the service:
      ```sh
      sudo systemctl enable relay_control.service
      ```
    - Start the service immediately:
      ```sh
      sudo systemctl start relay_control.service
      ```
    - Check the status of the service:
      ```sh
      sudo systemctl status relay_control.service
      ```

#### 2. Enable SSH on Raspberry Pi OS Lite

1. **Enable SSH via the terminal:**
    - Open a terminal on your Raspberry Pi.
    - Run the following command:
      ```sh
      sudo raspi-config
      ```
    - Navigate to `Interfacing Options` using the arrow keys.
    - Select `SSH` and press Enter.
    - Choose `Enable` and press Enter.
    - Exit the configuration tool.

2. **Alternatively, enable SSH by creating an empty file:**
    - Insert the SD card into your computer.
    - Create an empty file named `ssh` (no extension) in the root of the boot partition.
    - Safely eject the SD card and insert it back into the Raspberry Pi.
    - Boot the Raspberry Pi.

#### 3. Connect to Wi-Fi on Raspberry Pi OS Lite

1. **Edit the `wpa_supplicant.conf` file:**
    - Open the `wpa_supplicant.conf` file in a text editor:
      ```sh
      sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
      ```
    - Add the following configuration, replacing `YOUR_SSID` and `YOUR_PASSWORD` with your Wi-Fi network's SSID and password:
      ```sh
      ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
      update_config=1
      country=US

      network={
          ssid="YOUR_SSID"
          psk="YOUR_PASSWORD"
          key_mgmt=WPA-PSK
      }
      ```
    - Save the file and exit the editor (press `Ctrl+X`, then `Y`, and `Enter`).

2. **Restart the networking service or reboot:**
    - Restart the networking service:
      ```sh
      sudo systemctl restart dhcpcd
      ```
    - Alternatively, reboot the Raspberry Pi:
      ```sh
      sudo reboot
      ```

3. **Verify the connection:**
    - After rebooting, check if the Raspberry Pi is connected to the Wi-Fi network:
      ```sh
      hostname -I
      ```
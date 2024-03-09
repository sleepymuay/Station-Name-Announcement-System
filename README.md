
# CMU Transit Station Name Announcement System


The CMU Transit Station Name Announcement 
System is developed using a single-board computer to announce the next station for transit users.



## Installation

### Requirements

- Raspberry Pi 3 model B+ or higher
-  GPS Ublox NEO-M8N GPS Module with Antenna

### Supported OS

- Debian GNU/Linux 11 (bullseye) or higher

## Diagram

![Hardware Diagram](https://img5.pic.in.th/file/secure-sv1/hw-diagram.md.png)

### Connection Details:
- **Red Wire**: Raspberry Pi Pin 2 (5V) to GPS Module VCC Pin.
- **Black Wire**: Raspberry Pi Pin 6 (Ground) to GPS Module GND Pin.
- **Green Wire**: Raspberry Pi Pin 8 (GPIO14 TXD) to GPS Module RX Pin.
- **Blue Wire**: Raspberry Pi Pin 10 (GPIO15 RXD) to GPS Module TX Pin.

### Setting Up the OS

1. **Edit the `/boot/config.txt` file**:
    ```bash
    sudo nano /boot/config.txt
    ```
   Add the following lines at the bottom of the file:
    ```plaintext
    dtparam=spi=on
    dtoverlay=pi3-disable-bt
    core_freq=250
    enable_uart=1
    force_turbo=1
    ```
   Press `Ctrl+X` to exit, then `Y` to save.

2. **Edit the `/boot/cmdline.txt` file**:
    ```bash
    sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt
    sudo nano /boot/cmdline.txt
    ```
   Replace the content with:
    ```plaintext
    dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
    ```
   Press `Ctrl+X` to exit, then `Y` to save.

3. **Reboot your Raspberry Pi**:
    ```bash
    sudo reboot
    ```

4. **Disable Raspberry Pi Serial Getty Service**:
    - If `Serial0` is linked with `ttyAMA0`:
        ```bash
        sudo systemctl stop serial-getty@ttyAMA0.service
        sudo systemctl disable serial-getty@ttyAMA0.service
        ```
    - If `Serial0` is linked with `ttys0`:
        ```bash
        sudo systemctl stop serial-getty@ttys0.service
        sudo systemctl disable serial-getty@ttys0.service
        ```

5. **Activate `ttys0`**:
    ```bash
    sudo systemctl enable serial-getty@ttys0.service
    ```

### Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sleepymuay/Station-Name-Announcement-System.git
    cd Station-Name-Announcement-System
    ```

2. **Edit Station Details**:
    - Edit station details in `station.csv`.
    - Update the station's sound in the `sound` folder. Ensure filenames match entries in `station.csv`.

3. **Run the Code**:
    ```bash
    python3 project_readfile.py
    ```

### Additional Notes

Before running the code:
- Power the Raspberry Pi and connect the GPS Module.
- Calibrate the GPS until you see the red/green light blink on the GPS Module. **Ensure there are no obstructions above to ensure proper GPS calibration.** If necessary, move the setup outdoors for calibration.

# NIU E-Scooter Firmware Repository

This repository provides firmware files for KQI3 and KQI2 scooters, collected from various sources. Additionally, JSON descriptors are included with information such as file names, types, and MD5 checksums.

The repository also contains reverse engineered files:
- **All firmware binaries** have been reverse engineered to `.decompiled` files containing ARM assembly disassembly
- The decompiled **H07 bootloader** can be found in the KQI3 folder (original decompiled version)
- A decompiled version of the **KQI 300X DE firmware** is located in the "KQI300X" folder (original decompiled version)
- **New**: All other firmware files now have corresponding `.decompiled` files with ARM assembly disassembly generated using `reverse_firmware.py`

If you own the KQI 300 X/P version from the USA or the EU and are interested in making the firmware flashable, feel free to [contact me](mailto://david635883@proton.me).

## Reverse Engineering

This repository includes reverse engineered versions of all firmware files. Each `.bin` firmware file has a corresponding `.decompiled` file containing ARM assembly disassembly.

### Using the Reverse Engineering Tool

The repository includes `reverse_firmware.py`, a Python script that automatically generates ARM assembly disassembly for firmware files:

```bash
python3 reverse_firmware.py
```

The script will:
- Find all `.bin` files that don't have corresponding `.decompiled` files
- Generate ARM assembly disassembly using `arm-linux-gnueabi-objdump`
- Save the output to `.decompiled` files with proper headers

### Prerequisites

To run the reverse engineering tool, you need:
- Python 3
- ARM cross-compilation tools: `sudo apt install gcc-arm-linux-gnueabi binutils-arm-linux-gnueabi`

### Tutorial
A tutorial (in Spanish, but with subtitles): [YouTube Link](https://www.youtube.com/watch?v=40BTCnkcEHg)

---

## Firmware Downloads

### **KQI2 PRO**

#### Germany (DE):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%202/Pro/DE/update.json)

#### Europe (EU):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%202/Pro/EU/update.json)

#### USA (US):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%202/Pro/US/update.json)

---

### **KQI3 Sport**

#### Germany (DE):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Sport/DE/update.json)

#### Europe (EU):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Sport/EU/update.json)

#### USA (US):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Sport/US/update.json)

---

### **KQI3 Pro**

#### Germany (DE):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Pro/DE/update.json)

#### Europe (EU):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Pro/EU/update.json)

#### USA (US):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Pro/US/update.json)

---

### **KQI3 Max**

#### Germany (DE):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Max/DE/update.json)

#### Europe (EU):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Max/EU/update.json)

#### USA (US):
[Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%203/Max/US/update.json)

---

### **KQI300 X**

#### Germany (DE):
- [Update URL](https://raw.githubusercontent.com/davidpr0811/niu_firmware/main/KQI%20300/x/de/update.json)
- [Decompiled Firmware](https://github.com/davidpr0811/niu_firmware/blob/main/KQI%20300/x/de/update.json)

#### Europe (EU):
- **Update URL:** (not yet available)
- **Decompiled Firmware:** (not yet available)

#### USA (US):
- **Update URL:** (not yet available)
- **Decompiled Firmware:** (not yet available)

---

## Note
The files in the KQI3 and KQI2 folders are sourced from the [ScooterHacking Utility](https://github.com/scooterhacking/niu_scooters).

---

### Trick to Increase Speed on KQI3 Sport and KQI3 Pro
There is a trick to make the KQI3 Sport and KQI3 Pro scooters faster:
1. Flash the KQI3 Max firmware onto the scooter.
2. Set the custom mode speed to 38 km/h.
3. Flash the correct firmware for your scooter back onto the device.

**Important:**
- Avoid changing the scooter's settings via the app or locking the scooter after using this trick, as this will reset the scooter to its original maximum speed.


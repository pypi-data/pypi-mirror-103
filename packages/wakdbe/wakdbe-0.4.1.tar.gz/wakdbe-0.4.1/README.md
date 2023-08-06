<p align="center">
  <img src="https://img.shields.io/github/languages/top/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
  <img src="https://img.shields.io/github/license/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=license">
  <img src="https://img.shields.io/badge/depends-JAVA-informational">

</p>

<br />

<p align="center">
  <img src="https://img.shields.io/badge/windows-almost-blue">
  <img src="https://img.shields.io/badge/kali-beta-yellow">
  <img src="https://img.shields.io/badge/ubuntu-beta-yellow">
  <img src="https://img.shields.io/badge/mac-not%20tested-red">  
</p>


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
    <img src="https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png" alt="Logo" width="320" height="100">
  </a>

  <h3 align="center">WhatsApp Key/Database Extractor</h3>

  <p align="center">
    Extract key/msgstore.db from /data/data/com.whatsapp in Android v4.0+ without root.
    <br />
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Standalone Operations](#standalone-operations)
  * [Features & ToDo](#features--todo)
  * [Demo](#demo)
  * [Troubleshooting](#troubleshooting)
* [Limitations](#limitations)
* [Contributing](#contributing)
* [License](#license)
* [Agreement](#agreement)
* [Contact](#contact)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## About The Project

<!--[![Glimpse][product-screenshot]](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)-->

This project is inspired by [EliteAndroidApps/WhatsApp-Key-DB-Extractor](https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor). Since Android v4.0+ Google has removed adb backup and apps no longer supported being backed up by "adb backup -f myApp.ab -apk com.foobar.app". However there is one catch in this scenario and that is some old version of many apps including WhatsApp support that to this day, and that's the idea...

The idea is to install "Legacy Version" of WhatsApp on you device via adb and use "adb backup"  to fetch files from "/data/data/com.whatsapp" folder which includes both the 'key' and 'msgstore.db' (non encrypted) file and after that restore current WhatsApp.


### Built With
* [Python](https://www.python.org/)
* [Bash](https://www.gnu.org/software/bash/) (for Linux and OS X)

**Depends on**   

* [Java](https://www.java.com/) (To extract backup)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Getting Started

***Before doing anything take a backup of your chats and turn off your phone's internet so you don't lose any new messages.
For that go to 'WhatsApp Settings &#8594; Chat Settings &#8594; Chat Backup' here take a local bacakup. Prepare for Worst.***
After [intallation](#installation) follow on screen instructions.


### Prerequisites

* O/S: Any Windows/Mac/Linux.
* [Python 3.x](https://www.python.org/downloads/)
* [Java](https://www.java.com/en/download/)
* USB Debugging must be enabled on the target device. Settings &#8594; Developer Options &#8594; USB debugging.
  * If you cannot find Developer Options then please go to: Settings &#8594; About phone/device and tap the Build number multiple times until you're finally declared a developer.  
* Android device with Android 4.0 or higher. i.e. Ice Cream Sandwich, Jelly Bean, KitKat, Lollipop, Marshmallow, Nougat, Oreo, Pie, Q.  



### Installation

1. Download and install.
```bash
pip install wakdbe
```
2. Install dependencies (for linux and OSX only) : skip `sudo` for mac.
```bash
**TODO**
chmod +x bin/linux_dependencies.sh
sudo ./bin/linux_dependencies.sh
```
If you're getting any error while running above command you need to install the following manually for your linux distro. : [adb](https://developer.android.com/studio/command-line/adb) [curl](https://curl.se/download.html) [tar]() [openjdk11]() [7zip](https://www.7-zip.org/download.html) [scrcpy](https://github.com/Genymobile/scrcpy)

3. Unleash the beast
```python
python3 -m wakdbe -h
```

**Command Line Flags**

| Short | Flag                |          | Type   | Behaviour                                                              | Status |
| ----- | ------------------- | -------- | ------ | ---------------------------------------------------------------------- | ------ |
| -ar   |--allow-reboot       | Optional | Bool   | Reboots device before installing Legacy WhatsApp.                      | Stable |
| -tip  | --tcp-ip IP_ADDRESS | Optional | String | Connects to a remote device via TCP mode.                              | Stable |
| -tp   |--tcp-port PORT      | Optional | String | Port number to connect to. Default : 5555.                             | Stable |
| -s    | --scrcpy            | Optional | Bool   | Show device screen as a window using ScrCpy.                           | Stable |
| -to   | --tar-only          | Optional | Bool   | Get ALL files as a tarball instead of main files from whatsapp backup. | Beta   |

Example usage : 
```python
python3 -m wakdbe --allow-reboot --tcp-ip 192.168.43.130 --tcp-port 5555 --scrcpy --tar-only
python3 -m wakdbe -ar -tip 192.168.43.130 -tp 5555 -s -to
```

### Standalone Operations
**These operations are standalone implementation of their defined task. One should run these when specifically needed. For ex : Process finished but WhatsApp was not reinstalled on device.**

1. Run `view_extract` : To unpack whatsapp.ab to whatsapp.tar and extract files.
```
python3 -m wakdbe.view_extract
```
* IMP : For this to work there should be 'whatsapp.ab' file either in 'extracted/<userName>' folder or in 'tmp' folder in your directory.

2. Run `protect` : To compress/decompress user folder with(out) password for safekeeping.
```
python3 -m wakdbe.protect
```
* IMP : For this to work there should either be "userName" folder or "userName.7z" file in 'extracted' folder in current directory. Where "userName" is name of user you entered earlier.

3. Run `restore_whatsapp` : To reinstall WhatsApp on device.
```
python3 -m wakdbe.restore_whatsapp
```


### Features & ToDo
<!--https://github.com/StylishThemes/GitHub-Dark/wiki/Emoji-->

*  🟢 Extracts msgstore.db from /data/data/com.whatsapp. (duh)
*  🟢 Works wirelessly without USB cable using "ADB over TCP" with `--tcp-ip IP --tcp-port PORT` flags.
*  🟢 See and control your android phone with your computer using [ScrCpy](https://github.com/Genymobile/scrcpy) using `--scrcpy` flag.
*  🟢 Works with any android device v4.0+ so far.
*  🟢 Works with any android device no matter where it is in universe as long as it is running ADB over TCP.
*  🟢 Moves msgstore.db to your phone.
*  🟢 Creates password protected 7z file so keep your extraction safe.
*  🟢 Continues without JAVA installed and make "whatsapp.tar" out of "whatsapp.ab" once java is installed by running `python3 -m wakdbe.view_extract`.
*  🟢 Command line arguments
*  🟢 ADB Devices menu.
*  🟢 Implement datetime.
*  🟢 Extracts backup created over TCP.
*  🔴 Works with WhatsApp Business.


### Demo
https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/discussions/33


### Troubleshooting

* If running `python3 -m wa_kdbe` or any other file is throwing error like "python3 is recognised as interal or external command." AND python3 is "already added to path (in case of windows)" try running files with `py -m wa_kdbe` instead.
* If list is empty close terminal, remove and replug the device, and re-run the script. [Read more.](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/11#issuecomment-768500899)
* If you have never used USB Debugging before, you may also need to verify the fingerprint by ticking the checkbox and tapping 'allow' on device popup.  
* If you have set a default backup password in your Android settings, then this MUST be the  backup password that you PROVIDE when prompted to backup your data. Else it WILL fail!  
* If you get an error saying "AES encryption not allowed" then you need to update your Oracle Java Cryptography Extension (JCE) to Unlimited Strength Jurisdiction Policy Files.  
* WhatsApp crashing? Run `python3 -m wakdbe.restore_whatsapp`. Or "clear data/storage" / uninstall and reinstall from Play Store.
* In MIUI, "Failure [INSTALL_FAILED_USER_RESTRICTED: Install canceled by user]" occurs during installation of LegacyWhatsapp.apk, fix it by [allowing install via adb](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/16#issuecomment-768927639)
* If "[INSTALL_FAILED_VERSION_DOWNGRADE]" run with `--allow-reboot` flag.

  ```
  python3 -m wa_kdbe --allow-reboot
  ```
* If "[INSTALL_PARSE_FAILED_NOT_APK]" delete helpers/LegacyWhatsApp.apk and re-run.
* If "adb: error: cannot create 'tmp/WhatsAppbackup.apk': Permission denied" on macOS run script with `sudo`.

  ```
  sudo python3 -m wa_kdbe
  ```


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Limitations

There always are limitations on how much we can make it work  and this is what allows us to keep going. Well no matter what I do sometimes this tool just won't work on some devices and if that's your case you can try [this fork of MarcoG3's WhatsDump](https://github.com/Tkd-Alex/WhatsDump) by [Alessandro Maggio](https://github.com/Tkd-Alex/).

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project on GitHub.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. "Draft" a pull request and mark it "Ready for review" once work is done.

Other ways to contribute is to buy me a coffee but let's just say it is to test out new features of the project. **Checkout [features/fast](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/discussions/53#discussioncomment-625798) to test backup and reinstallation of WhatsApp on device level.** This makes it quite time saving specially in case of TCP.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/blob/master/LICENSE) for more information.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Agreement

I made this project because it was hard for me to kill time and the other one was very old. 
This tool is provided "as-is" and hence you will be responsible however you use it. Cheers☕

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contact

Yuvraj Raghuvanshi - [Send me a mail](mailto:YuvrajRaghuvanshi.S%40protonmail.com?subject=From%20GitHub%20WA-KDBE%20:%20%3CAdd%20subject%20here.%3E "Send me a mail, Don't change subject line.")

Project Link: [https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

[license-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/blob/master/LICENSE
[product-screenshot]: https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png

# Auto Requirements installer.
import json
import os
from os import path
import pathlib
import socket
import sys

try:
    import packaging
    import psutil
    import requests
    import termcolor
    from tqdm import tqdm
except ImportError:
    print('\nFirst run : Auto installing python requirements.\n')
    try:
        # Trying both methods of installations
        os.system('pip3 install --upgrade packaging psutil termcolor requests tqdm')
    except:
        os.system(
            'python3 -m pip install --upgrade packaging psutil termcolor requests tqdm')


import argparse
import concurrent.futures
import platform
import re
import subprocess
import time

from wakdbe.helpers import ADBDeviceSerialId as deviceId
from wakdbe.helpers import TCPDeviceSerialId as tcpDeviceId
from wakdbe.helpers.CustomCI import CustomInput, CustomPrint
from wakdbe.helpers.LinuxUSB import LinuxUSB
from wakdbe.helpers.WIndowsUSB import WindowsUSB
from wakdbe.view_extract import ExtractAB

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global Variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'
isJAVAInstalled = False

global myDir
myDir = pathlib.Path(__file__).parent.absolute()


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    CheckBin()
    ShowBanner()
    global isJAVAInstalled
    isJAVAInstalled = CheckJAVA()
    print('\n')
    try:
        CustomPrint('System Info : ' +
                    json.dumps(GetSysInfo(), indent=2, default=str))
        print('\n')
    except:
        CustomPrint(
            'Can\'t get system information. Continuing anyway...', 'yellow')
    CustomPrint('Current release date : 22/04/2021', 'cyan')
    print('\n')
    readInstruction = CustomInput(
        '\aPlease read above instructions carefully \u2191 . Continue? (default y) : ', 'yellow') or 'y'
    if(readInstruction.upper() == 'Y'):
        print('\n')
        CustomInput(
            '\aIf you haven\'t already, it is adviced to take a WhatsApp chat backup by going to WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup. Hit Enter key to continue.', 'yellow')
        USBMode()
    else:
        Exit()


def BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath):
    os.system(adb + ' shell am force-stop com.whatsapp') if(SDKVersion >
                                                            11) else os.system(adb + ' shell am kill com.whatsapp')
    CustomPrint('Backing up WhatsApp ' + versionName +
                ' apk, the one installed on device to ' + tmp + 'WhatsAppbackup.apk')
    os.mkdir(tmp) if not (os.path.isdir(tmp)) else CustomPrint(
        'Folder ' + tmp + ' already exists.', 'yellow')
    os.system(adb + ' shell cp ' + WhatsAppapkPath +
              ' /sdcard/WhatsAppbackup.apk')
    os.system(adb + ' pull /sdcard/WhatsAppbackup.apk ' +
              helpers + 'WhatsAppbackup.apk')
    # Delete temp apk from /sdcard.
    os.system(adb + ' shell rm -rf /sdcard/WhatsAppbackup.apk')
    CustomPrint('Apk backup complete.')


def BackupWhatsAppDataasAb(SDKVersion):
    CustomPrint('Backing up WhatsApp data as ' + tmp +
                'whatsapp.ab. May take time, don\'t panic.')
    try:
        os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab com.whatsapp') if(SDKVersion >=
                                                                             23) else os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e:
        CustomPrint(e, 'red')
        Exit()
    CustomPrint('Done backing up data. Size : ' +
                str(os.path.getsize(tmp + 'whatsapp.ab')) + ' bytes.')


def CheckBin():

    if (not pathlib.Path.is_dir(myDir / 'bin')):
        CustomPrint('I can not find bin folder, check again...', 'red')
        Exit()
    else:
        pass


def CheckJAVA():
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output(
        'java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled):
        CustomPrint('Found Java installed on system.')
        return isJAVAInstalled
    else:
        noJAVAContinue = CustomInput(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'red') or 'c'
        if(noJAVAContinue.upper() == 'C'):
            CustomPrint(
                'Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'yellow')
            return isJAVAInstalled
        else:
            Exit()


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system(
        bin + '/adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    os.system('pause')
    quit()


def GetSysInfo():
    info = {}
    info['Platform'] = platform.system()
    info['Platform Release'] = platform.release()
    info['Platform Version'] = platform.version()
    info['Architecture'] = platform.machine()
    info['Hostname'] = socket.gethostname()
    info['Processor'] = platform.processor()
    info['RAM'] = str(
        round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
    return info


def InstallLegacy(SDKVersion):
    CustomPrint('Installing legacy WhatsApp V2.11.431, hold tight now.')
    if(SDKVersion >= 17):
        os.system(adb + ' install -r -d ' + helpers + 'LegacyWhatsApp.apk')
    else:
        os.system(adb + ' install -r ' + helpers + 'LegacyWhatsApp.apk')
    CustomPrint('Installation Complete.')


def RealDeal(SDKVersion, WhatsAppapkPath, versionName, sdPath):
    BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath)
    UninstallWhatsApp(SDKVersion)
    # Reboot here.
    if(isAllowReboot):
        if(not tcpIP):
            print('\n')
            CustomPrint('Rebooting device, please wait.', 'yellow')
            os.system(adb + ' reboot')
            while(subprocess.getoutput(adb + ' get-state') != 'device'):
                CustomPrint('Waiting for device...')
                time.sleep(5)
            CustomInput('Hit Enter key after unlocking device.', 'yellow')
        else:
            CustomPrint(
                'Rebooting device in TCP mode break the connection and won\'t work until explicitly turned on in device and/or in PC. Skipping...', 'yellow')

    InstallLegacy(SDKVersion)
    # Before backup run app
    os.system(adb + ' shell am start -n com.whatsapp/.Main')
    CustomInput(
        '\aHit Enter key after running Legacy WhatsApp for a while. Ignore invalid date warning.', 'yellow')
    BackupWhatsAppDataasAb(SDKVersion)
    ReinstallWhatsApp()
    print('\n')
    CustomPrint(
        '\aOur work with device has finished, it is safe to remove it now.', 'yellow')
    print('\n')
    ExtractAB(isJAVAInstalled, sdPath=sdPath,
              ADBSerialId=ADBSerialId, isTarOnly=isTarOnly)


def ReinstallWhatsApp():
    CustomPrint('Reinstallting original WhatsApp.')
    try:
        os.system(adb + ' install -r -d ' + helpers + 'WhatsAppbackup.apk')
    except Exception as e:
        CustomPrint(e, 'red')
        CustomPrint('Could not install WhatsApp, install by running \'restore_whatsapp.py\' or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings \u2192 app settings \u2192 WhatsApp.')
        Exit()


def RunScrCpy(_isScrCpy):
    if(_isScrCpy):
        cmd = bin + '/scrcpy.exe --max-fps 15 -b 4M --always-on-top' if(
            isWindows) else 'scrcpy --max-fps 15 -b 4M --always-on-top'
        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=False)
        proc.communicate()


def ShowBanner():
    banner_content = '''
================================================================================
========                                                                ========
========  db   d8b   db  .d8b.         db   dD d8888b. d8888b. d88888b  ======== 
========  88   I8I   88 d8' `8b        88 ,8P' 88  `8D 88  `8D 88'      ======== 
========  88   I8I   88 88ooo88        88,8P   88   88 88oooY' 88ooooo  ======== 
========  Y8   I8I   88 88~~~88 C8888D 88`8b   88   88 88~~~b. 88~~~~~  ======== 
========  `8b d8'8b d8' 88   88        88 `88. 88  .8D 88   8D 88.      ======== 
========   `8b8' `8d8'  YP   YP        YP   YD Y8888D' Y8888P' Y88888P  ======== 
========                                                                ========
================================================================================
    '''
    CustomPrint(banner_content, 'green', ['bold'], False)
    CustomPrint('============ WhatsApp Key / Database Extrator for non-rooted Android ===========',
                'green', ['bold'], False)
    intro_content = '''
================================================================================
===                                                                          ===
===  xxxxx  PLEASE TAKE WHATSAPP CHAT BACKUP BEFORE GETTING STARTED.  xxxxx  ===
===                                                                          ===
===     For that go to 'WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup'     ===
===              here take a local backup. Prepare for Worst.                ===
===                                                                          ===
===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===
===   unencrypted file) and your 'key' file from '/data/data/com.whatsapp'   ===
===  directory in Android 4.0+ device without root access. However you need  ===
===   to have JAVA installed on your system in order to 'view the extract'.  ===
===  If you don't have JAVA installed then you can 'view extract' later by   ===
===   running 'view_extract.py'. The idea is to install a 'Legacy WhatsApp'  ===
===       temporarily on your device in order to get the android backup      ===
===    permission. You should not lose any data and your current WhatsApp    ===
===   version will be installed after this process so don't panic and don't  ===
=== stop this script while it's working. However if something fails you can  ===
===    run 'restore_whatsapp.py' and reinstall current WhatsApp or simply    ===
===                    update that from Google Play Store.                   ===
===                                                                          ===
===                      Script by : Yuvraj Raghuvanshi                      ===
===                      Github.com/YuvrajRaghuvanshiS                       ===
================================================================================
    '''
    CustomPrint(intro_content, 'green', ['bold'], False)


def UninstallWhatsApp(SDKVersion):
    if(SDKVersion >= 23):
        try:
            CustomPrint('Uninstalling WhatsApp, skipping data.')
            os.system(adb + ' shell pm uninstall -k com.whatsapp')
            CustomPrint('Uninstalled.')
        except Exception as e:
            CustomPrint('Could not uninstall WhatsApp.')
            CustomPrint(e, 'red')
            Exit()


def USBMode():
    if(isWindows):
        ACReturnCode, SDKVersion, WhatsAppapkPath, versionName, sdPath = WindowsUSB(
            adb)
        RealDeal(SDKVersion, WhatsAppapkPath, versionName,
                 sdPath) if ACReturnCode == 1 else Exit()
    else:
        ACReturnCode, SDKVersion, WhatsAppapkPath, versionName, sdPath = LinuxUSB(
            ADBSerialId)
        RealDeal(SDKVersion, WhatsAppapkPath, versionName,
                 sdPath) if ACReturnCode == 1 else Exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-ar', '--allow-reboot', action='store_true',
                        help='Allow reboot of device before installation of LegacyWhatsApp.apk to prevent some issues like [INSTALL_FAILED_VERSION_DOWNGRADE]')
    parser.add_argument(
        '-tip', '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default : 5555')
    parser.add_argument('-s', '--scrcpy', action='store_true',
                        help='Run ScrCpy to see and control Android device.')
    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in <username>.tar file instead of just getting few important files.')
    args = parser.parse_args()
    #args = parser.parse_args('--tcp-ip 192.168.43.130 --scrcpy'.split())

    isAllowReboot = args.allow_reboot
    tcpIP = args.tcp_ip
    tcpPort = args.tcp_port
    isScrCpy = args.scrcpy
    isTarOnly = args.tar_only
    if(tcpIP):
        if(not tcpPort):
            tcpPort = '5555'
        ADBSerialId = tcpDeviceId.init(tcpIP, tcpPort)
    else:
        ADBSerialId = deviceId.init()
    if(not ADBSerialId):
        Exit()

    # Global command line helpers
    tmp = 'tmp/'
    helpers = 'helpers/'
    bin = str(pathlib.Path(myDir / 'bin'))
    if(isWindows):
        adb = bin + '/adb.exe -s ' + ADBSerialId
    else:
        adb = 'adb -s ' + ADBSerialId

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(main)
        time.sleep(1)
        f2 = executor.submit(RunScrCpy, isScrCpy)

import os
import pathlib
import platform
import shutil


from wakdbe.helpers.CustomCI import CustomInput, CustomPrint

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global command line helpers
extracted = 'extracted/'
global mainDir
mainDir = pathlib.Path(__file__).parent.absolute()
bin = str(pathlib.Path(mainDir / 'bin')) + '\\'
if(isWindows):
    sevenZip = bin + '7za.exe'
else:
    sevenZip = '7z'


def main():
    CustomPrint('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    isCompressing = CustomInput('Are you (C)ompressing or (D)ecompressing? : ')
    while(True):
        if(isCompressing.upper() == 'C'):
            ListUserFolders()
            print('\n')
            userFolder = CustomInput(
                'Enter a name of folder from above (case sensitive) : ')
            Compress(userFolder)
            break
        elif(isCompressing.upper() == 'D'):
            ListUserFiles()
            print('\n')
            userZip = CustomInput(
                'Enter a name of file from above (case sensitive) : ')
            Uncompress(userZip)
            break
        else:
            isCompressing = CustomInput('Choose either \'c\' or \'d\' : ')
            continue


def Compress(userFolder):
    if(not os.path.isdir(extracted + userFolder)):
        CustomPrint('Could not find directory ' + extracted + userFolder)
        Exit()
    elif(len(os.listdir(extracted + userFolder)) == 0):
        CustomPrint('User folder is empty.')
        Exit()
    else:
        password = CustomInput('Choose a password for zip : ')
        if(password):
            password = ' -p' + password
        os.system(sevenZip + ' a -t7z -mhe ' + extracted +
                  userFolder + ' ' + extracted + userFolder + '/* ' + password)
        print('\n')
        CustomPrint(
            'If you see \'Everything is OK\' in above line then it is recommended to delete user folder.')
        deleteUserFolder = CustomInput(
            'Delete ' + userFolder + ' folder? (default y) : ') or 'y'
        print('\n')
        CustomPrint('\aYour \'' + userFolder + '.7z\' file is in ' + os.path.realpath(extracted) + ' folder. Password is : ' +
                    password.replace(' -p', ''), 'yellow')
        print('\n')
        CustomInput('Hit Enter key to continue.')
        if(deleteUserFolder.upper() == 'Y'):
            DeleteUserFolder(userFolder)
        else:
            Exit()


def DeleteUserFolder(userFolder):
    CustomPrint('Deleting...')
    try:
        shutil.rmtree(extracted + userFolder)
    except Exception as e:
        CustomPrint(e, 'red')
        CustomPrint('Please manually delete it.', 'red')
    Exit()


def DeleteUserZip(userZip):
    CustomPrint('Deleting...')
    try:
        os.remove(extracted + userZip)
    except Exception as e:
        CustomPrint(e, 'red')
        CustomPrint('Please manually delete it.', 'red')
    Exit()


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    try:  # Open in explorer.
        if(isWindows):
            os.startfile(os.path.realpath(extracted))
        elif(isLinux):
            os.system('xdg-open ' + os.path.realpath(extracted))
        else:
            os.system('open ' + os.path.realpath(extracted))
    except:
        pass
    CustomInput('Hit \'Enter\' key to continue....', 'cyan')
    quit()


def ListUserFiles():
    if(not os.path.isdir(extracted)):
        CustomPrint('\aCan\'t find \'extracted\' folder...', 'red')
        Exit()
    print('\n')
    CustomPrint('Available user files in extracted directory.')
    print('\n')
    allFiles = next(os.walk(extracted))[2]
    if(len(allFiles) == 1 and os.path.isfile(extracted + '.placeholder')):
        CustomPrint('No user files found in ' + extracted + ' folder.', 'red')
        Exit()
    for file in allFiles:
        if(file != '.placeholder'):
            CustomPrint(file)


def ListUserFolders():
    if(not os.path.isdir(extracted)):
        CustomPrint('\aCan\'t find \'extracted\' folder...', 'red')
        Exit()
    print('\n')
    CustomPrint('Available user folders in extracted directory.')
    print('\n')
    allFolders = next(os.walk(extracted))[1]
    if(len(allFolders) == 0):
        CustomPrint('No folders found in ' + extracted + ' folder.', 'red')
        Exit()
    for folder in allFolders:
        CustomPrint(folder)


def Uncompress(userZip):
    if(not str(userZip).endswith('7z')):
        userZip = userZip + '.7z'
    if(not os.path.isfile(extracted + userZip)):
        CustomPrint('Could not find ' + extracted + userZip)
        Exit()
    elif(os.path.getsize(extracted + userZip) <= 0):
        CustomPrint(extracted + userZip + ' is empty.')
        Exit()
    else:
        password = CustomInput('Enter password, leave empty for none : ')
        if(password):
            password = ' -p' + password
        os.system(sevenZip + ' e -aot ' + extracted + userZip +
                  ' -o' + extracted + userZip.replace('.7z', '') + password)
        print('\n')
        CustomPrint(
            'If you see \'Everything is OK\' in above line then you can delete user zip file.')
        deleteUserZip = CustomInput(
            'Delete ' + userZip + ' ? (default n) : ') or 'n'
        print('\n')
        CustomPrint('\aYour extracted \'' + userZip.replace('.7z',
                                                            '') + '\' folder is in ' + os.path.realpath(extracted + userZip.replace('.7z', '')) + ' folder.', 'yellow')
        print('\n')
        CustomInput('Hit Enter key to continue.')
        if(deleteUserZip.upper() == 'Y'):
            DeleteUserZip(userZip)
        else:
            Exit()


if __name__ == "__main__":
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
# check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234

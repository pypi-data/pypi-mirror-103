# Clien [cli-environment]
## Tool to help developer to create encrypted password
### [Under-Development]

## Installation
```
pip install Clien-karjakak
```
## Usage
**Create password that set to environment variable in encrypted mode.**
```Console
clien -c # Will launch a tkinter Entry to show hidden for data.
```
**Read encrypted variable's data.**
```Console
clien -r %VAR_DATA% # Will launch tkinter Entry for password to decrypt encryption.
```
**If use echo, the data will come out encrypted data.**
```Console
echo %CLIENTEST%
5ua2erb9dualy1a0d

clien -r %CLIENTEST% # After key-in password
Ok Banget
```
**TAKE NOTE:**
* **Wrong password will either raise an error or produce different result than the original.**
* **Please do not forget your passcode.**

**Usage in script:**
```Python
from clien import cmsk, reading, insdata, pssd

# Encrypting to environment variable
cmsk("data that will be encrypted", "VAR_NAME", "passcode")

# For decrypting
reading(os.environ['VAR_NAME'], "passcode")

# For interactive usage using CLI or GUI program.
GetData = insdata()
cmsk(GetData[0], GetData[1], Getdata[2])

ReadData = pssd()
reading(os.environ['VAR_NAME'], ReadData)
```

## Notes
* **This package is used in Ezpub-karjakak [as dependency] for encrypting token.**
* **Is best use for any developer that require free-hassle of creating environment variable.**
* **Is save from prying eyes in case "echo" is used.**


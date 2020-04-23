# PyInstaller for Windows Store

[Date] 23 Apr 2020

[Environment]
* Python 3.7
* Kivy 1.11.1
* PyInstaller 3.6
* OS: Windows 10 Pro 1809 (Required for MSIX)

### Prepare Application Directories

Separate installation and working directories. You will not be able to modify the installation directory. Therefore, 
use local data directory for the files you will change.

You can get the local application data dir by:
```
self.workdir = os.environ['APPDATA']
```

### Build PyInstaller Executable

* First, read [Kivy Guide](https://kivy.org/doc/stable/guide/packaging-windows.html).

* Install python3

Python3.7 should be 64 bit for 64 bit windows. Otherwise, icon in exe yields virus warnings.

* Create your env (.kivy) and activate it
```
python -m venv .kivy
.kivy\Scripts\activate
```
* Get pip install script [from](https://bootstrap.pypa.io/get-pip.py) and install
```
python get-pip.py
```

* Install kivy
```
pip install kivy
```

* Update pyinstaller and additional libs
```
pip install kivy.deps.sdl2
pip install kivy.deps.glew
pip install kivy.deps.angle 
pip install --upgrade pyinstaller
pip install pyenchant
pip install setuptools==44.0.0
#or pip install --upgrade 'setuptools<45.0.0'
pip install Cython==0.29.10
pip install pypiwin32
```

* Install your required libs 

* Create pyinstaller spec file
```
python -m PyInstaller --name theapp
```

* Edit spec file

[Sample spec file](theapp.spec)

* Build package
```
python -m PyInstaller theapp.spec
pyinstaller theapp.spec
```

* Delete critical source code if they remain in app
```
del dist\theapp\my.py
```


### Single setup file with Inno

* Install [Inno](https://jrsoftware.org/isdl.php#stable)

* Set Program Files (x86 for 64 bit) as Installation Dir
```
DefaultDirName={pf}\{#MyAppName}
```
* Enable installation privilege selection
```
PrivilegesRequiredOverridesAllowed=commandline dialog
```
* You can use the same created theapp.iss file again.

## Build MSIX Package

* You should have a Microsoft Developer account. If not, [create](https://partner.microsoft.com).

* Get Package Information from the application submission you created [at](https://partner.microsoft.com). 

* Open MSIX and select the setup file you created with Inno.

* Enter package information

-- Package name: 

-- Package display name: 

-- Publisher name: 

-- Publisher display name: 

-- Version: 

-- Package Description: 

-- Signing preference: Do not sign

-- Installation Location: Program Files(x86)

* Open manifest file at last page by selecting Package editor

-- Change Manifest File or Edit from Capabilities Menu

```
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.18335.0" />
  </Dependencies>


  <Capabilities>
    <uap:Capability Name="picturesLibrary" />
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>

```

### Validate your package 

Install Windows 10 SDK. Use Windows App Certification Kit to validate your MSIX package. In case of problems analyze its report.


### Issues

* OpenGL version 1.1 on remote window 10 virtual machine

[1](https://github.com/kivy/kivy/issues/5248), 
[2](https://github.com/kivy/kivy/issues/5071),
[3](https://community.khronos.org/t/i-have-opengl-3-1-but-kivy-says-that-i-have-only-1-1/103980/6)

* To build pyinstaller package in .spec file
```
# to build package in azure vm (no opengl >2.0 so use opengl es)
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
```
 
### LINKS

[MSIX Usage](https://docs.microsoft.com/en-us/windows/msix/packaging-tool/create-app-package)

[MSIX Supported Platforms](https://docs.microsoft.com/en-us/windows/msix/supported-platforms)

[Windows App Certification Kit](https://developer.microsoft.com/en-us/windows/downloads/app-certification-kit/)



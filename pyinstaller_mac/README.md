# PyInstaller for Mac App Store

[Date] 27 Apr 2020

[Environment]
* Python 3.7
* Kivy 1.11.1
* PyInstaller 3.6
* OS: MacOS Catalina 10.15.4 (Required for Transporter)

### Prepare Application Directories

Make sandbox compliant directory structure. 

Application installation directory can not be changed after signing the package with the certificate. 

Therefore, you should use sandbox container data directory as working directory. Put your results, config files, etc. that the application changes in that directory.

[Home dir of sandbox container](https://developer.apple.com/documentation/foundation/1413045-nshomedirectory)


## Build mac osx app with pyinstaller

* First, read Kivy [guide](https://kivy.org/doc/stable/guide/packaging-osx.html)

* Create python3 virtualenv

```
python3 -m venv ~/.kivy 
source ~/.kivy/bin/activate
```

* Install kivy, cython, pyinstaller
```
pip install Cython==0.29.10
pip install -U kivy
pip install -U pyinstaller
pip install pyenchant
```

* Install required libraries

Note: If you are using opencv use headless version to get rid of qt dependency which causes mac submission reject due to non-public API usage.
```
pip install opencv-contrib-python-headless==4.1.2.30
```

* create pyinstaller spec file

```
pyinstaller -y --clean --windowed --name theapp \
  --exclude-module _tkinter \
  --exclude-module Tkinter \
  --exclude-module enchant \
  --exclude-module twisted \
  main.py
```

* Modify spec file

[Sample spec file](theapp.spec)



* Delete critical source code if they remain in app
```
find dist/ -name my.py -delete

```

* Build app

```
python -m PyInstaller theapp.spec
# or
pyinstaller -y --clean --windowed theapp.spec
# or
pyinstaller -y --clean --windowed --osx-bundle-identifier com.esenbil.theapp theapp.spec
```

* Remove 32 bit libs if there exists any in your package. Mac App Store accepts only 64 bit binaries.

Use ```lipo``` command.
```
lipo -remove i386 "$i" -o "$i"
```

* Move python base_library.zip to Resources and make a symbolic link to avoid signing problem.
 
```
mv Theapp.app/Contents/MacOS/base_library.zip Theapp.app/Contents/Resources/
cd Theapp.app/Contents/MacOS
ln -s ./../Resources/base_library.zip base_library.zip
cd -
```

* Run executable from command line to see debug output
```
dist/Theapp.app/Contents/MacOS/TheApp
```


### Sign and Create Mac Package

* Create your certificate and keys at [appstoreconnect](https://appstoreconnect.apple.com). Import them to your Keychain.

You need "3rd Party Mac Developer Application" (to sign package) and ""3rd Party Mac Developer Installer" (to create installer package) certificates.

* Check  your certificates
```
security find-identity -p codesigning
```

* Create your app in [App Store Connect](https://appstoreconnect.apple.com)

- Set proper bundle id.

* Adjust Info.plist located at TheApp.app/Contents directory.

For Mac applications you should modify the default Info.plist that pyinstaller produces.

[Sample](Info.plist)



* Sign the package with proper entitlements
```
codesign --deep --entitlements p.entitlements -s "3rd Party Mac Developer Application: ZZZ (ZZZ)" dist/Theapp.app/
```

[Sample entitlements](p.entitlements)


* Check the sign
```
codesign --display --entitlements - dist/Theapp.app/
```

* Build package
```
productbuild --sign "3rd Party Mac Developer Installer: ZZZ (ZZZ)" --component dist/Theapp.app/ /Applications dist/Theapp.pkg
```

* Validate package with altool to see if there are any errors. Create temporary application specific password at [appleid](https://appleid.apple.com/)

```
xcrun altool -t osx -f Theapp.pkg --primary-bundle-id com.esenbil.theapp  --validate-app --username ZZZ
```

* Use Transporter to submit your package

* Finally, modify app settings in App Store Connect -> My Apps and submit for review.


### Issues in Review

* "Your app requests keystrokes access from the user during operation of launch of the app."

"We also advise ensuring the Keystrokes modal is not presented to the user.

To resolve this issue, please confirm that you are using:

- NSEvent.addLocalMonitor

rather than

- CGEvent.TapCreate. "

* Use opencv headless version to get rid of qt dependency. Qt uses non-public system API calls which result in rejection.

[macOS 10.15 keystroke permission for SDL2](https://discourse.libsdl.org/t/macos-10-15-new-permission-prompts/26251)

[Advances in macOS Security](https://asciiwwdc.com/2019/sessions/701)

[Headless opencv](https://pypi.org/project/opencv-python-headless/)

* Entitlement reasons should be described in Info.plist

[Writing purpose string](https://stackoverflow.com/questions/54677322/apple-rejected-app-asking-to-provide-relevant-purpose-string-info-plist)
 
 
### Links

[macOS binaries crash if codesigned with hardened runtime enabled](https://github.com/pyinstaller/pyinstaller/issues/4629)

- The entitlement key <key>com.apple.security.cs.allow-unsigned-executable-memory</key> is not accepted in submission. This issue is maybe due to 32 bit libs in the package.

[Embedding Python in a MacOS Application](https://medium.com/python-pandemonium/embedding-a-python-application-in-macos-d866adfcaf94)

[Recipe OSX Code Signing](https://github.com/pyinstaller/pyinstaller/wiki/Recipe-OSX-Code-Signing)

[Create a certificate signing request](https://help.apple.com/developer-account/#/devbfa00fef7)

[Create Developer ID certificates](https://help.apple.com/developer-account/#/dev04fd06d56)

[Mac App Sandbox](https://developer.apple.com/documentation/security/app_sandbox)

[On Mac Sandbox](https://geosn0w.github.io/A-Long-Evening-With-macOS%27s-Sandbox/)

[Home dir of sandbox container](https://developer.apple.com/documentation/foundation/1413045-nshomedirectory)

- "In macOS, it is the application’s sandbox directory or the current user’s home directory (if the application is not in a sandbox)"
- os.environ('HOME') = /Users/ersinesen/Library/Containers/com.esenbil.theapp/Data

[Validate signed app](https://help.apple.com/asc/appsaltool/#/apdATD1E53-D1E1A1303-D1E53A1126)

[macOS Code Signing In Depth](https://developer.apple.com/library/archive/technotes/tn2206/_index.html)

[Upload Tools](https://help.apple.com/app-store-connect/#/devb1c185036)

[base_library.zip should be in the Contents/Resources not Contents/MacOS folder else codesigning is fragile](https://github.com/pyinstaller/pyinstaller/issues/3550)

[How do you fix “code object is not signed at all In subcomponent](https://stackoverflow.com/questions/29076321/how-do-you-fix-code-object-is-not-signed-at-all-in-subcomponent-in-xcode-6-m)
# Qt CLI installer

This is a simple script replacing the official graphical Qt installer. It can
automatically download prebuilt Qt binaries for any target (you're not bound to
Linux binaries on Linux; you could also download iOS binaries). 

This is a great alternative to the 2.5GB+ offline installers which just include
everything and are the only official way to pin QT versions with. Think of this
as a pinned online installer alternative. 

This isn't official nor set in stone. If something breaks, please create an
issue. 

**Dependencies**: Python 3.7, Python `requests` library, 7z

## Usage

```
./qli-installer.py <qt-version> <host> <target> [<arch>]
```

The Qt version is formatted like this: `5.11.3`  
Host is one of: `linux`, `mac`, `windows`  
Target is one of: `desktop`, `android`, `ios` (iOS only works with mac host)  
For android and windows you also need to specify an arch: `win64_msvc2017_64`,
`win64_msvc2015_64`, `win32_msvc2015`, `win32_mingw53`, `android_x86`,
`android_armv7`

Example: Installing Qt 5.12.0 for Linux:

```bash
./qli-installer.py 5.12.0 linux desktop
```

Example: Installing Android (armv7) Qt 5.10.2:

```bash
./qli-installer.py 5.10.2 linux android android_armv7
```

Example: Installing QT 5.12.3 (msvc_2017) Qt 5.10.2:

```bash
./qli-installer.py 5.12.3 windows desktop win32_msvc2017
```

All these examples will create a `tmp` folder within the root of the script and
an `output` folder with the downloaded target.

## Original Repository

https://git.kaidan.im/lnj/qli-installer/blob/master/

This fork of this tool is hosted on GitHub:

https://github.com/nelsonjchen/qli-installer  
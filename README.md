# Qt CLI installer

[![Build Status](https://dev.azure.com/nelsonjchen/QLI-Installer/_apis/build/status/nelsonjchen.qli-installer?branchName=master)](https://dev.azure.com/nelsonjchen/QLI-Installer/_build/latest?definitionId=15&branchName=master)

This is a simple script replacing the official online-only graphical Qt installer. It can
automatically download prebuilt Qt binaries for any target (you're not bound to
Linux binaries on Linux; you could also download iOS binaries).

This is a great alternative to the 2.5GB+ offline executable installers which just include
everything and are the only official way to pin Qt versions with. Think of this
as a version selecting online installer alternative that Qt doesn't put out.
It's great for projects using cloud CI systems without access to a huge cache or
capacity to host a pinned Qt download themselves.

Naturally, this is also headless and lightweight. Though if you would like to use the
*official* large installers headlessly, might I suggest you take a look at the
[CuteCI project][cuteci]? It's way heavier than this though in file footprint
and takes much longer to install with even on a fast machine in a datacenter.
For example, the extracted CuteCI UI silent install takes about 7 minutes on
Windows to install the Windows Qt5 MSVC Win64 toolkit while this script
takes about 21 seconds. Still, it is **official** which this will never be. It
also supports pure-offline installation. This script requires connectivity to Qt
mirrors.

This isn't the official installer though so don't expect support from Qt!
If something breaks, please create an issue at in *this* project's tracker.

**Dependencies**: Python 3.6/3.7, Python `requests` library
 (see or `pip install -r` `requirements.txt`), 7z or p7zip

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

The `tmp` and `output` folders can be adjusted with their respective
environment variables: `QLI_TMP_DIR` and `QLI_OUT_DIR`.

The Base URL can be adjusted too if the default Qt URL is too unstable with
`QLI_BASE_URL`. This repository uses an alternate URL for its own testing
because the default URL is too unstable. Mirrors can be found here:

http://download.qt.io/static/mirrorlist/

## Examples

*WIP*

https://github.com/nelsonjchen/barrier/tree/azure-pipelines

## Azure Pipelines

The script is tested against all currently stable and supported versions of
QT versions, host platforms, targets, and architectures.

The number of jobs is a bit insane but it's *all* tested to see if reasonable
targets to be downloaded and used on a platform can be installed.
E.g. iOS on a Mac and MSVC on Windows.

Because of this, **the `azure-pipelines.yml` in the root is generated!**
Install the packages in `.azure-pipelines/requirements.txt` and run
`.azure-pipelines/generate_azure_pipelines_yml.py` to regenerate
 `azure-pipelines.yml`.

## Original Repository and Other Forks

https://git.kaidan.im/lnj/qli-installer/blob/master/

This fork of this tool is hosted on GitHub:

https://github.com/nelsonjchen/qli-installer

After making this fork , I found another fork of lnjx's qli-installer
that also ported QLI Installer to Windows. 😒 If you're looking for a
version that's in PyPI and is also continuously tested on the target
platforms, look at `aqtinstall`:

https://pypi.org/project/aqtinstall/

It has parallel downloading and extraction support too!


[cuteci]: https://github.com/hasboeuf/cuteci/

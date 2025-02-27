#!/usr/bin/env python3
#
# Copyright (C) 2018 Linus Jahn <lnj@kaidan.im>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import concurrent.futures
import os
import shutil
import sys
import xml.etree.ElementTree as ElementTree
from os import getenv
from pathlib import Path

import requests

if len(sys.argv) != 6:
    print("Usage: {} <qt-version> <host> <target> <arch> <package_name>\n".format(sys.argv[0]))
    print("qt-version:   Qt version in the format of \"5.X.Y\"")
    print("host systems: linux, mac, windows")
    print("targets:      desktop, android, ios")
    exit(1)

base_url = getenv('QLI_BASE_URL', "https://download.qt.io/online/qtsdkrepository/")

# Qt version
qt_version = sys.argv[1]
qt_ver_num = qt_version.replace(".", "")
# one of: "linux", "mac", "windows"
os_name = sys.argv[2]
# one of: "desktop", "android", "ios"
target = sys.argv[3]

# Target architectures:
#
# linux/desktop:   "gcc_64"
# mac/desktop:     "clang_64"
# mac/ios:         "ios"
# windows/desktop: "win64_msvc2017_64", "win64_msvc2015_64",
#                  "win32_msvc2015", "win32_mingw53"
# */android:       "android_x86", "android_armv7"
arch = ""
if len(sys.argv) >= 5:
    arch = sys.argv[4]
elif os_name == "linux" and target == "desktop":
    arch = "gcc_64"
elif os_name == "mac" and target == "desktop":
    arch = "clang_64"
elif os_name == "mac" and target == "ios":
    arch = "ios"

if arch == "":
    print("Please supply a target architecture.")
    exit(1)

package_name=sys.argv[5]
package_name_tmpl1="qt.qt5.{}.{}.{}"
package_name_tmpl2="qt.{}.{}.{}"

# Build repo URL
packages_url = base_url
if os_name == "windows":
    packages_url += os_name + "_x86/"
else:
    packages_url += os_name + "_x64/"
packages_url += target + "/"
packages_url += "qt5_" + qt_ver_num + "/"

# Get packages index
update_xml_url = packages_url + "Updates.xml"
reply = requests.get(update_xml_url)
update_xml = ElementTree.fromstring(reply.content)

package_desc = ""
full_version = ""
archives = []
archives_url = ""
for packageupdate in update_xml.findall("PackageUpdate"):
    name = packageupdate.find("Name").text
    if name == package_name_tmpl1.format(qt_ver_num, package_name, arch) or name == package_name_tmpl2.format(qt_ver_num, package_name, arch):
        full_version = packageupdate.find("Version").text
        archives = packageupdate.find("DownloadableArchives").text.split(", ")
        package_desc = packageupdate.find("Description").text
        if ".qt5." in name:
            archives_url = packages_url + package_name_tmpl1.format(qt_ver_num, package_name, arch) + "/"
            break
        else:
            archives_url = packages_url + package_name_tmpl2.format(qt_ver_num, package_name, arch) + "/"
            break

if archives_url == "":
    print("not package found")
    exit(1)

if not full_version or not archives:
    print("Error while parsing package information!")
    exit(1)

print("****************************************")
print("Installing {}".format(package_desc))
print("****************************************")
print("HOST:      ", os_name)
print("TARGET:    ", target)
print("ARCH:      ", arch)
print("Source URL:", archives_url)
print("****************************************")


def download_file(target_url, local_filename):
    with requests.get(target_url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename


tmp_directory_path = Path(getenv('QLI_TMP_DIR', Path(Path(__file__).parent, 'tmp')))
tmp_directory_path.mkdir(parents=True, exist_ok=True)
out_directory_path = Path(getenv('QLI_OUT_DIR', Path(Path(__file__).parent, 'output')))
out_directory_path.mkdir(parents=True, exist_ok=True)


def download_extract_archive(archives_url, full_version, archive, tmp_directory_path, out_directory_path):
    url = archives_url + full_version + archive
    local_archive_path = Path(tmp_directory_path, archive)

    print(f"Downloading {archive}...")

    download_file(url, local_archive_path)

    print(f"Extracting {archive}...")
    os.system(f'7z x -y {local_archive_path} -o{out_directory_path}')
    os.remove(local_archive_path)


with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    jobs = [
        executor.submit(download_extract_archive, archives_url, full_version, archive, tmp_directory_path,
                        out_directory_path)
        for archive in archives
    ]
    for job in jobs:
        print(repr(job.result()))


print("Finished installation")

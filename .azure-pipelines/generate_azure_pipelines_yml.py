"""
This generates a matrix of QT versions to test downloading against
"""

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import List

from ruamel.yaml import YAML


@dataclass
class BuildJob:
    qt_version: str
    host: str
    target: str
    arch: str


@dataclass
class PlatformBuildJobs:
    platform: str
    build_jobs: List[BuildJob]


python_versions = [
    '3.7',
]

qt_versions = [
    '5.9.7',
    '5.11.3',
    '5.12.3',
    '5.13.0',
]

mobile_qt_versions = [
    '5.12.3',
    '5.13.0',
]

linux_build_jobs = []
mac_build_jobs = []
windows_build_jobs = []

all_platform_build_jobs = [
    PlatformBuildJobs('linux', linux_build_jobs),
    PlatformBuildJobs('mac', mac_build_jobs),
    PlatformBuildJobs('windows', windows_build_jobs),
]

# Linux Desktop

for qt_version in qt_versions:
    linux_build_jobs.append(
        BuildJob(qt_version, 'linux', 'desktop', 'gcc_64')
    )

# Mac Desktop

for qt_version in qt_versions:
    mac_build_jobs.append(
        BuildJob(qt_version, 'mac', 'desktop', 'clang_64')
    )

# Mac iOS
for qt_version in mobile_qt_versions:
    mac_build_jobs.append(
        BuildJob(qt_version, 'mac', 'ios', 'ios')
    )

# Windows Desktop

windows_build_jobs.extend(
    [

        BuildJob('5.9.8', 'windows', 'desktop', 'win64_msvc2017_64'),
        BuildJob('5.9.8', 'windows', 'desktop', 'win64_msvc2015_64'),
        BuildJob('5.9.8', 'windows', 'desktop', 'win64_msvc2013_64'),
        BuildJob('5.9.8', 'windows', 'desktop', 'win32_msvc2015'),
        BuildJob('5.9.8', 'windows', 'desktop', 'win32_mingw53'),
    ]
)

windows_build_jobs.extend(
    [
        BuildJob('5.11.3', 'windows', 'desktop', 'win64_msvc2017_64'),
        BuildJob('5.11.3', 'windows', 'desktop', 'win64_msvc2015_64'),
        BuildJob('5.11.3', 'windows', 'desktop', 'win32_msvc2015'),
        BuildJob('5.11.3', 'windows', 'desktop', 'win32_mingw53'),
    ]
)

windows_build_jobs.extend(
    [
        BuildJob('5.12.3', 'windows', 'desktop', 'win64_msvc2017_64'),
        BuildJob('5.12.3', 'windows', 'desktop', 'win64_msvc2015_64'),
        BuildJob('5.12.3', 'windows', 'desktop', 'win64_mingw73'),
        BuildJob('5.12.3', 'windows', 'desktop', 'win32_msvc2017'),
        BuildJob('5.12.3', 'windows', 'desktop', 'win32_mingw73'),
    ]
)

windows_build_jobs.extend(
    [
        BuildJob('5.13.0', 'windows', 'desktop', 'win64_msvc2017_64'),
        BuildJob('5.13.0', 'windows', 'desktop', 'win64_msvc2015_64'),
        BuildJob('5.13.0', 'windows', 'desktop', 'win64_mingw73'),
        BuildJob('5.13.0', 'windows', 'desktop', 'win32_msvc2017'),
        BuildJob('5.13.0', 'windows', 'desktop', 'win32_mingw73'),
    ]
)

# All Androids for all platforms

for qt_version in mobile_qt_versions:
    for android_arch in [
        'android_x86',
        'android_armv7',
    ]:
        for platform_build_jobs in all_platform_build_jobs:
            platform_build_jobs.build_jobs.append(
                BuildJob(qt_version, platform_build_jobs.platform, 'android', android_arch)
            )

matrices = {}

for platform_build_job in all_platform_build_jobs:
    yaml_dictionary = {
        'matrix': {}
    }
    for build_job, python_version in product(platform_build_job.build_jobs, python_versions):
        yaml_dictionary['matrix'][
            f'Python {python_version} QT {build_job.qt_version} {build_job.host} {build_job.target} {build_job.arch}'] = \
            {
                'PYTHON_VERSION': python_version,
                'QT_VERSION': build_job.qt_version,
                'HOST': build_job.host,
                'TARGET': build_job.target,
                'ARCH': build_job.arch,
                'QLI_BASE_URL': 'http://mirrors.ocf.berkeley.edu/qt/online/qtsdkrepository/',
            }
    matrices[platform_build_job.platform.capitalize()] = yaml_dictionary

# Load azure-pipelines.tmpl.yml
with open(Path(Path(__file__).parent, 'azure-pipelines.tmpl.yml'), 'r') as f:
    azure_pipelines_yaml = YAML().load(f.read())

# Attach strategies to their respective jobs
for job_yaml in azure_pipelines_yaml['jobs']:
    if job_yaml['job'] in matrices:
        job_yaml['strategy'] = matrices[job_yaml['job']]

with open(Path(Path(__file__).parent.parent, 'azure-pipelines.yml'), 'w') as f:
    YAML().dump(azure_pipelines_yaml, f)

pass

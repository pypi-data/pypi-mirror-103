# coding: utf-8
# Copyright 2021 yuncliu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
"""electronpy entry"""

import sys
import subprocess
import os

CUR_DIR = os.path.dirname(__file__)


def main_linux():
    x=[os.path.join(CUR_DIR, "electron", "electron")]
    x.extend(sys.argv[1:])
    if os.getuid() == 0:
        x.append('--no-sandbox')
    pid = os.fork()
    try:
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.exit(0)

    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.exit(0)
    subprocess.Popen(x)


def main_win32():
    x=[os.path.join(CUR_DIR, "electron", "electron.exe")]
    x.extend(sys.argv[1:])
    pid = subprocess.Popen(x, shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
            subprocess.DETACHED_PROCESS)

def main():
    if sys.platform.lower() == 'win32':
        main_win32()
    else:
        main_linux()

if __name__ == '__main__':
    main()

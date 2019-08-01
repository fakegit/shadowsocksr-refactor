#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor.
 @file: require.py

 Copyright 2019 valord577

 Licensed under the Apache License, Version 2.0 (the "License"); you may
 not use this file except in compliance with the License. You may obtain
 a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.
"""

import sys
import select


def check_os():
    if 'linux' != sys.platform:
        print(' Note: Only support Linux.')
        sys.exit(1)

    if not hasattr(select, 'epoll'):
        print(' Note: Require \'epoll\' model.')
        sys.exit(1)


def check_python():
    info = sys.version_info

    if info[0] not in [2, 3]:
        print(' Error: Python 3.6+ required.')
        sys.exit(1)

    # deprecate Python 2.x
    if info[0] == 2:
        print(' Error: Python 2.x Deprecated. Use 3.6+ instead.')
        sys.exit(1)

    if info[0] == 3 and not info[1] >= 6:
        print(' Error: Python 3.6+ required.')
        sys.exit(1)

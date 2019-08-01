#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: clowwindy
 @modify: valor.
 @file: conf.py (renamed from 'version.py')

 Copyright 2017 breakwa11
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


def version() -> str:
    return 'ShadowsocksR-Refactor [server] v4.1.0 Snapshot at 2019-08-01.'


# @return:  the path of ssr conf file
def ssr_conf_path ()-> str:
    # relative path
    # or you can use absolute path
    return 'user-config.json'


def logger_init():
    import logging
    logging.basicConfig(level=1,
                        format='%(asctime)s [%(levelname)-8s] :%(lineno)-4d %(filename)-20s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def help_msg() -> str:
    return '''Usage: ShadowsocksR-Refactor [server]...
A fast tunnel proxy that helps you bypass firewalls.

You can supply configurations via a configuration file (json file) only.

General options:
  -h, --help             show this help message and exit
  -v, --version          show version information

Online help: <https://github.com/valord577/shadowsocksr-refactor>
'''

#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor.
 @file: args.py

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
import getopt
# -- import from shadowsockesr-v
import conf
import exit


def check():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hv', ['help', 'version'])
        for opt, param in opts:
            if opt in ('-h', '--help'):
                print(conf.help_msg())
                exit.ok()
            if opt in ('-v', '--version'):
                print(conf.version())
                exit.ok()
    except getopt.GetoptError:
        print(' Error: args checked.')
        print(conf.help_msg())
        exit.error()

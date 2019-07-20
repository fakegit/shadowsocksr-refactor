#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor.
 @file: logger.py

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

import logging
import conf

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


def init():
    if conf.print_console():
        return

    # if running on the server, config logger
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


# @msg:   logs
# @level: logging level, such as logging.ERROR
def out(msg, level: int):
    if conf.print_console():
        print(msg)
    else:
        # if running on the server, record logs
        logging.log(level, msg)


def error(msg):
    out(msg, ERROR)


def warning(msg):
    out(msg, WARNING)


def info(msg):
    out(msg, INFO)


def debug(msg):
    out(msg, DEBUG)

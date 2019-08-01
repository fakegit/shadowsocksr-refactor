#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor.
 @file: utils.py

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

import os
from typing import Dict
# -- import from shadowsockesr-v
from common import is_blank
import exit


def check_file_path(file: str):
    if is_blank(file):
        exit.error(f'Blank file path. [arg -> {file}]')

    if not os.path.exists(file):
        exit.error('Not found file.')


def parse_json(file: str) -> Dict:
    import json

    d = {}
    with open(file=file, encoding='utf-8') as f:
        d = json.load(f)
        f.close()

    return d


def parse_xml(file: str) -> Dict:
    import xml.etree.cElementTree as xmlParser

    check_file_path(file)
    root = xmlParser.ElementTree(file=file).getroot()

    # get configurations
    conf = {}
    # parse xml file
    traversing_nodes(root, conf)
    return conf[root.tag]


# recursive
def traversing_nodes(node, conf: Dict):
    # no child, insert node into Dict
    if len(node) == 0:
        if not conf.__contains__(node.tag):
            conf[node.tag] = node.text
        else:
            # convert value to list
            if isinstance(conf[node.tag], list):
                conf[node.tag].append(node.text)
            else:
                conf[node.tag] = [conf[node.tag], node.text]
        return

    if not conf.__contains__(node.tag):
        conf[node.tag] = {}
        _temp_dict = conf[node.tag]
    else:
        if isinstance(conf[node.tag], list):
            conf[node.tag].append({})
        else:
            conf[node.tag] = [conf[node.tag], {}]
        _temp_dict = conf[node.tag][len(conf[node.tag]) - 1]

    for elem in list(node):
        traversing_nodes(elem, _temp_dict)

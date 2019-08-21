#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: clowwindy
 @modify: valor.
 @file: shell.py

 Copyright 2015 clowwindy
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

from typing import Dict
# -- import from shadowsockesr-v
import encrypt
import common
import exit
import utils


def get_ssr_conf(ssr_conf_path: str) -> Dict:
    _ssr_conf: Dict = utils.parse_json(ssr_conf_path)

    if not _ssr_conf:
        exit.error('Require ssr-config.')

    # -- check params --
    port = _ssr_conf.get('server_port')
    if port is None:
        exit.error('Require \'server_port\'.')
    if type(port) != int or port <= 0:
        exit.error('Illegal \'server_port\'.')

    password = _ssr_conf.get('password')
    if common.is_blank(password):
        exit.error('Require \'password\'.')

    method = _ssr_conf.get('method')
    if common.is_blank(method):
        exit.error('Require \'method\'.')
    if not encrypt.is_supported(method):
        exit.error(f'Not supported method [{method}]')

    protocol = _ssr_conf.get('protocol')
    if common.is_blank(protocol):
        exit.error('Require \'protocol\'.')

    obfs = _ssr_conf.get('obfs')
    if common.is_blank(obfs):
        exit.error('Require \'obfs\'.')

    dns_list = _ssr_conf.get('dns')
    if dns_list is None or type(dns_list) != list or len(dns_list) == 0:
        exit.error('Require \'dns server\'.')
    for dns in dns_list:
        host = dns.get('host')
        if ':' in host:
            exit.error("Not support ipv6 dns host.")
        if not common.is_ipv4(host):
            exit.error("Illegal ipv4 dns host.")

    # -- default params --
    _ssr_conf['server'] = '::'
    _ssr_conf['password'] = common.to_bytes(_ssr_conf['password'])
    _ssr_conf['protocol_param'] = _ssr_conf.get('protocol_param', '')
    _ssr_conf['obfs_param'] = _ssr_conf.get('obfs_param', '')

    # process default data
    try:
        _ssr_conf['forbidden_ip'] = \
            common.IPNetwork(_ssr_conf.get('forbidden_ip', '127.0.0.0/8,::1/128'))
    except Exception as e:
        exit.error('error configuration \'forbidden_ip\'.')
    try:
        _ssr_conf['forbidden_port'] = common.PortRange(_ssr_conf.get('forbidden_port', ''))
    except Exception as e:
        exit.error('error configuration \'forbidden_port\'.')
    try:
        _ssr_conf['ignore_bind'] = \
            common.IPNetwork(_ssr_conf.get('ignore_bind', '127.0.0.0/8,::1/128,10.0.0.0/8,192.168.0.0/16'))
    except Exception as e:
        exit.error('error configuration \'ignore_bind\'.')

    return _ssr_conf

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
import logger
import encrypt
import common
import exit
import utils


def check_config(config: Dict, is_local: bool):
    if is_local and not config.get('password'):
        exit.error('password not defined.')

    if not is_local and not config.get('password') \
            and not config.get('port_password'):
        exit.error('password or port_password not defined.')

    if config.get('local_address') == '0.0.0.0':
        logger.warning('warning: local set to listen on 0.0.0.0, it\'s not safe')
    if config.get('server') in ['127.0.0.1', 'localhost']:
        logger.warning('warning: server set to listen on %s:%s, are you sure?'
                        % (common.to_str(config['server']), config['server_port']))
    if config.get('timeout') < 100:
        logger.warning('warning: your timeout %d seems too short'
                        % int(config.get('timeout')))
    if config.get('timeout') > 600:
        logger.warning('warning: your timeout %d seems too long'
                        % int(config.get('timeout')))

    encrypt.try_cipher(config['password'], config['method'])


def get_ssr_conf(is_local: bool, ssr_conf_path: str):
    _ssr_conf: Dict = utils.parse_json(ssr_conf_path)

    if not _ssr_conf:
        exit.error('ssr-config not defined.')

    # process default data
    if is_local:
        if _ssr_conf.get('server') is None:
            exit.error('server addr not defined.')
        else:
            _ssr_conf['server'] = common.to_str(_ssr_conf['server'])
    else:
        _ssr_conf['server'] = common.to_str(_ssr_conf.get('server', '0.0.0.0'))
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

    _ssr_conf['server_port'] = int(_ssr_conf.get('server_port', 8388))
    _ssr_conf['local_address'] = common.to_str(_ssr_conf.get('local_address', '127.0.0.1'))
    _ssr_conf['local_port'] = int(_ssr_conf.get('local_port', 1080))
    _ssr_conf['password'] = common.to_bytes(_ssr_conf.get('password', b''))
    _ssr_conf['method'] = common.to_str(_ssr_conf.get('method', 'aes-128-ctr'))
    _ssr_conf['protocol'] = common.to_str(_ssr_conf.get('protocol', 'auth_aes128_md5'))
    _ssr_conf['protocol_param'] = common.to_str(_ssr_conf.get('protocol_param', ''))
    _ssr_conf['obfs'] = common.to_str(_ssr_conf.get('obfs', 'tls1.2_ticket_auth'))
    _ssr_conf['obfs_param'] = common.to_str(_ssr_conf.get('obfs_param', ''))
    _ssr_conf['port_password'] = None
    _ssr_conf['additional_ports'] = _ssr_conf.get('additional_ports', {})
    _ssr_conf['additional_ports_only'] = \
        _ssr_conf.get('additional_ports_only') is not None and 'true' == _ssr_conf.get('additional_ports_only')
    _ssr_conf['timeout'] = int(_ssr_conf.get('timeout', 120))
    _ssr_conf['udp_timeout'] = int(_ssr_conf.get('udp_timeout', 60))
    _ssr_conf['udp_cache'] = int(_ssr_conf.get('udp_cache', 64))
    _ssr_conf['fast_open'] = _ssr_conf.get('fast_open') is not None and 'true' == _ssr_conf.get('fast_open')
    _ssr_conf['workers'] = _ssr_conf.get('workers', 1)
    _ssr_conf['pid-file'] = _ssr_conf.get('pid-file', '/var/run/shadowsocksr.pid')
    _ssr_conf['log-file'] = _ssr_conf.get('log-file', '/var/log/shadowsocksr.log')
    _ssr_conf['verbose'] = _ssr_conf.get('verbose') is not None and 'true' == _ssr_conf.get('verbose')
    _ssr_conf['connect_verbose_info'] = _ssr_conf.get('connect_verbose_info', 0)

    check_config(_ssr_conf, is_local)
    return _ssr_conf

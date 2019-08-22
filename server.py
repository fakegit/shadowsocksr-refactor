#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
 @author: clowwindy
 @modify: valor.
 @file: server.py

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


def main():
    import logging
    # -- import from shadowsockesr-v
    import conf
    import exit
    import shell
    import eventloop
    import tcprelay
    import udprelay
    import asyncdns

    # -- init logging --
    conf.logger_init()
    # show version
    logging.info(conf.version())

    # -- starting ssr --
    # get ssr configurations
    ssr_conf = shell.get_ssr_conf(ssr_conf_path=conf.ssr_conf_path())

    if not ssr_conf.get('dns_ipv6', False):
        asyncdns.IPV6_CONNECTION_SUPPORT = False

    password = ssr_conf['password']
    method = ssr_conf['method']
    protocol = ssr_conf['protocol']
    protocol_param = ssr_conf['protocol_param']
    obfs = ssr_conf['obfs']
    obfs_param = ssr_conf['obfs_param']
    udp_enable = ssr_conf['udp_enable']
    dns_list = ssr_conf['dns']

    logging.info(f'Server start with '
                 f'password [{password}] '
                 f'method [{method}] '
                 f'protocol[{protocol}] '
                 f'protocol_param[{protocol_param}] '
                 f'obfs [{obfs}] '
                 f'obfs_param [{obfs_param}]')

    server = ssr_conf['server']
    port = ssr_conf['server_port']
    logging.info(f'Starting server at [{server}]:{port}')

    try:
        ssr_conf['out_bind'] = ''
        ssr_conf['out_bindv6'] = ''

        # create epoll (singleton)
        loop = eventloop.EventLoop()

        # dns server (singleton)
        dns_resolver = asyncdns.DNSResolver(dns_list)
        dns_resolver.add_to_loop(loop)

        stat_counter_dict = {}
        # listen tcp && register socket
        tcp = tcprelay.TCPRelay(ssr_conf, dns_resolver, stat_counter=stat_counter_dict)
        tcp.add_to_loop(loop)

        if udp_enable:
            # listen udp && register socket
            udp = udprelay.UDPRelay(ssr_conf, dns_resolver, False, stat_counter=stat_counter_dict)
            udp.add_to_loop(loop)

        # run epoll to handle socket
        loop.run()
    except Exception as e:
        exit.error(e)


if __name__ == '__main__':
    # -- require --
    import require
    # only support Linux and require 'epoll' model.
    require.check_os()
    # Python 2.x Deprecated. Use 3.6+ instead.
    require.check_python()

    import args
    # -- check args --
    args.check()

    # -- do main func --
    main()

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
    import sys
    import os
    import signal
    import resource
    # -- import from shadowsockesr-v
    import logger
    import conf
    import exit
    import shell, daemon, eventloop, tcprelay, udprelay, asyncdns, common

    # get ssr configurations
    ssr_conf = shell.get_ssr_conf(is_local=False, ssr_conf_path=conf.configuration_path())

    # start daemon
    daemon.daemon_exec(ssr_conf)

    logger.info('current process open files[cmd\'ulimit -n\'] resource: soft %d hard %d' %
                 resource.getrlimit(resource.RLIMIT_NOFILE))

    # todo Multiport -> Single port
    if not ssr_conf['port_password']:
        ssr_conf['port_password'] = {}

        server_port = ssr_conf['server_port']
        if type(server_port) == list:
            for a_server_port in server_port:
                ssr_conf['port_password'][a_server_port] = ssr_conf['password']
        else:
            ssr_conf['port_password'][str(server_port)] = ssr_conf['password']

    if not ssr_conf.get('dns_ipv6', False):
        asyncdns.IPV6_CONNECTION_SUPPORT = False

    # no used
    # if config.get('manager_address', 0):
    #     logging.info('entering manager mode')
    #     manager.run(config)
    #     return

    tcp_servers = []
    udp_servers = []
    dns_resolver = asyncdns.DNSResolver()
    if int(ssr_conf['workers']) > 1:
        stat_counter_dict = None
    else:
        stat_counter_dict = {}
    port_password = ssr_conf['port_password']
    config_password = ssr_conf.get('password', 'm')
    del ssr_conf['port_password']
    for port, password_obfs in port_password.items():
        method = ssr_conf["method"]
        protocol = ssr_conf.get("protocol", 'origin')
        protocol_param = ssr_conf.get("protocol_param", '')
        obfs = ssr_conf.get("obfs", 'plain')
        obfs_param = ssr_conf.get("obfs_param", '')
        bind = ssr_conf.get("out_bind", '')
        bindv6 = ssr_conf.get("out_bindv6", '')
        if type(password_obfs) == list:
            password = password_obfs[0]
            obfs = common.to_str(password_obfs[1])
            if len(password_obfs) > 2:
                protocol = common.to_str(password_obfs[2])
        elif type(password_obfs) == dict:
            password = password_obfs.get('password', config_password)
            method = common.to_str(password_obfs.get('method', method))
            protocol = common.to_str(password_obfs.get('protocol', protocol))
            protocol_param = common.to_str(password_obfs.get('protocol_param', protocol_param))
            obfs = common.to_str(password_obfs.get('obfs', obfs))
            obfs_param = common.to_str(password_obfs.get('obfs_param', obfs_param))
            bind = password_obfs.get('out_bind', bind)
            bindv6 = password_obfs.get('out_bindv6', bindv6)
        else:
            password = password_obfs
        a_config = ssr_conf.copy()
        ipv6_ok = False
        logger.info("server start with protocol[%s] password [%s] method [%s] obfs [%s] obfs_param [%s]" %
                (protocol, password, method, obfs, obfs_param))
        if 'server_ipv6' in a_config:
            try:
                if len(a_config['server_ipv6']) > 2 and a_config['server_ipv6'][0] == "[" and a_config['server_ipv6'][-1] == "]":
                    a_config['server_ipv6'] = a_config['server_ipv6'][1:-1]
                a_config['server_port'] = int(port)
                a_config['password'] = password
                a_config['method'] = method
                a_config['protocol'] = protocol
                a_config['protocol_param'] = protocol_param
                a_config['obfs'] = obfs
                a_config['obfs_param'] = obfs_param
                a_config['out_bind'] = bind
                a_config['out_bindv6'] = bindv6
                a_config['server'] = a_config['server_ipv6']
                logger.info("starting server at [%s]:%d" %
                             (a_config['server'], int(port)))
                tcp_servers.append(tcprelay.TCPRelay(a_config, dns_resolver, False, stat_counter=stat_counter_dict))
                udp_servers.append(udprelay.UDPRelay(a_config, dns_resolver, False, stat_counter=stat_counter_dict))
                if a_config['server_ipv6'] == '::':
                    ipv6_ok = True
            except Exception as e:
                logger.error(e)

        try:
            a_config = ssr_conf.copy()
            a_config['server_port'] = int(port)
            a_config['password'] = password
            a_config['method'] = method
            a_config['protocol'] = protocol
            a_config['protocol_param'] = protocol_param
            a_config['obfs'] = obfs
            a_config['obfs_param'] = obfs_param
            a_config['out_bind'] = bind
            a_config['out_bindv6'] = bindv6
            logger.info("starting server at %s:%d" %
                         (a_config['server'], int(port)))
            tcp_servers.append(tcprelay.TCPRelay(a_config, dns_resolver, False, stat_counter=stat_counter_dict))
            udp_servers.append(udprelay.UDPRelay(a_config, dns_resolver, False, stat_counter=stat_counter_dict))
        except Exception as e:
            if not ipv6_ok:
                logger.error(e)

    def run_server():
        def child_handler(signum, _):
            logger.warning('received SIGQUIT, doing graceful shutting down..')
            list(map(lambda s: s.close(next_tick=True),
                     tcp_servers + udp_servers))
        signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM),
                      child_handler)

        def int_handler(signum, _):
            sys.exit(1)
        signal.signal(signal.SIGINT, int_handler)

        try:
            loop = eventloop.EventLoop()
            dns_resolver.add_to_loop(loop)
            list(map(lambda s: s.add_to_loop(loop), tcp_servers + udp_servers))

            daemon.set_user(ssr_conf.get('user', None))
            loop.run()
        except Exception as e:
            exit.error(e)

    if int(ssr_conf['workers']) > 1:
        if os.name == 'posix':
            children = []
            is_child = False
            for i in range(0, int(ssr_conf['workers'])):
                r = os.fork()
                if r == 0:
                    logger.info('worker started')
                    is_child = True
                    run_server()
                    break
                else:
                    children.append(r)
            if not is_child:
                def handler(signum, _):
                    for pid in children:
                        try:
                            os.kill(pid, signum)
                            os.waitpid(pid, 0)
                        except OSError:  # child may already exited
                            pass
                    sys.exit()
                signal.signal(signal.SIGTERM, handler)
                signal.signal(signal.SIGQUIT, handler)
                signal.signal(signal.SIGINT, handler)

                # master
                for a_tcp_server in tcp_servers:
                    a_tcp_server.close()
                for a_udp_server in udp_servers:
                    a_udp_server.close()
                dns_resolver.close()

                for child in children:
                    os.waitpid(child, 0)
        else:
            logger.warning('worker is only available on Unix/Linux')
            run_server()
    else:
        run_server()


if __name__ == '__main__':
    # -- require --
    import require
    # only support 'posix'(Linux/Darwin).
    require.check_os()
    # Python 2.x Deprecated. Use 3.6+ instead.
    require.check_python()

    import args
    # -- check args --
    args.check()

    # -- init --
    import logger
    logger.init()
    # show version
    import conf
    logger.info(conf.version())

    # -- do main func --
    main()

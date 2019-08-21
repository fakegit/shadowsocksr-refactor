ShadowsocksR - Refactor
===========

A fast tunnel proxy that helps you bypass firewalls.

Info
------

|Edition |Change logs |Latest Out |
|:----- |:------ |:------ |
|Server |[Change logs](CHANGES) |v4.1.1 Snapshot at 2019-08-21 |

Require
------

* Python 3.6+
* Linux && Require 'epoll' model

Usage
------

#### Get python source code

    # clone this branch via git
    git clone -b refactor-server https://github.com/valord577/shadowsocksr-refactor.git
    
    # or download as zip file and unzip it

#### Initialize the project

    # change directory into the root path of project and initialize the project
    cd ./shadowsocksr-refactor && bash initcfg.sh

#### Edit the configuration file

    # ./conf/config.json is just a template
    # editting ./user-config.json is ok
    vi user-config.json
    
    # then save it

#### Running and stopping

    # running
    bash run.sh
    
    # stopping
    bash stop.sh

#### Tail logs file

    tail -500f ssr-refactor.log

GUI Client
------

Use GUI clients on your local PC/phones.

Check the README of your client for more information.

* [Windows](https://github.com/shadowsocksr-backup/shadowsocksr-csharp)
* [MacOS](https://github.com/qinyuhang/ShadowsocksX-NG-R/releases)
* [Android](https://github.com/shadowsocksr-backup/shadowsocksr-android)
* [Linux](https://github.com/qingshuisiyuan/electron-ssr-backup)
* IOS (App named 'Shadowrocket', Non-Chinese mainland)

License
-------

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

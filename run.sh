#!/bin/bash

ulimit -n 65535 && nohup python3 server.py a > ssr-refactor.log 2>&1 &

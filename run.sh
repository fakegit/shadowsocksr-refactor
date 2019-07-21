#!/bin/bash

ulimit -n 512000 && nohup python3 server.py a > ssr-refactor.log 2>&1 &
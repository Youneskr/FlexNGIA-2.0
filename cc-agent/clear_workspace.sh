#!/bin/bash

sudo rm -rf results/* 2>/dev/null
sudo rm -rf analysis/images/* 2>/dev/null
sudo rm -rf agent/traces/* 2>/dev/null
sudo rm -rf agent/workspace
sudo rm -f "clock.log"
sudo ./clock.sh clear >/dev/null 2>&1
mkdir -p agent/workspace
mkdir -p agent/traces/repo

#!/bin/bash

sudo rm -rf results/* 2>/dev/null
sudo rm -rf analysis/images/* 2>/dev/null
sudo rm -rf agent/traces/* 2>/dev/null
sudo rm -rf agent/workspace
mkdir -p agent/workspace
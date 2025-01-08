#!/bin/bash
rsync -avz -e "ssh -p 3022" --delete k8s/ root@external.lab00:/k8s/

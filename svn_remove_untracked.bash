#!/usr/bin/env bash

svn st | grep '^?' | awk '{print $2}' | xargs -I{} rm -rf '{}'

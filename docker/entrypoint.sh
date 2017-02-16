#!/bin/bash

if [[ $@ == *"--export"* ]]; then
  grip $@
else
  grip /export 0.0.0.0:80  $@
fi

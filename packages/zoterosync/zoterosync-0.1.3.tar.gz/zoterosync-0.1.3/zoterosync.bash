#!/bin/bash

if [ -f ".env" ]; then
  . .env
else
  ZOTEROSYNC_PATH="$HOME/.zoterosync"
fi
mkdir -p $ZOTEROSYNC_PATH
cd "$ZOTEROSYNC_PATH"

if [ -f "bin/activate" ]; then
	source bin/activate
	python zoterosync_cli.py "$@"
else
	echo "virtualenv not installed"
fi

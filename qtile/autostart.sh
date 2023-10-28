#!/bin/bash

xinput set-prop "ELAN1200:00 04F3:3067 Touchpad" "libinput Tapping Enabled" 1

dunst &

if ! [[ $(pgrep nm-applet 2> /dev/null) ]]; then
  nm-applet --indicator &
fi

if ! [[ $(pgrep picom 2> /dev/null) ]]; then
  picom --no-vsync &
fi

#!/bin/bash

xinput set-prop "ELAN1200:00 04F3:3067 Touchpad" "libinput Tapping Enabled" 1

dunst &

flameshot &

nm-applet --indicator &

picom --no-vsync &

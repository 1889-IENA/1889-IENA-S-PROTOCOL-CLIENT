#!/bin/bash


clear


read -p "Root or Normal? ( R / N )" user_choice


if [ "$user_choice" = "R" ]; then
    sudo .venv/bin/python "v4.0.0/IENA_Client.py"
elif [ "$user_choice" = "N" ]; then
    .venv/bin/python "v4.0.0/IENA_Client.py"
fi

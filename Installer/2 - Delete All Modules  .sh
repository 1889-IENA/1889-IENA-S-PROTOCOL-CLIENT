#!/bin/bash


clear


.venv/bin/python -m pip uninstall -r "Installer/Module_List/requirements.txt" -y


read -n 1 -s -r -p "Done"

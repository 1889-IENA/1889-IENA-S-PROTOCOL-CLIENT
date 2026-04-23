#!/bin/bash


clear


.venv/bin/ruff check "v4.0.0/PROTOCOL/CONNECTOR/S_Connection.py"


.venv/bin/ruff check "v4.0.0/PROTOCOL/S/S_Admin.py"
.venv/bin/ruff check "v4.0.0/PROTOCOL/S/S_Login.py"
.venv/bin/ruff check "v4.0.0/PROTOCOL/S/S_Missions.py"
.venv/bin/ruff check "v4.0.0/PROTOCOL/S/S_Profile.py"
.venv/bin/ruff check "v4.0.0/PROTOCOL/S/S_Redirect.py"


read -n 1 -s -r -p "Done"

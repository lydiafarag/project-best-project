#!/bin/bash
#here we kill any existing tmux sessions
#tmux kill-server
#enter into the project
cd project-best-project
git fetch && git reset origin/main --hard

#enter python venv and install subsequent dependancies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

#starting flask in a detached tmux session
#tmux new-session -d -s Flask
#tmux send-keys 'source python3-virtualenv/bin/activate' C-m
#tmux send-keys 'flask run --host=0.0.0.0' C-m
#tmux detach -s Flask
systemctl daemon-reload
systemctl restart myportfolio

#!/bin/bash

# Check if script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root."
    echo "I didn't do anything."
    exit 1
fi

# set defaults (may be changed if not available)
port='4200'
host='0.0.0.0'
user='gm'
appname='GradeMan'

echo "installing $appname..."

# Install necessary dependencies
apt-get update
apt-get install -y $(cat requirements.txt)

# Create appuser
useradd -m $user

# Copy app to /home/appuser/appname directory
mkdir -p /home/$user/$appname
for file in ./*; do
  if [[ ! "$file" =~ \.conf$ ]] && [[ ! "$file" =~ \.sqlite3$ ]] && [[ "$file" != *"__pycache__"* ]]; then
    cp -r "$file" "/home/$user/$appname"
  fi
done
#cp -r * /home/$user/$appname

# Change ownership to appuser
chown -R $user:$user /home/$user

# Create (or renew) systemd service file
rm /etc/systemd/system/$appname.service
cat > /etc/systemd/system/$appname.service <<EOL
[Unit]
Description=$appname
After=network.target

[Service]
User=$user
Group=$user
WorkingDirectory=/home/$user/$appname
ExecStart=waitress-serve --host=$host --port=$port app:$appname
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd daemon
systemctl daemon-reload

# Enable and (re-)start app service
systemctl enable $appname
systemctl restart $appname

import subprocess
import os

def zabbix_agent():
    # Update package repository and install required packages
    subprocess.run(['wget', 'https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb'])
    subprocess.run(['sudo', 'dpkg', '-i', 'zabbix-release_6.4-1+ubuntu22.04_all.deb'])
    subprocess.run(['sudo', 'apt', 'update', '-y'])

    subprocess.run(['sudo', 'apt', 'install', 'zabbix-agent', '-y'])
    subprocess.run(['systemctl', 'restart', 'zabbix-agent'])
    subprocess.run(['systemctl', 'enable', 'zabbix-agent'])
    subprocess.run(['systemctl', 'status', 'zabbix-agent'])

    #subprocess.run(['sudo', 'apt', 'update', '-y'])


if __name__ == "__main__":
    zabbix_agent()



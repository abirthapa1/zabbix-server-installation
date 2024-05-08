import subprocess
#import os
import re
import time
def zabbix_server_installation():
    
    try:
        # Update package repository and install required packages
        subprocess.run(['wget', 'https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb'])
        subprocess.run(['sudo', 'dpkg', '-i', 'zabbix-release_6.4-1+ubuntu22.04_all.deb'])
        subprocess.run(['sudo', 'apt', 'update', '-y'])
        
        #installing the required packages
        subprocess.run(['sudo', 'apt', 'install', 'zabbix-server-mysql', 'zabbix-frontend-php', 'zabbix-apache-conf', 'zabbix-sql-scripts', 'zabbix-agent', '-y'])
        
        #checking if mysql installed or not
        check_mysql_installed()

        print("\n<--------Connecting to MySQL Server...------------>\n")
        time.sleep(2)

        subprocess.run(['sudo', 'mysql', '-e', 'create', 'database', 'zabbix', 'character', 'set', 'utf8mb4', 'collate', 'utf8mb4_bin;'])

        password = input("\nEnter the database password: ")

        #updating the password in the mysql which would have a user
        #zabbix running in localhost
        subprocess.run(['sudo', 'mysql', '-e', 'create', 'user', 'zabbix@localhost', 'identified', 'by',  f'{password};'])

        #granting all the privileges to the user we created in previous step
        subprocess.run(['sudo', 'mysql', '-e', 'grant', 'all', 'privileges', 'on', 'zabbix.*', 'to', 'zabbix@localhost;'])

        subprocess.run(['sudo', 'mysql', '-e', 'set', 'global', 'log_bin_trust_function_creators', '=', '1;'])

        #On Zabbix server host import initial schema and data. You will be prompted to enter your newly created password.
        subprocess.run(['sudo', 'mysql', '-e', 'zcat', '/usr/share/zabbix-sql-scripts/mysql/server.sql.gz', '|', 'mysql', '--default-character-set=utf8mb4', '-uzabbix', '-p', 'zabbix'])

        subprocess.run(['sudo', 'mysql', '-e', 'set', 'global', 'log_bin_trust_function_creators', '=', '0;'])

        #opening the file zabbix_server.conf file
        edit_zabbix_server_conf()

        time.sleep(2)

        #Start Zabbix server and agent processes and make it start at system boot.
        subprocess.run(['sudo', 'systemctl', 'restart', 'zabbix-server', 'zabbix-agent', 'apache2'])
        subprocess.run(['sudo', 'systemctl', 'enable', 'zabbix-server', 'zabbix-agent', 'apache2'])

        #check the status of the services
        subprocess.run(['sudo', 'systemctl', 'status', 'zabbix-server', 'zabbix-agent', 'apache2'])

    except subprocess.CalledProcessError as e:
        print("Error:", e)

    finally:
        print("Process complete.")

#checking if mysql is installed or not
def check_mysql_installed():
    try:
        #checks if which mysql throws a non zero status meaning mysql not installed or not
        subprocess.run(["which", "mysql"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("--------------------- MYSQL INSATLLED ALREADY -----------------------\n\n")

    
    except subprocess.CalledProcessError as e:
        
        #starts installing mysql
        print("Couldn't find mysql so trying to install")
        try:
            print("<------------------------Installing Mysql---------------------------->\n\n")
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install mysql-server'])
            subprocess.run(['sudo', 'systemctl',' start', ' mysql.service'])
        
        #Error installing mysql
        except subprocess.CalledProcessError as e:
            print("Error installing mysql", e)

def edit_zabbix_server_conf():
    try:
        #defining the zabbix_server.conf file path"
        filename = '/etc/zabbix/zabbix_server.conf'

        password = input("\nEnter the database password entered before: ")
        
        # Opening our text file in read only 
        # mode using the open() function 
        with open(filename, 'r') as file:
            
            # Reading the content of the file 
            # using the read() function and storing 
            # them in a new variable 
            data = file.read()
            
            #Defining the pattern where we are going to make the changes
            pattern = "DBPassword\s*=.*"

            #updating the content of the variable data with the inputed password
            updated_password = re.sub(pattern, f'DBPassword={password}', data)


        #writing the updated password to the file
        with open(filename, 'w') as file:
            file.write(updated_password)
    
    #no such file exists
    except FileNotFoundError:
        print("-------------------------------NO SUCH FILE--------------------------------")        

if __name__ == "__main__":
    zabbix_server_installation()



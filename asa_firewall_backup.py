#!/usr/bin/python3
#multi context ASA firewall backup 
from netmiko import ConnectHandler
import sys
import os
import time
import datetime
import shutil
import getpass

username = input('Username: ')
password = getpass.getpass('Password: ')
secret   = getpass.getpass('Enable: ')

ftp_server = 'ftp_ip'
ftp_location = '/'
backup_location = '/root/Network_Device_Backups/ASA/'


cisco_asa = {
    'device_type': 'cisco_asa',
    'host': 'asa_ip',
    'username': username,
    'password': password,
    'secret': secret,
}



 


try:
    net_connect = ConnectHandler(**cisco_asa)
except:
    print >> sys.stderr, "Unable to connec to ASA."
    sys.exit(1)

net_connect.enable()

change_to_sys = "changeto system"
result0 = net_connect.send_command_timing(change_to_sys)

context_list=['admin', 'context_A' , 'context_B']  #context_name

for j in context_list:
    
    backup_command = "backup context "+j +" location ftp:"
    
    result = net_connect.send_command_timing(backup_command)
    backup_filename = j+'_FW-MELLAT-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.tar.gz'
    print(backup_filename)
    ftp_url = 'ftp://test:123456@10.5.224.18/'+backup_filename

    if '[Press return to continue or enter a backup location]:' in result:
       result += net_connect.send_command_timing(ftp_url)
    
    file_path = ftp_location+backup_filename

    while not os.path.exists(file_path):
        os.makedirs(file_path)
        time.sleep(10)

    if os.path.isfile(file_path):
        shutil.move(file_path, backup_location)


net_connect.exit_enable_mode()
net_connect.disconnect()


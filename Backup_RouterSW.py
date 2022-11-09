#!/usr/bin/python3

from netmiko import ConnectHandler
import os
import time
import datetime
import json
import getpass

username = input('Username: ')
password = getpass.getpass('Password: ')
#secret   = getpass.getpass('Enable: ')

device_list = 'router.json'
backup_filename = 'RTR-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'
vlan_filename = 'RTR-Show-VLAN-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
cdp_filename = 'RTR-Show-CDP-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
status_filename = 'RTR-Interface-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
lag_filename = 'RTR-LAG-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
arp_filename = 'RTR-ARP-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'


with open(device_list) as json_file:
    data = json.load(json_file)
    # Change data['router_list'] to data['switch_list'] if you are using switch.json
    for router in data['router_list']:
        cisco = {
    	    'device_type': 'cisco_ios',
    	    'host':   router['ip'],
    	    'username': username,    # Provide SSH username
    	    'password': password,    # Provide SSH password
    	    #'secret': secret,     # Optional, defaults to ''
	    }

        try:
            net_connect = ConnectHandler(**cisco)
        except:
                continue

        net_connect.enable()

        output_run_config = net_connect.send_command("show running-config")
        output_vlan = net_connect.send_command("show vlan brief")
        output_cdp = net_connect.send_command("show cdp neighbor")
        output_status = net_connect.send_command("show ip inter brief")
        output_lag = net_connect.send_command("show etherchannel summary ")
        output_arp = net_connect.send_command("show ip arp")

        net_connect.exit_enable_mode()
        net_connect.disconnect()

        #Create a separate directory for each device if not exists.
        backup_dir = '/root/Datacenter_Backups/Router/'+router['hostname']
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        #Write the device running-config to a file.
        f0 = open(backup_dir+'/'+backup_filename, 'w')
        f0.write(output_run_config)
        f0.close()

        #Write the device VLAN output to a file.
        f1 = open(backup_dir+'/'+vlan_filename, 'w')
        f1.write(output_vlan)
        f1.close()

        f2 = open(backup_dir+'/'+cdp_filename, 'w')
        f2.write(output_cdp)
        f2.close()

        f3 = open(backup_dir+'/'+status_filename, 'w')
        f3.write(output_status)
        f3.close()

        f4 = open(backup_dir+'/'+lag_filename, 'w')
        f4.write(output_lag)
        f4.close()

        f5 = open(backup_dir+'/'+arp_filename, 'w')
        f5.write(output_arp)
        f5.close()

#Switch_Backup
'''
backup_filename = 'SW-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'
vlan_filename = 'SW-Show-VLAN-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
cdp_filename = 'SW-Show-CDP-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
status_filename = 'SW-Interface-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
arp_filename = 'SW-ARP-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
lag_filename = 'SW-LAG-status-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'

with open(device_list) as json_file:
    data = json.load(json_file)
    
    for switch in data['switch_list']:
        cisco = {
    	    'device_type': 'cisco_ios',
    	    'host':   switch['ip'],
    	    'username': username,    # Provide SSH username
    	    'password': password,    # Provide SSH password
    	    #'secret': secret,     # Optional, defaults to ''
	    }

        try:
            net_connect = ConnectHandler(**cisco)
        except:
                continue

        net_connect.enable()

        output_run_config = net_connect.send_command("show running-config")
        output_vlan = net_connect.send_command("show vlan brief")
        output_cdp = net_connect.send_command("show cdp neighbor")
        output_status = net_connect.send_command("show interface status")
        output_arp = net_connect.send_command("show ip arp")
        output_lag = net_connect.send_command("show etherchannel summary ")

        net_connect.exit_enable_mode()
        net_connect.disconnect()

        #Create a separate directory for each device if not exists.
        backup_dir = '/root/Datacenter_Backups/Switch/'+switch['hostname']
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        #Write the device running-config to a file.
        f0 = open(backup_dir+'/'+backup_filename, 'w')
        f0.write(output_run_config)
        f0.close()

        #Write the device VLAN output to a file.
        f1 = open(backup_dir+'/'+vlan_filename, 'w')
        f1.write(output_vlan)
        f1.close()

        f2 = open(backup_dir+'/'+cdp_filename, 'w')
        f2.write(output_cdp)
        f2.close()

        f3 = open(backup_dir+'/'+status_filename, 'w')
        f3.write(output_status)
        f3.close()

        f4 = open(backup_dir+'/'+arp_filename, 'w')
        f4.write(output_arp)
        f4.close()

        f5 = open(backup_dir+'/'+lag_filename, 'w')
        f5.write(output_lag)
        f5.close()
'''

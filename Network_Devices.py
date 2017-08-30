#-*- coding:utf-8 -*-

import paramiko
import xlrd
import os
import time

def ssh2(ip, port, username, passwd, cmd, device):
    buffer=[]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, passwd)
        chan = ssh.invoke_shell()
        for x in cmd:
            chan.send(x)
            while not chan.recv_ready():
                time.sleep(5)
            respond = chan.recv(9999)
            buffer.append(bytes.decode(respond))
        ssh.close()
        print('Getting \'' + device +'\' benchmark is in processing, please wait...\n')
    except:
        print('Connect to %s Error\n' %(ip))
        #raise
        buffer.append('Error')
        pass
    return buffer

def write_log(path, file, content):
    if os.path.isfile(path + file) == False:
        with open(path + file, 'a') as f:
            for x in content:                
                f.write(str(x) + '\n')
        new = 'created ' + path + file + '.\n'
    else:
        with open(path + file, 'w+') as f:
            for x in content:                
                #print(x)
                f.write(str(x) + '\n')
        new = path + file + ' has been overwrote.\n'
    return new

def input_info(file, sheet_name):
    device_name, brand, ip, port, username, passwd, cmd = [], [] ,[], [], [], [], []
    data = xlrd.open_workbook(file)
    table = data.sheet_by_name(sheet_name)
    value = []
    for x in range(table.nrows):
        value.append(table.row_values(x))
    for x in value:
        device_name.append(x[0])
        brand.append(x[1])
        ip.append(x[2])
        port.append(x[3])
        username.append(x[4])
        passwd.append(x[5])
        cmd.append(x[6].split(','))
    device_name = device_name[1:]
    brand = brand[1:]
    ip = ip[1:]
    port = port[1:]
    username = username[1:]
    passwd = passwd[1:]
    cmd = cmd[1:]
    for x in range(len(cmd)):
        if brand[x] == 'Cisco_Router':
            cmd[x] = cmd[x] + ['terminal length 0', 'show bgp', 'show cdp', 'show crypto key mypubkey rsa', 'show interface description', 'show logging', 'show mpls interface', 'show ntp associations det', 'show ntp status', 'show running-config']
        if brand[x] == 'Cisco_L2_Switch':
            cmd[x] = cmd[x] + ['terminal length 0', 'show running-config', 'show version']
        if brand[x] == 'Cisco_L3_Switch':
            cmd[x] = cmd[x] + ['terminal length 0', 'show running-config', 'show version']
        if brand[x] == 'Huawei_Router':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display current-configuration', 'display ftp-server', 'display info-center', 'display interface', 'display logbuffer', 'display ntp-service status', 'display snmp-agent sys-info', 'display user-interface']
        if brand[x] == 'Huawei_L2_Switch':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display current-configuration', 'display ftp-server', 'display info-center', 'display interface', 'display logbuffer', 'display ntp-service status', 'display snmp-agent sys-info', 'display user-interface']
        if brand[x] == 'Huawei_L3_Switch':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display current-configuration', 'display ftp-server', 'display info-center', 'display interface', 'display logbuffer', 'display ntp-service status', 'display snmp-agent sys-info', 'display user-interface']
        if brand[x] == 'H3C_Router':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display brief interface display interface brief', 'display current-configuration', 'display ftp-server', 'display info-center', 'display interface', 'display isis brief', 'display ntp-service status', 'display ospf brief', 'display password-control', 'display snmp-agent sys-info', 'display user-interface', 'display version']
        if brand[x] == 'H3C_L2_Switch':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display arp detection', 'display current-configuration', 'display domain', 'display ip http', 'display logbuffer size 1', 'display ndp', 'display ntp status', 'display password', 'display password-control', 'display port-security', 'display radius scheme', 'display user-interface']
        if brand[x] == 'H3C_L3_Switch':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display arp detection', 'display current-configuration', 'display domain', 'display ip http', 'display logbuffer size 1', 'display ndp', 'display ntp status', 'display password', 'display password-control', 'display port-security', 'display radius scheme', 'display user-interface']
        if brand[x] == 'H3C_Firewall':
            cmd[x] = cmd[x] + ['screen-length 0 temporary ', 'display current-configuration', 'display ftp-server', 'display info-center', 'display interface', 'display interface brief', 'display ip interface brief', 'display local-user', 'display ntp-service status', 'display ospf brief', 'display password-control', 'display patch information', 'display snmp-agent sys-info', 'display user-interface', 'display userlog export', 'display version']
        if brand[x] == 'Hillstone_Firewall':
            cmd[x] = cmd[x] + ['show aaa-server', 'show admin user', 'show configuration', 'show logging', 'show ntp status', 'show policy', 'show version', 'show zone']
        if brand[x] == 'HP_SanSwitch':
            cmd[x] = cmd[x] + []
        if brand[x] == 'F5_LoadBlance':
            cmd[x] = cmd[x] + []
        for y in range(len(cmd[x])):
            cmd[x][y] = cmd[x][y] + '\n'
    return device_name, brand, ip, port, username, passwd, cmd


if __name__ == "__main__":
#    input_file = input('请输入excel文件所在路径（如：D:\\file\\file.xls）:\n')
    input_file = r'D:\\Python\test.xlsx'
#    sheet = input('请输入excel文件所在sheet（如：info）:\n')
    sheet = r'test'
#    export_path = input('请输入输出文件所在路径（如：D:\\file\\）:\n注意注意注意：若该文件夹内存在基线抓取结果，原有文件可能被覆盖！！！ \n')
    export_path = r'D:\\Python\test' + '\\'
    print('In processing, please wait...\n')
    info = input_info(input_file, sheet)
    result = []
    path = export_path + time.strftime('%Y%m%d', time.localtime())
    if os.path.exists(path) == False:
        os.makedirs(path)
    for x in range(len(info[1])):
        log = []
        log = ssh2(info[2][x], int(info[3][x]), info[4][x], info[5][x], info[6][x], info[0][x])
        print(write_log(path + '\\', info[0][x] + '-' + time.strftime('%Y%m%d', time.localtime()) + '-benchmark.log', log))
#    os.system('pause')  


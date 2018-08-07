#!/usr/bin/env Python
# -*- coding:UTF-8 -*-

import telnetlib, time, paramiko, datetime, os, re


def exchange_mask(mask):
    # 计算二进制字符串中 '1' 的个数
    count_bit = lambda bin_str: len([i for i in bin_str if i == '1'])
    # 分割字符串格式的子网掩码为四段列表
    mask_splited = mask.split('.')
    # 转换各段子网掩码为二进制, 计算十进制
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    return sum(mask_count)
class DeviceMessage(object):
    def __init__(self, deviceName, deviceType, deviceIp, username, password):
        self.deviceName = str(deviceName)
        self.deviceType = str(deviceType)
        self.deviceIp = str(deviceIp)
        self.username = str(username)
        self.password = str(password)
        self.getWayIp = str(None)
        self.devicePortIpv4 = str(None)
        self.devicePortIpv6 = str(None)
        self.devicePortStatu = str(None)
        self.deviceInterface = str(None)
        self.devicePortIpv4 = str(None)
        self.devicePortIpv6 = str(None)

    def setGetWayIp(self, getWayIp):
        self.getWayIp = str(getWayIp).replace('\n', '')

    def setIpv4Value(self, devicePortIpv4):
        self.devicePortIpv4 = str(devicePortIpv4)

    def setIpv6Value(self, devicePortIpv6):
        self.devicePortIpv6 = str(devicePortIpv6)

    def setPortFlag(self, devicePortStatu):
        self.devicePortStatu = str(devicePortStatu)

    def setInterface(self, deviceInterface):
        self.deviceInterface = str(deviceInterface)

    def toString(self):
        return self.deviceName + '\t' + self.deviceIp + '\t' + self.deviceType + '\t' + self.username + '\t' + self.password + '\t' + self.devicePortIpv4 + '\t' + self.devicePortIpv6 + '\t' + self.deviceInterface + '\t' + self.devicePortStatu + '\t' + self.getWayIp + '\n'
import cx_Oracle

ssssssss = datetime.datetime.now()

startTime = datetime.datetime.now()
conn = cx_Oracle.connect('xxxx/xxxx@ipaddress/xxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
curs = conn.cursor()

# 对数据的处理，或者先进行存储，释放数据库资源，防止长时间占用出现未知问题  由于数据不多，所以直接储存再内存中就可以，提高程序效率
sql = "select DEVICE_NAME, DEVICE_VENDOR, DEVICE_IP, TELNET_USERNAME, TELNET_PASSWORD, GATE_WAY_IP from ctg_device_addinfo "  # TODO   where rownum<=10     where GATE_WAY_IP is not null and rownum<=15
curs.execute(sql)
ipList = list()
while True:
    row = curs.fetchone()
    if row:
        devm = DeviceMessage(row[0], row[1], row[2], row[3], row[4])  # TODO
        if row[5]:
            devm.setGetWayIp(row[5])  # 添加gatway信息
        else:
            devm.setGetWayIp(None)
        ipList.append(devm)
    else:
        break

curs.close()
conn.close()

##################################################################   开始对的数据进行处理
# 登陆机器
f = open('1111111__logTime.log', 'w')
for i in ipList:
    # print(i.toString())
    showInterfaceCommand = None
    if i.deviceType == 'Cisco':
        showInterfaceCommand = 'show interfaces | include line protocol is'
    elif i.deviceType == 'Huawei':
        showInterfaceCommand = ''
    elif i.deviceType == 'Juniper':
        showInterfaceCommand = ''
    else:
        showInterfaceCommand = ''

    logInfo = LogInfo()
    if i.getWayIp == 'None':
        logInfo.setValue(device_name=i.deviceIp, username=i.username, password=i.password, connection='telnet',
                         getwayIp=i.getWayIp, targetUserName='', targetPassWord='')
    else:
        logInfo.setValue(device_name=i.getWayIp, username=i.username, password=i.password, connection='telnet',
                         getwayIp=i.deviceIp, targetUserName=i.username, targetPassWord=i.password)
    logInfo.connectionMethed()
    if logInfo.isLog:
        if i.deviceType == 'Cisco':
            logInfo.device.command('term len 0', time_delay=5)
            message = logInfo.device.command(showInterfaceCommand, time_delay=20)
            message = message.replace('\r', '')
            file_name = 'message/' + '__' + i.deviceIp + '.txt'
            f1 = open(file_name, 'w')
            f1.write(i.toString())
            f1.write(message)
            f1.flush()
            f1.close()
        elif i.deviceType == 'Huawei':
            message = 'Huawei'
            f.write('HuaWei:' + i.toString() + '\n')
        elif i.deviceType == 'Juniper':
            message = 'Juniper'
            f.write('Juniper:' + i.toString() + '\n')
        else:
            message = 'unkonw'
            f.write('unkonw:' + i.toString() + '\n')
    else:
        message = 'Login failure'
        f.write('Login failure:' + i.toString() + '\n')
    logInfo.device.close()
endTime = datetime.datetime.now()
print("第一部分 runTime:" + str((endTime - startTime).seconds))
f.closed

####################################################################################################

sss2 = datetime.datetime.now()
rootdir = 'message'
list_File = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list_File)):
    path = os.path.join(rootdir, list_File[i])
    if os.path.isfile(path):
        print(path)
        f = open(path, 'r')
        path = path.replace('message', 'port')
        port_file = open(path, 'w')
        port_file.write(f.readline())  # 将第一行有用的信息输入进去
        while True:
            message = f.readline()
            if message:
                # POS2/0/0 is administratively down, line protocol is down
                findPort = re.findall(r'(.+?) is(.+?), line protocol is', message)
                if findPort:
                    port_file.write(findPort[0][0] + '\n')
            else:
                break
        f.close()
        port_file.close()
eee2 = datetime.datetime.now()
print("第二部分 Runtime:" + str((eee2 - sss2).seconds))

############################################################################################################
# 获取ip 信息
sss3 = datetime.datetime.now()
rootdir = 'port'
list_File = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list_File)):
    path = os.path.join(rootdir, list_File[i])
    addInterFace_Ipv4 = list()
    addInterFace_Ipv6 = list()

    if os.path.isfile(path):
        ff = open(path, 'r')
        message = ff.readline()
        groupMessage = message.split('\t')
        # 置空devm
        # devm.setNoneValue()
        devm = DeviceMessage(deviceName=groupMessage[0], deviceType=groupMessage[2], deviceIp=groupMessage[1],
                             username=groupMessage[3], password=groupMessage[4])
        devm.setGetWayIp(groupMessage[9])
        print(devm.toString())
        interface_List = list()
        while True:
            line = ff.readline()
            if line:
                print(line)
                interface_List.append(line.replace('\n', ''))  # 减少/n的对报文的影响
            else:
                break
        ff.close()  # 读取所有的信息结束

        # 登陆机器
        logInfo = LogInfo()
        if devm.getWayIp == 'None':
            logInfo.setValue(device_name=devm.deviceIp.replace('\n', ''), username=devm.username,
                             password=devm.password,
                             connection='telnet',
                             getwayIp=devm.getWayIp, targetUserName='', targetPassWord='')
        else:
            logInfo.setValue(device_name=devm.getWayIp.replace('\n', ''), username=devm.username,
                             password=devm.password,
                             connection='telnet',
                             getwayIp=devm.deviceIp.replace('\n', ''), targetUserName=devm.username,
                             targetPassWord=devm.password)
        logInfo.connectionMethed()

        try:
            if logInfo.isLog:
                print(logInfo.device.endFlag)
                file_name = path.replace('port', 'Ipv4_Ipv6')
                f1 = open(file_name, 'w')
                f1.write(devm.toString())
                # logInfo.device.command('term len 0', time_delay=5)  # 直接提交命令  不管错不错
                for j in range(len(interface_List)):
                    showInterfaceCommand = 'show running-config interface ' + interface_List[j]
                    devm.setInterface(interface_List[j])
                    if devm.deviceType == 'Cisco':
                        message = logInfo.device.command(showInterfaceCommand, time_delay=20)
                        message = message.replace('\r', '')
                        # f1.write(message)  # TODO 做解析
                        findShutDown = 'shutdown'
                        findErrorMessage = '% No such configuration item(s)'
                        findIp = re.findall(r'ip address (.+?)\n', message)
                        findIpv4 = re.findall(r'ipv4 address (.+?)\n', message)
                        findIpv6 = re.findall(r'ipv6 address (.+?)\n', message)

                        if findIp:
                            devm.setIpv4Value(findIp[0])
                        elif findIpv4:
                            devm.setIpv4Value(findIpv4[0])
                        else:
                            devm.setIpv4Value(None)

                        if findIpv6:
                            devm.setIpv6Value(findIpv6[0])
                        else:
                            devm.setIpv6Value(None)

                        if findShutDown in message:
                            devm.setPortFlag('shutdown')
                        elif findErrorMessage in message:
                            devm.setPortFlag('% No such configuration item(s)')
                        else:
                            if devm.devicePortIpv4 != 'None' or devm.devicePortIpv6 != 'None':
                                devm.setPortFlag('up')
                            else:
                                devm.setPortFlag('shutdown')

                        f1.write(devm.toString())

                        ipv4 = devm.devicePortIpv4
                        ipv6 = devm.devicePortIpv6
                        ipv4_mask = ''
                        ipv6_mask = ''

                        if ipv4 != 'None':
                            findIpv4 = ipv4.split(' ')
                            ipv4 = findIpv4[0]
                            ipv4_mask = str(exchange_mask(findIpv4[1]))

                        if ipv6 != 'None':
                            findIpv6 = ipv6.split('/')
                            ipv6 = findIpv6[0]
                            ipv6_mask = findIpv6[1]

                        # DEVICE_NAME IP_ADDRESS SUBNET_MASK_NUMBER DEVICE_IP PORT
                        addInterFace_Ipv4.append(
                            (devm.deviceName, ipv4, ipv4_mask, devm.deviceIp, devm.deviceInterface))
                        addInterFace_Ipv6.append(
                            (devm.deviceName, ipv6, ipv6_mask, devm.deviceIp, devm.deviceInterface))
                        pass
                        # TODO 做储存 数据库中
                    elif devm.deviceType == 'Huawei':
                        message = 'Huawei'
                        # f.write('HuaWei:' + i.toString() + '\n')
                    elif devm.deviceType == 'Juniper':
                        message = 'Juniper'
                        # f.write('Juniper:' + i.toString() + '\n')
                    else:
                        message = 'unkonw'
                        # f.write('unkonw:' + i.toString() + '\n')
                # for end
                f1.flush()
                f1.close()

            else:
                message = 'Login failure'
                # f.write('Login failure:' + i.toString() + '\n')
            print(message)
            logInfo.device.close()
        except (Exception) as e:
            print(e)
    else:
        pass

    conn = cx_Oracle.connect('xxxx/xxxx@ipaddress/xxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
    curs = conn.cursor()
    curs.executemany(
        'insert into ctg_device_ipv4(DEVICE_NAME,IP_ADDRESS,SUBNET_MASK_NUMBER,DEVICE_IP,PORT)  values(:1,:2,:3,:4,:5)',
        addInterFace_Ipv4)
    curs.executemany(
        'insert into ctg_device_ipv6(DEVICE_NAME,IP_ADDRESS,SUBNET_MASK_NUMBER,DEVICE_IP,PORT)  values(:1,:2,:3,:4,:5)',
        addInterFace_Ipv6)
    # 提交事务
    conn.commit()
    curs.close()
    conn.close()

eee3 = datetime.datetime.now()
print("第三部分 Runtime:" + str((eee3 - sss3).seconds))

eeeeeeeee = datetime.datetime.now()

print("总体 Runtime:" + str((eeeeeeeee - ssssssss).seconds))
      

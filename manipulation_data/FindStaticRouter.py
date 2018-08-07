class SSSSSSSSS(object):
    def __init__(self, DEVICE_NAME, DEVICE_IP):
        self.DEVICE_NAME = DEVICE_NAME
        self.DEVICE_IP = DEVICE_IP
        self.SUBNET_MASK_NUMBER = None
        self.IP_ADDRESS = None
        self.PORT = None


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

# 1 首先找出所有的IP地址范围  都需要在数据库寻找的字段有
# DEVICE_NAME, DEVICE_VENDOR, DEVICE_MODEL, DEVICE_IP, REMOTE_PROTOCOL, TELNET_USERNAME, TELNET_PASSWORD


conn = cx_Oracle.connect('xxx/xxx@ipaddress/xxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
curs = conn.cursor()

sql = "select DEVICE_NAME, DEVICE_VENDOR, DEVICE_IP, TELNET_USERNAME, TELNET_PASSWORD, GATE_WAY_IP from ctg_device_addinfo "  # TODO   where rownum<=10     where GATE_WAY_IP is not null and rownum<=15
curs.execute(sql)
ipList = list()
#   数据封装
while True:
    row = curs.fetchone()
    if row:
        devm = DeviceMessage(row[0], row[1], row[2], row[3], row[4])
        if row[5]:
            devm.setGetWayIp(row[5])  # 添加gatway信息
        else:
            devm.setGetWayIp(None)
        ipList.append(devm)
    else:
        break

curs.close()
conn.close()
###################################################################################################

# 登陆机器
# 用文件记录登陆时候出现错误或者机型
f = open('1111111__FindStaticRouter.log', 'w')
for i in ipList:
    # 确认输入的命令
    showStaticCommand = None
    if i.deviceType == 'Cisco':
        showStaticCommand = 'show running-config  router static'
    elif i.deviceType == 'Huawei':
        showStaticCommand = ''
    elif i.deviceType == 'Juniper':
        showStaticCommand = ''
    else:
        showStaticCommand = ''
    # 登陆类
    logInfo = LogInfo()
    # 判断是否填入getway信息
    if i.getWayIp == 'None':
        logInfo.setValue(device_name=i.deviceIp, username=i.username, password=i.password, connection='telnet',
                         getwayIp=i.getWayIp, targetUserName='', targetPassWord='')
    else:
        logInfo.setValue(device_name=i.getWayIp, username=i.username, password=i.password, connection='telnet',
                         getwayIp=i.deviceIp, targetUserName=i.username, targetPassWord=i.password)
    # 连接
    logInfo.connectionMethed()
    if logInfo.isLog:
        if i.deviceType == 'Cisco':
            logInfo.device.command('term len 0', time_delay=5)
            message = logInfo.device.command(showStaticCommand, time_delay=20)
            message = message.replace('\r', '')
            if "% Invalid input detected at '^' marker." not in message:
                file_name = 'message/' + '__' + i.deviceIp + 'show_running-config_router_static.txt'
                f1 = open(file_name, 'w')
                f1.write(i.toString())
                f1.write(message)
                f1.flush()
                f1.close()
            else:
                f.write('Cisco Command Is Bad:' + i.toString() + '\n')
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
f.close()

rootdir = 'message'
list_File = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list_File)):
    path = os.path.join(rootdir, list_File[i])
    ipv4List = list()
    if os.path.isfile(path):
        ff = open(path, 'r')
        deviceMessage = ff.readline() # 取出第一行数据
        deviceMessage = deviceMessage.split('\t')
        while True:
            line = ff.readline()
            if line:
                if line == ' address-family ipv4 unicast\n':
                    while True:
                        temp = ff.readline()
                        if temp:
                            if '!\n' in temp:
                                break
                            ssssssssssssss = SSSSSSSSS(DEVICE_NAME=deviceMessage[0], DEVICE_IP=deviceMessage[1])
                            if 'Null0' in temp:
                                try:
                                    findMessage = re.findall(r'( +)(.+?)/(\d+) Null0\n', temp)
                                    ssssssssssssss.IP_ADDRESS = findMessage[0][1]
                                    ssssssssssssss.SUBNET_MASK_NUMBER = findMessage[0][2]
                                    ssssssssssssss.PORT = 'Null0'
                                except (Exception) as e:
                                    # 处理特殊情况
                                    findMessage = re.findall(r'( +)(.+?)/(\d+) Null0(.+?)\n', temp)
                                    ssssssssssssss.IP_ADDRESS = findMessage[0][1]
                                    ssssssssssssss.SUBNET_MASK_NUMBER = findMessage[0][2]
                                    ssssssssssssss.PORT = 'Null0'
                            else:
                                findMessage = re.findall(r'( +)(.+?)/(\d+) (.+?) (.+?)\n', temp)
                                if findMessage:
                                    ssssssssssssss.IP_ADDRESS = findMessage[0][1]
                                    ssssssssssssss.SUBNET_MASK_NUMBER = findMessage[0][2]
                                    ssssssssssssss.PORT = findMessage[0][3]
                                else:
                                    findMessage = re.findall(r'( +)(.+?)/(\d+) (.+?)\n', temp)
                                    ssssssssssssss.IP_ADDRESS = findMessage[0][1]
                                    ssssssssssssss.SUBNET_MASK_NUMBER = findMessage[0][2]
                                    ssssssssssssss.PORT = findMessage[0][3]
                            ipv4List.append((
                                ssssssssssssss.DEVICE_NAME, ssssssssssssss.DEVICE_IP,
                                ssssssssssssss.SUBNET_MASK_NUMBER,
                                ssssssssssssss.IP_ADDRESS, ssssssssssssss.PORT))
                        else:
                            break
            else :
                break
        ff.close()


    conn = cx_Oracle.connect('xxx/xxx@ipaddress/xxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
    curs = conn.cursor()
    curs.executemany('insert into ctg_device_routestatic(DEVICE_NAME,DEVICE_IP,SUBNET_MASK_NUMBER,IP_ADDRESS,PORT)  values(:1,:2,:3,:4,:5)',ipv4List)
    # 提交事务
    conn.commit()

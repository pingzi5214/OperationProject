conn = cx_Oracle.connect('xxxx/xxxx@ipaddress/xxxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
curs = conn.cursor()

sql = "select DEVICE_NAME, DEVICE_VENDOR, DEVICE_IP, TELNET_USERNAME, TELNET_PASSWORD, GATE_WAY_IP from ctg_device_addinfo where DEVICE_VENDOR = 'Cisco'"
# TODO   where rownum<=10     where GATE_WAY_IP is not null and rownum<=15
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
f = open('11111111__Find_C_IpAddress.log', 'w')
for i in ipList:
    # 确认输入的命令
    showStaticCommand = 'show run | b router bgp 4134 | include route-policy | include network'
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
    llllllll = list()
    if logInfo.isLog:
        logInfo.device.command('term len 0', time_delay=5)
        message = logInfo.device.command(showStaticCommand, time_delay=20)
        message = message.replace('\r', '')
        if "% Invalid input detected at '^' marker." not in message:
            # line = f.read()
            f.write('命令获取成功返回结果如下:' + i.toString() + '\n'+ message +'\n')
            findMessage = re.findall(r'( +)network (.+?)/(\d+) route-policy (.+?)\n', message)
            if findMessage:
                for index in range(findMessage.__len__()):
                    temp = findMessage[index]
                    llllllll.append(('Null', '202.97.32.121', findMessage[0][2], findMessage[0][1]))
            # file_name = 'message/' + '__' + i.deviceIp + 'Find_C_IpAddress.txt'
            # f1 = open(file_name, 'w')
            # f1.write(i.toString())
            # f1.write(message)
            # f1.flush()
            # f1.close()
        else:
            f.write('Cisco Command Is Bad:' + i.toString() + '\n' + message + '\n')
    else:
        message = 'Login failure'
        f.write('Login failure:' + i.toString() + '\n')
    logInfo.device.close()
    # 入库
    if llllllll.__len__() > 0 :
        conn = cx_Oracle.connect('xxxx/xxxx@ipaddress/xxxxxxx')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
        curs = conn.cursor()
        curs.executemany(
            'insert into ctg_device_broute(DEVICE_NAME,DEVICE_IP,SUBNET_MASK_NUMBER,IP_ADDRESS)  values(:1,:2,:3,:4)',
            llllllll)
        # 提交事务
        conn.commit()
    else:
        f.write('返回报文有问题，需要验证:' + i.toString() + '\n' + message + '\n')
f.close

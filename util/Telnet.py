#!/usr/bin/env Python
# -*- coding:UTF-8 -*-
# 当前类是Telnet连接类
class Telnet(object):
    def __init__(self, device_name, username, password, delay=5, port=23):
        self.device_name = device_name  # 连接驱动名
        self.username = username  # 连接用户名
        self.password = password  # 连接密码
        self.delay = float(delay)  # 设置相应等待延迟
        self.port = int(port)  # 端口号
        self.access = None
        self.endFlag = None
        # self.endFlagJuniper = '{master}'
        self.moreFlag = '(\-)+( |\()?[Mm]ore.*(\)| )?(\-)+'

    def connect(self):
        print '登陆方式：TELNET'
        result = None
        try:
            self.access = telnetlib.Telnet(self.device_name, self.port, timeout=60)
            login_prompt = self.access.expect(["Username:", "login:"], self.delay)

            self.access.write(self.username + "\n")

            password_prompt = self.access.expect(["Password:"], self.delay)

            self.access.write(self.password + "\n")

            isLog = self.access.expect(["#", ">"], self.delay)

            if '#' in isLog[2] or '>' in isLog[2]:
                result = self.access
            else:
                result = None
        except (Exception) as e:
            print(str(self.device_name) + ':' + str(e))  # 登陆异常
            if 'Connection reset by peer' in str(e):
                print '设备登录异常，继续下一设备登录'
                excepFlag = True  # 登陆异常标志
                result = None
            else:
                result = None

        if result != None:
            self.access.write('\n')
            time.sleep(0.5)
            message = self.access.expect(['#', '>'], 2)
            message = message[2].replace('\r', '')
            message = message.replace('\n', '')
            print 'endflag:', message
            self.endFlag = message

        return result

    def close(self):
        return self.access.close()

    def command(self, command, time_delay=60):
        self.access.write(command + '\n')
        time.sleep(0.5)
        message = self.access.expect([r'%s' % self.moreFlag, self.endFlag], time_delay)  # 这是修改的地方
        # 0 完全接收
        # -1 超时
        result = message[2]
        result = result.replace('---- More ----', '')
        result = re.sub('---\((.*)\)---', '', result)
        result = result.replace('More', '')
        result = result.replace('\x1b', '')
        result = result.replace('\r', '')
        result = result.replace(' --More--', '')
        result = result.replace(' --More-', '')
        result = result.replace('-', '')
        if message[0] == 0:
            result += self.getMore()
        elif message[0] == 1:
            pass
        elif message[0] == -1:
            # Recvive timeout
            result = result + '\t Recvive timeout'
        return result

    def getMore(self):
        print '第二次endflag：' + self.endFlag
        print 'get more method'
        result = ''
        counts = 1
        try:
            while True:
                print counts
                counts = counts + 1
                self.access.write(' ')
                i = self.access.expect([r'%s' % self.moreFlag, self.endFlag], timeout=10)
                # Get result
                temp = i[-1]
                temp = temp.replace(' --More--', '')
                temp = temp.replace(' --More-', '')
                temp = re.sub('---\((.*)\)---', '', temp)
                temp = temp.replace('More', '')
                temp = temp.replace('-', '')
                temp = temp.replace('\r', '')
                temp = temp.replace('\x08', '')
                temp = temp.replace('\x1b', '')
                temp = temp.replace('---- More ----', '')
                temp = temp.replace('                                        ', '')
                # temp = temp.replace('{master}','')
                print temp
                result += temp
                if i[0] == -1:
                    break
        except (Exception) as e:
            print(e)
        return result

    def commandSecondLog(self, targetIp, username, password, time_delay=5):
        self.access.write(' telnet ' + targetIp + '\n')  # 发送等登陆命令
        login = self.access.expect(["Username:", "login:", "timed out"], time_delay)
        if 'timed out' in login[2] or login[0] == -1:
            return False
        self.access.write(username + '\n')  # 发送用户名
        login_UserName = self.access.expect(["Password:"], 5)
        if 'command not found' in login_UserName[2] or 'marker' in login_UserName[2] or 'position' in login_UserName[2]:
            return False
        self.access.write(password + '\n')  # 发送密码
        login_PassWord = self.access.expect(["#", ">"], 5)
        if 'User Access Verification' in login_PassWord[2] or 'Error: Tacacs server reject' in login_PassWord[2]:
            return False

        self.access.write('\n')
        time.sleep(0.5)
        message = self.access.expect(['#', '>'], 2)
        message = message[2].replace('\r', '')
        message = message.replace('\n', '')
        message = message.replace('{master}', '')

        self.endFlag = message

        return True

    def getWayClose(self):
        self.access.write('quit' + '\n')

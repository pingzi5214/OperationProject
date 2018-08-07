#!/usr/bin/env Python
# -*- coding:UTF-8 -*-
# 当前类是SSH连接类

class SSH(object):
    #  SSH 在碰到转登的时候，由于工具使用不是很熟悉会出现各种问题，慎用 ，出现情况的时候，需要再次添加

    def __init__(self, device_name, username, password, buffer="65535", delay="1", port="22"):
        self.device_name = device_name  # 连接驱动名
        self.username = username  # 连接名
        self.password = password  # 连接密码
        self.buffer = buffer  # 连接缓存
        self.delay = delay  # 连接最大延迟时间
        self.port = int(port)  # 连接端口
        self.pre_conn = None
        self.client_conn = None
        self.endFlag = None
        self.moreFlag = '(\-)+( |\()?[Mm]ore.*(\)| )?(\-)+'

    def connect(self):
        self.pre_conn = paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.pre_conn.connect(self.device_name, username=self.username,
                                  password=self.password, allow_agent=False,
                                  look_for_keys=False, port=self.port, timeout=5)
        except (Exception) as e:
            print(e)
            return None
        self.client_conn = self.pre_conn.invoke_shell(width=10000, height=10000)
        self.client_conn.settimeout(60)  # 设置会话超时时间
        output = ""
        while True:
            time.sleep(1)  # time_delay
            if self.client_conn.recv_ready():
                output = output + self.client_conn.recv(65535)
            else:
                break

        output = output.split('\n')[-1]
        self.endFlag = output  # 获取结束字符
        print(self.endFlag)
        return self.client_conn  # 返回没有什么特殊含义

    def close(self):
        return self.pre_conn.close()

    def clear_buffer(self):
        if self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer)
        else:
            return None

    def command(self, command, time_delay=2):
        self.client_conn.send(command + "\n")
        output = ""
        self.clear_buffer()  # 这个可能是需要更改的地方
        while True:
            self.getMore(output)
            output += self.client_conn.recv(1024)
            if self.endFlag in output:
                break
        return output

    def getMore(self, bufferData):
        # 查看当前行是不是需要特殊处理
        if re.search(self.moreFlag, bufferData.replace("\r", "").split('\n')[-1]):
            self.client_conn.send(' ')

    def command_Change(self, command, time_delay=2):
        self.client_conn.sendall(command + "\n")
        not_done = True
        output = ""
        # self.clear_buffer()  # 这个可能是需要更改的地方
        while not_done:
            time.sleep(1.5)  # time_delay
            if self.client_conn.recv_ready():
                output = output + self.client_conn.recv(1024)
            else:
                not_done = False
        return output

    def commandSecondLog(self, targetIp, username, password, time_delay=60):
        output1 = self.command_Change('telnet ' + targetIp)
        if 'timed out' in output1:
            return False
        output2 = self.command_Change(username + '')  # 需要进行容错处理
        if 'command not found' in output2 or 'marker' in output2 or 'position' in output2:
            return False
        output3 = self.command_Change(password + '')  # 需要进行容错处理
        if 'User Access Verification' in output3 or 'Error: Tacacs server reject' in output3:
            return False

        if ':' in output1 and ':' in output2 and output3 == '':
            for i in range(0, 10):  # 特殊处理了一下，如果十次等待还是等不到结果，我们就认为登陆失败，相应的，登陆时间会延长。
                output3 = self.command_Change(' ')
                if output3 != '':
                    break

        if ':' in output1 and ':' in output2 and ('#' in output3 or '>' in output3):  # 查看登陆返回符号是否正确
            message = self.command_Change("")
            self.endFlag = message.replace("\r", "").replace("\n", "")
            print(self.endFlag)
            return True
        else:
            return False

    def getWayClose(self):
        self.client_conn.send("quit\n")

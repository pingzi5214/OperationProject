#!/usr/bin/env Python
# -*- coding:UTF-8 -*-
# 登陆信息储存类
class LogInfo(object):
    def __init__(self):  # 创建连接的时候默认的都是None
        self.device = None  # 连接驱动类
        self.device_name = None  # 连接驱动名
        self.username = None  # 连接名
        self.password = None  # 连接密码
        self.connection = None  # 连接方式
        self.getwayIp = None  # 第二次登陆ip
        self.targetUserName = None  # 第二次登陆的用户名
        self.targetPassWord = None  # 第二次登陆的密码
        self.isLog = False  # 判断是否登陆成功

    def setValue(self, device_name, username, password, connection, getwayIp, targetUserName, targetPassWord):
        self.device_name = device_name  # 连接驱动名
        self.username = username  # 连接名
        self.password = password  # 连接密码
        self.connection = connection  # 连接方式
        self.getwayIp = getwayIp  # 第二次登陆ip
        self.targetUserName = targetUserName  # 第二次登陆的用户名
        self.targetPassWord = targetPassWord  # 第二次登陆的密码

    def connectionMethed(self):
        if self.connection == 'telnet':
            # print('telnet login !!!')
            self.device = Telnet(device_name=self.device_name,
                                 username=self.username,
                                 password=self.password)
        else:
            # print('ssh login !!!')
            self.device = SSH(device_name=self.device_name,
                              username=self.username,
                              password=self.password,
                              buffer=4096)
        flag = self.device.connect()
        # 判断登陆是否成功，是否需要切换登陆方式
        if flag == None:
            if self.connection == 'telnet':
                self.device = SSH(device_name=self.device_name,
                                  username=self.username,
                                  password=self.password,
                                  buffer=4096)
            else:
                self.device = Telnet(device_name=self.device_name,
                                     username=self.username,
                                     password=self.password)
            flag = self.device.connect()
            if flag != None:
                self.isLog = True
        else:
            self.isLog = True

        if self.isLog:
            if self.getwayIp != '' and self.targetUserName != '' and self.targetPassWord != '':  # 判断是否需要再次登陆
                flag = self.device.commandSecondLog(self.getwayIp, self.targetUserName, self.targetPassWord)  # 再次登陆
                self.isLog = flag

    def close(self):
        if self.isLog:  # 如果登陆成功
            if self.getwayIp != '' and self.targetUserName != '' and self.targetPassWord != '':
                # 如果有getway信息先清除getway
                logInfo.device.getWayClose()
            # 再退出
            logInfo.device.close()
        else:
            if self.getwayIp != '' and self.targetUserName != '' and self.targetPassWord != '':
                # 如果getway也登陆不上，
                logInfo.device.close()

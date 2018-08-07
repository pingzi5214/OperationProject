# FindStaticRouter
## 对Cisco类型的设备进行统计静态路由
  登陆设备执行show running-config router static命令，解析返回的数据信息
  解析出每个路由的相关信息（地址、子网掩码的位数、端口号）。
  ```
    xxxxxxxxxx #show run router static
    Mon Jun 4 10:34:34.709 GMT
    router static
      address-family ipv4 unicast
        xxx.xxx.xxx.xxx/32 端口号 xxxxxxxxxxx
        xxx.xxx.xxx.xxx/32 端口号 xxxxxxxxxxx
        xxx.xxx.xxx.xxx/32 端口号 xxxxxxxxxxx
        xxx.xxx.xxx.xxx/32 端口号 xxxxxxxxxxx
        xxx.xxx.xxx.xxx/32 端口号 xxxxxxxxxxx
      ! 
  ```
  

# FindInterfacesAndIpAddress
## 对数据库中所有Cisco类型的设备进行登陆，查看端口对应的IPV4和IPV6的地址，统计处出来入库

* 首先统计出来当前机器的所有端口
* 根据统计出来的端口进行IPv4和IPV6的查找
要分析的部分如下
```
xxxxxxxxxxxxx #show running-config interface
Thu May 17 09:24:53.121 GMT
interface Loopback0
 description For Global Routng
 ipv4 address xxx.xxx.xxx.xxx 255.255.255.255
 ipv6 address xx:xx:xx:xx:xx/128 
```

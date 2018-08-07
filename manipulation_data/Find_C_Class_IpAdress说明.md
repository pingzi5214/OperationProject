# Find_C_Class_IpAdress
## 寻找机器中的C类IP地址
* 对Cisco类型的设备进行登录 然后执行show run | b router bgp 4134 对返回结果进行解析，具体返回如下

```
xxxxxxx # show run | b router bgp 4134 | include network | include router-plicy
Fri Jun  8 02:10:25.960 GMT
Building configuration...
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
  network xxx.xxx.xxx.xxx/32 route-policy xxxxxxx
xxxxxxx # 
```

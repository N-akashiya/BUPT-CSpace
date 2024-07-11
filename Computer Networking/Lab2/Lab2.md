# 计算机网络Lab2 {ignore}

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [一、实验准备](#一-实验准备)
  - [1.1 实验内容和目的](#11-实验内容和目的)
  - [1.2 实验环境](#12-实验环境)
- [二、实验操作及分析](#二-实验操作及分析)
  - [2.1 捕获 DHCP 报文并分析](#21-捕获-dhcp-报文并分析)
    - [2.1.1 操作](#211-操作)
    - [2.1.2 分析](#212-分析)
  - [2.2 分析数据分组的分片传输过程](#22-分析数据分组的分片传输过程)
    - [2.2.1 操作](#221-操作)
    - [2.2.2 分析](#222-分析)
    - [2.2.3 异常分析](#223-异常分析)
  - [2.3 分析 TCP 通信过程](#23-分析-tcp-通信过程)
    - [2.3.1 操作](#231-操作)
    - [2.3.2 分析](#232-分析)
- [三、实验总结](#三-实验总结)

<!-- /code_chunk_output -->


# 一、实验准备

## 1.1 实验内容和目的

实验二：IP 和 TCP 数据分组的捕获和解析

本次实验为协议分析型，内容如下：

1. 捕获在连接 Internet 过程中产生的网络层分组：DHCP 分组，ARP 分组，IP 数据分组，ICMP 分组；
2. 分析各种分组的格式，说明各种分组在建立网络连接过程中的作用；
3. 分析 IP 数据分组分片的结构，了解计算机上网的工作过程，学习各种网络层分组的格式及其作用，理解长度大于1500 字节 IP 数据组分片传输的结构；
4. 分析 TCP 建立连接，拆除连接和数据通信的流程；

## 1.2 实验环境

- Windows 11
- WireShark 4.2.5
- VMware Ubuntu 22.04.1 (辅助)

# 二、实验操作及分析

## 2.1 捕获 DHCP 报文并分析

### 2.1.1 操作

1. Wireshark设置Filter: `udp.port==68`
2. Dos窗口执行命令 ipconfig/release
    
    执行命令 ipconfig/renew
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled.png" width="500">
</p>
    
3. 重新设置WireShark的选项，Filter: `icmp or arp`
4. Dos窗口执行一个ping命令

### 2.1.2 分析

DHCP (Dynamic Host Configuration Protocol) 地址分配过程

*Computer Networking-A Top-Down Approach*

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled.jpeg" width="400">
</p>

Wireshark抓取的报文

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%201.png)

release后出现的第一个报文 DHCP Release 释放已申请的IP地址

renew后通过 DHCP Discover, Offer, Request, Ack 完成IP地址的获取

- DHCP Release
    
    ![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%202.png)


- DHCP Discover
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%203.png" width="500">
</p>
    
    - 当前PC没有分配到IP地址，故Source为0.0.0.0；DHCP服务器的IP地址未知，故Destination为255.255.255.255（进行广播，网络上只有DHCP服务器才会响应）
    - PC会随机出一个Transaction ID，如果之后收到的 Offer 中的Transaction ID与之不同，PC会将该 Offer 丢弃
    - Message type: 1 (Client)
    - Bootp flags: 最高位为1指定 
    - Offer 为广播形式

- DHCP Offer
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%204.png" width="500">
</p>
    
    - DHCP服务器以广播形式发送一个包含出租的IP地址和其他设置的 Offer 提供信息
    - Message type: 2 (Server)
    - Your (client) IP address: 服务器提供的IP地址 192.168.1.6
    - Option (51): 租约 1day
    - Option (54): DHCP地址
- DHCP Request
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%205.png" width="500">
</p>
    
    - PC只接受第一个收到的 Offer，以广播形式向服务器请求使用这个IP地址
    - Option (50): 指出要使用的IP地址
- DHCP Ack
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%206.png"
width="500">
</p>

    - DHCP服务器确认所提供的IP地址
    - DHCP服务器IP地址为192.168.1.1
    - Hops（经过的 DHCP 中继的数目）一直都是0，说明未经过router转发

---

ARP (Address Resolution Protocol): 目的IP→目的MAC

工作流程：

1. 每个主机都会在自己的ARP缓冲区建立一个ARP列表，以表示IP地址和MAC地址之间的对应关系
2. 当A要发送数据时，首先检查ARP列表中是否有B的IP地址对应的MAC地址，如果有则直接发送，如果没有就向本网段的所有主机发送ARP数据包，该数据包有：A的IP地址和MAC地址、B的IP地址
3. 当本网络的所有主机收到该ARP数据包时，首先检查数据包中的IP地址是否是自己的IP地址，如果不是，则忽略该数据包，如果是，则首先从数据包中取出A的IP和MAC地址写入到ARP列表中；然后将自己的MAC地址写入到ARP响应包中，告诉A自己是它想找的MAC地址
4. A收到ARP响应包后，将B的IP和MAC地址写入ARP列表中，并利用此信息发送数据。如果A一直没有收到响应包，则表示ARP查询失败

查看ARP表

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%207.png" width="50%" height="50%">
</p>

10.3.9.161 不在表中

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%208.png" width="400">
</p>

Wireshark捕获分组

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%209.png)

分析ICMP：

共8个(4组) ICMP报文，以第一组为例。

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2010.png)

Frame4是一个ping request（发送请求），Frame5是一个ping reply（返回响应），二者数据相同。

并没看到对10.3.9.161的ARP请求。由于目标IP：10.3.9.161和本地IP不在同一子网中，必须通过网关进行通信。

*注：从这里开始本地IP变为10.29.140.132

验证：ping 默认网关(10.29.0.1) 

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2011.png)

查看虚拟机IP（和PC在同一子网中）

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2012.png" width="400">
</p>

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2013.png" width="400">
</p>

Wireshark捕获分组

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2014.png)

分析ARP：

- 本设备ARP表中没有10.29.57.124的记录，首先发 ARP request (Broadcast)，目标MAC地址此时未知
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2015.png"
  width="500">
</p>

    
- 目标设备收到request后发送 ARP reply，此时双方IP地址和MAC地址均已知
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2016.png"
  width="500">
</p>
    
- 尽管有些ICMP Echo request显示为no response found!，但是ping命令的输出显示所有请求都得到了回复，这表明从功能上来说，网络通信是成功的。

## 2.2 分析数据分组的分片传输过程

### 2.2.1 操作

制作大于8000字节的 IP 数据分组并发送，捕获后分析其分片传输的分组结构

Dos窗口执行命令 ping -l 8000 [www.bupt.edu.cn](http://www.bupt.edu.cn)

Wireshark设置Filter: `ip.addr==10.3.9.161`

### 2.2.2 分析

每个ICMP包都被分成6个Fragment，以第一个为例。

![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2017.png)

IP header 20bytes，前5段1480bytes，最后一段608bytes，可知链路MTU为1500bytes，共计8008bytes (data 8000 + ICMP header 8)

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/58271f74-f8cd-46c9-b4d8-78f94fd86278.png"
  width="500">
</p>

Fragment 1：DF=0, MF=1 (后面还有更多分段), Offset=0 (第一个分段在包中的偏移量为0)

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2018.png"
  width="500">
</p>

Fragment 6：DF=0, MF=0 (后面没有分段了), Offset=7400 (bytes)

同一个ICMP包的分段，Identification字段相同

### 2.2.3 异常分析

接下来，我没在学校做，遇到了一些不符合预想的现象

<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2019.png" width="400">
</p>

此时PC的IP是192.168.0.194

- 使用VPN时，
解析出的 [www.bupt.edu.cn](http://www.bupt.edu.cn/)的IP地址是198.18.0.16，超时
- 未使用VPN时，
解析出的[vn46.bupt.edu.cn](http://vn46.bupt.edu.cn/)的IP地址是211.68.69.240，成功ping通

分析：

- DNS查询时，可能有一个CNAME把 [www.bupt.edu.cn](http://www.bupt.edu.cn/)重定向到[vn46.bupt.edu.cn](http://vn46.bupt.edu.cn/)
- VPN可能改变DNS服务器，从而导致不同的DNS解析结果，198.18.0.16可能不可达

## 2.3 分析 TCP 通信过程

### 2.3.1 操作

为了观察TCP建立连接的三次握手，数据通信和优雅方式拆除连接的流程，进行如下操作：

1. 浏览器打开 [www.bupt.edu.cn](http://www.bupt.edu.cn/)
2. 关闭页面
3. Wireshark设置Filter: `ip.src==10.3.9.161 or ip.dst==10.3.9.161`

### 2.3.2 分析

- TCP 3-way handshaking
    
    *Computer Networking-A Top-Down Approach*
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%201.jpeg" width="400">
</p>
    
Wireshark捕获分组
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2020.png" >
</p>

Client一个应用程序发出CONNECT请求，本地TCP实体创建一条连接记录，并标记为SYN SENT状态。
1. Client向Server发送一个SYN段（SYN=1, seq=0）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2021.png" width="500">
</p>
    
2. Server向Client针对此次连接的SYN+ACK（SYN=1, seq=0, ack=1）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2022.png" width="500">
</p>
    
3. Client向Server发出三次握手最后一个ACK段（seq=1, ack=1）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2023.png" width="500">
</p>

Client port=60502，HTTP建立连接通常Server port=80

注意到最后的ACK没有Options，因为前两步已完成(MSS, Window, SAK)协商。建立连接消耗了1个序号。

切换到ESTABLISHED状态，可以发送和接收数据了。
    
- 数据通信
    
    ![Untitled](%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2024.png)
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2025.png"
  width="500">
</p>  
    Server发送 PSH+ACK 给Client，push data不需要缓存
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2026.png"
  width="500">
</p>
    
Client没有捎带确认，立即发送单独的ACK

Client发送数据给Server与上述情况类似。
    
- TCP 4-step half-close
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2027.png"
  width="400">
</p>
    Wireshark捕获分组
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/0eaf989b-e76b-40d0-b36a-c50010d53898.png">
</p>

应用结束，执行CLOSE

1. Client发一个FIN+ACK段（seq=1069, ack=1847）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2028.png"  width="500">
</p>
    
2. Server发一个ACK段（seq=1847, ack=1070）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2029.png"
  width="500">
</p>

Client到Server这一方向上的连接关闭，Client进入FIN WAIT2状态。

3. Server发一个FIN+ACK段（seq=1847, ack=1070）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2030.png"  width="500">
</p>
    
4. Client发一个ACK段（seq=1070, ack=1848）
    
<p align="center">
  <img src="%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9CLab2%20a0310bf7c3ec461b99d31825b13f9fc2/Untitled%2031.png"
  width="500">
</p>
    
双方都关闭了连接（不代表TCP连接记录删除）。消耗了1个序号。
    

# 三、实验总结

本次分析实验使我对计算机网络理论课学到的知识有了更清晰、具体的认知，掌握了Wireshark的使用。为了解析报文，我查阅了很多相关文档资料，现在对DHCP, ARP, ICMP这些辅助控制协议，以及TCP有了更深的理解。

第一部分ping没看到理论上该看到的ARP报文，查资料排查原因，为了看到正统过程我找了同一子网下的虚拟机IP，然而在虚拟机联网上花费了大量时间（Ubuntu 22.04和旧版本有一定区别）过程有点坎坷，但总体来说还是有较大收获的。
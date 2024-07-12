# 基于多线程的网络抓包程序 {ignore}

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [实现](#实现)
- [开发环境及工具](#开发环境及工具)
- [设计思路](#设计思路)
- [类的关系](#类的关系)
- [评价](#评价)
  - [线程设计](#线程设计)
  - [面向对象设计原则](#面向对象设计原则)
  - [设计模式](#设计模式)
- [系统使用说明](#系统使用说明)
  - [配置](#配置)
    - [依赖](#依赖)
    - [项目结构](#项目结构)
  - [编译运行](#编译运行)
  - [使用](#使用)
  - [运行效果](#运行效果)
- [总结](#总结)

<!-- /code_chunk_output -->


# 实现

1、实时自动捕获指定网络接口的数据包；

2、可以在任何时候通过设置仅捕获指定IP的数据包；

3、对捕获到的数据包进行解析，提取出协议头部、数据载荷等信息；

4、图形用户界面；

5、多线程。

# 开发环境及工具

- Windows 11
- JDK 21.0.2
- Visual Studio Code
- Gradle
- Pcap4J
- Swing

# 设计思路

我理解的本作业的要求是做一个类似Wireshark的网络抓包程序，UI界面布局基本都是仿照着做的。通过多线程实现捕获和处理数据包，提高了程序的响应性和效率。

<div style="display: flex; justify-content: center; align-items: center;">
  <img src="%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled.png" width="20%" style="margin-right: 50px;"/>
  <img src="%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled.jpeg" width="20%"/>
</div>

![Untitled](%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled%201.png)

![Untitled](%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled%202.png)

一开始的设计是Main, Capture, UI这3个类，捕获分析一个线程，处理用户输入一个线程。

在完成过程中为了debug以及面向对象设计原则，最后完整版是Main, Capture, Parser, UI, Controller, Logger

# 类的关系

生成的UML类图

<p align="center">
  <img src=%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled%203.png>
</p>

- Main 类为程序入口，`main`通过 `SwingUtilities.invokeLater` 调用 UI 类；
- UI 类负责创建和显示图形用户界面，并与 Controller 交互；
- Controller 类管理 UI 组件的行为，并处理开始、停止捕获以及更新过滤器的操作；
- Capture 类实现数据包捕获逻辑，运行在单独的线程中；
    - PacketHandler 是一个函数接口，用于处理捕获的数据包；
- Parser 类用于解析数据包并返回解析后的信息；
- Logger 类实现单例模式，用于记录日志信息；

# 评价

## 线程设计

- 多线程
    - Capture实现了`Runnable`接口，其`run`方法中包含了一个循环，运行在一个单独的线程中，这个线程在Controller的`startCapture`方法中启动
    - Swing是单线程的，对大部分Swing对象的修改必须在EDT上进行
    - Controller使用了`ExecutorService`处理用户输入(IP filter)，确保操作在后台线程中执行，异步执行避免了阻塞UI响应
        - `interactExe` 是一个单线程的 `ExecutorService`；`updateFilter` 方法通过 `interactExe.submit` 提交任务
- 线程安全
    - `running`使用`volatile`，抓包运行状态线程之间可见
    - `synchronized`同步对`filterIp`的访问，确保对过滤器的读写操作是原子的，避免线程间的数据不一致或竞态条件
    - `synchronized`用在`getInstance()`方法，确保在多线程环境中，Logger类的实例只会被创建一次，调用`getInstance()`返回的是同一个Logger实例。

## 面向对象设计原则

- SRP
    - Main：启动应用程序；
    - UI：图形化界面；
    - Controller：处理用户交互和控制流程；
    - Capture：捕获数据包；
    - Parser：解析数据包；
    - Logger：记录日志；
- OCP
    - 可复用设计Parser，可通过增加新的解析方法扩展支持的协议类型
- DIP
    - 尽量使用抽象层，Capture依赖于一个抽象的 `PacketHandler` 接口

## 设计模式

- 单例模式
    - Logger
    - 在全局范围内只有一个实例。通过私有构造函数和公共静态方法 `getInstance()` 实现该模式。单例模式的优势在于节省资源，并确保日志记录的统一性。
- MVC 模式
    - Model: Capture, Parser
    - View: UI
    - Controller: Controller
    - 分离逻辑、界面、控制流程，利于提高代码的可维护性和可扩展性。

# 系统使用说明

## 配置

### 依赖

build.gradle

```java
plugins {
    id 'application'
    id 'java'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.guava:guava:31.1-jre'
    implementation 'org.pcap4j:pcap4j-core:1.8.2'
    implementation 'org.pcap4j:pcap4j-packetfactory-static:1.8.2'
    implementation 'org.pcap4j:pcap4j-distribution:1.8.2'
    implementation 'ch.qos.logback:logback-classic:1.2.9'
    testImplementation 'junit:junit:4.13.2'
}
```

 JDK 1.2 开始自带Swing，无需添加依赖

### 项目结构

```css
com.javafinal/
├── .gradle/
├── app/
│   ├── build/
│   └── src/
│       ├── main/
│       │   ├── java/
│       │   │   └── com/
│       │   │       └── javafinal/
│       │   │           ├── Capture.java
│       │   │           ├── Controller.java
│       │   │           ├── Logger.java
│       │   │           ├── Main.java
│       │   │           ├── Parser.java
│       │   │           └── UI.java
│       │   └── resources/
│       │       └── icon.png
│       └── test/
│           ├── java/
│           └── resources/
├── build.gradle
├── gradle/
├── .gitattributes
├── .gitignore
├── gradlew
├── gradlew.bat
└── settings.gradle
```

## 编译运行

```bash
gradle build
gradle run
```

## 使用

1. 在界面上方的下拉菜单中选择要监控的网络接口，输入指定IP（或在抓包过程中随时输入IP后点击 ’➤’，输入非法按钮无效，同时会筛选之前捕获的内容）
2. 点击‘Start!!’，开始抓包；捕获的分组实时显示在下方表格中
3. 点击‘Stop!!’，停止抓包
4. 可以查看日志文件debug.log，其中包括网络数据包信息和更新filter的情况

## 运行效果

![Untitled](%E5%9F%BA%E4%BA%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%9A%84%E7%BD%91%E7%BB%9C%E6%8A%93%E5%8C%85%E7%A8%8B%E5%BA%8F%20bafb2708e8954ef893ce538bc75d1ae9/Untitled%204.png)


# 总结

本项目实现了一个类似Wireshark的网络数据包捕获分析工具。该工具可以实时监控指定网络接口的数据包，应用IP地址过滤器进行筛选。系统使用了多线程，保证了在捕获数据包的同时，用户界面仍能保持响应。

通过本项目，我学习了Pcap4J和Swing的使用，掌握了Java多线程。根据面向对象的设计原则，不断优化项目结构，加深了我对Java面向对象的理解，顺便复习了一些计算机网络知识。
---
title: 在Mac上部署Jenkins
categories: [Tech]
tags: [jenkins]
date: 2019-11-23
---

## 安装 Jenkins

官网目前推荐的方式是docker运行Jenkins，只需要一条命令就可以搞定。docker是很好用，不过也会有一些不方便的地方：

- 不能完全访问本地磁盘，需要挂载后才可以，而挂载某个目录还需要提前在docker客户端注册，有点绕。
- 不能访问本地代理，大家都知道我们的网络条件不是很好，可能会自建代理，docker中使用代理也不方便。

文件读写的问题有网友说可以通过rsync之类的软件解决，听上去可行，其实也不方便。所以到最后，我们可能还是选择在本地安装Jenkins。

在官网选择适合MacOSX的pkg下载后双击开始安装，输入本机密码后就可以完成安装并且Jenkins默认会启动，但是有可能你发现什么都没发生。注意，此处有坑。

1. 你本机需要有java的虚拟机环境，而且必须是8-11版本的，12以上的不支持（截止2019/12）
2. 你本机的8080端口不能有别的服务

你可以通过运行这个命令来进行启动测试：

```
sh /Library/Application\ Support/Jenkins/jenkins-runner.sh
```

你可以cat一下这个文件，执行的时候也是有回显的，比较容易知道问题出在哪。你还可以通过下面的命令来看本机有哪些目录和文件是Jenkins创建的：

```
find / -iname "*jenkins*" 2>/dev/null
```

## 配置 Jenkins

在这个目录下面有一个简单的文档介绍了怎么配置Jenkins：

- /Library/Documentation/Jenkins/command-line-preferences.html

当然，这些配置都是比较底层的，列出当前存在的配置项目：

```
$ defaults read /Library/Preferences/org.jenkins-ci
{
    heapSize = 512m;
    httpPort = 8080;
    minHeapSize = 256m;
    minPermGen = 256m;
    permGen = 512m;
    tmpdir = "/Users/Shared/Jenkins/tmp";
}
```

修改默认端口的命令：

```
$ sudo defaults write /Library/Preferences/org.jenkins-ci httpPort 8090
```

可以配置的选项如下：

- prefix
- httpPort
- httpListenAddress
- httpsPort
- httpsListenAddress
- war (Defaults to `/Applications/Jenkins/jenkins.war`)
- JENKINS_HOME (Defaults to `/Users/Shared/Jenkins`)
- minHeapSize (Defaults to 256m on 64bit architectures and 64m on 32bit)
- heapSize (Defaults to 512m on 64bit architectures and 128m on 32bit)
- minPermGen (Defaults to 256m on 64bit architectures and 64m on 32bit)
- permGen (Defaults to 512m on 64bit architectures and 128m on 32bit)

你可以删掉某个配置从而使用默认值：

```
$ sudo defaults remove /Library/Preferences/org.jenkins-ci JENKINS_HOME
```

Jenkins 安装后默认会建立一个标准用户名为 jenkins，Jenkins 系统本身的配置会放在`JENKINS_HOME`目录里，这个目录上面已经提到，默认在 `/Users/Shared/Jenkins`，Jenkins 启动后的设置和安装的插件都会被放在这里，包括 job 的 workspace 等等。

Jenkins 默认的日志目录在 `/var/log/jenkins`，系统运行的错误和异常可以在这里找找。

## 启动和停止 Jenkins

如果为了调试，可以用这个命令：

```
sh /Library/Application\ Support/Jenkins/jenkins-runner.sh
```

如果是正常使用，启动和停止的命令如下：

```
$ sudo launchctl load /Library/LaunchDaemons/org.jenkins-ci.plist
$ sudo launchctl unload /Library/LaunchDaemons/org.jenkins-ci.plist
```

为了方便日后的管理，建议将这两条命令配置成 `alias` 放到你的 bash 启动脚本里，比如这样。

```
# your ~/.bash_profile

alias start-jenkins="sudo launchctl load /Library/LaunchDaemons/org.jenkins-ci.plist";
alias stop-jenkins="sudo launchctl unload /Library/LaunchDaemons/org.jenkins-ci.plist";
```

## 更新 Jenkins

不出意外，按照 Jenkins 网页端的引导就可以完成 Jenkins 的更新。如果网络条件很差，你也可以到官网下载war包，然后替换 `/Applications/Jenkins/jenkins.war` 即可，期间需要手动停止和启动服务。

## 卸载 Jenkins

Google搜出来的排在比较靠前的卸载方案是：

1. 手动删除 war 包
2. 手动删除 `JENKINS_HOME` 目录
3. 手动删除 jenkins 用户

但其实不用那么麻烦，只需要一条命令即可。

```
sh  /Library/Application\ Support/Jenkins/Uninstall.command
```

期间需要输入本机管理员密码，大致输出如下。

```
Jenkins uninstallation script

The following commands are executed using sudo, so you need to be logged
in as an administrator. Please provide your password when prompted.

+ sudo launchctl unload /Library/LaunchDaemons/org.jenkins-ci.plist
Password:
+ sudo rm /Library/LaunchDaemons/org.jenkins-ci.plist
+ sudo rm -rf /Applications/Jenkins '/Library/Application Support/Jenkins' /Library/Documentation/Jenkins
+ sudo rm -rf /Users/Shared/Jenkins
+ sudo rm -rf /var/log/jenkins
+ sudo rm -f /etc/newsyslog.d/jenkins.conf
+ sudo dscl . -delete /Users/jenkins
+ sudo dscl . -delete /Groups/jenkins
+ pkgutil --pkgs
+ grep 'org\.jenkins-ci\.'
+ xargs -n 1 sudo pkgutil --forget
Forgot package 'org.jenkins-ci.support.pkg' on '/'.
Forgot package 'org.jenkins-ci.documentation.pkg' on '/'.
Forgot package 'org.jenkins-ci.jenkins21903.postflight.pkg' on '/'.
Forgot package 'org.jenkins-ci.launchd-jenkins.pkg' on '/'.
Forgot package 'org.jenkins-ci.jenkins.osx.pkg' on '/'.
+ set +x
```

## 小结

在 Mac 上部署 Jenkins 有点像鸡肋，食之无味，弃之不舍。如果一定要在 Mac 上需要完成一些自动化的任务，同时希望配置简单友好，不知道你有没有更好的办法？
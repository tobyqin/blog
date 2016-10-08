---
title: Python中的logging模块
date: 2016-10-08 20:57:43
tags: python
categories: Coding
---
今天修改了项目里的logging相关功能，用到了python标准库里的logging模块，在此做一些记录。主要是从官方文档和stackoverflow上查询到的一些内容。

- [官方文档](https://docs.python.org/2.7/library/logging.html)
- [技术博客](http://blog.csdn.net/balderfan/article/details/7644807)

## 基本用法
下面的代码是一些最基本的用法。

```python
# -*- coding: utf-8 -*-

import logging
import sys

# 获取logger实例
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

# 文件日志
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

# 输出不同级别的log
logger.debug('this is debug info')
logger.info('this is information')
logger.warn('this is warning message')
logger.error('this is error message')
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')

# 2016-10-08 21:59:19,493 INFO    : this is information
# 2016-10-08 21:59:19,493 WARNING : this is warning message
# 2016-10-08 21:59:19,493 ERROR   : this is error message
# 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
# 2016-10-08 21:59:19,493 CRITICAL: this is critical message

# 移除一些日志处理器
logger.removeHandler(file_handler)
```

处理这些基本用法，还有一些技巧性的东西可以分享一下。

### 格式化输出日志
```python
# 格式化输出
service_name = "Booking"
logger.error('%s service is down!' % service_name)  # 使用python自带的字符串格式化，不推荐
logger.error('%s service is down!', service_name)  # 使用logger的格式化，推荐
logger.error('%s service is %s!', service_name, 'down')  # 多参数格式化

# 2016-10-08 21:59:19,493 ERROR   : Booking service is down!
# 2016-10-08 21:59:19,493 ERROR   : Booking service is down!
# 2016-10-08 21:59:19,493 ERROR   : Booking service is down!
```

### 记录异常信息
```python
# 记录异常信息
try:
    1 / 0
except:
    # 等同于error级别，但是会额外输出当前抛出的异常
    logger.exception('this is an exception message')

# 2016-10-08 21:59:19,493 ERROR   : this is an exception message
# Traceback (most recent call last):
#   File "D:/Git/py_labs/demo/use_logging.py", line 45, in <module>
#     1 / 0
# ZeroDivisionError: integer division or modulo by zero
```

### 配置要点

#### GetLogger()
这是最基本的入口，该方法参数可以为空，默认值是root，如果在同一个程序中一直都使用同一个name的logger，其实拿到的会是同一个实例，使用这个技巧就可以跨模块调用同样的logger来记录日志。

#### Formatter
Formatter对象定义了log信息的结构和内容，构造时需要带两个参数：
- 一个是格式化的模板fmt，默认只有 `message`
- 一个是格式化的时间样式，默认为 `2003-07-08 16:49:45,896 (%Y-%m-%d %H:%M:%S)`

fmt中允许使用的变量可以参考下表。
| formater | comment |
|--------|--------|
|%(name)s                 |          Logger的名字|
|%(levelno)s               |         数字形式的日志级别|
|%(levelname)s          |        文本形式的日志级别|
|%(pathname)s            |      调用日志输出函数的模块的完整路径名，可能没有|
|%(filename)s              |       调用日志输出函数的模块的文件名|
|%(module)s           |           调用日志输出函数的模块名|
|%(funcName)s         |        调用日志输出函数的函数名|
|%(lineno)d           |              调用日志输出函数的语句所在的代码行|
|%(created)f          |              当前时间，用UNIX标准的表示时间的浮点数表示|
|%(relativeCreated)d  |       输出日志信息时的，自Logger创建以来的毫秒数|
|%(asctime)s          |            字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒|
|%(thread)d           |              线程ID。可能没有|
|%(threadName)s       |       线程名。可能没有|
|%(process)d          |            进程ID。可能没有|
|%(message)s          |         用户输出的消息|

#### SetLevel
Logging有如下级别: DEBUG，INFO，WARNING，ERROR，CRITICAL
默认级别是WARNING，logging模块只会输出指定level以上的log。这样的好处, 就是在项目开发时debug用的log，在产品release阶段不用一一注释，只需要调整logger的级别就可以了，很方便的。

#### Handler
最常用的是StreamHandler和FileHandler, 用于向不同的输出端打log。
Logging包含很多handler, 可能用到的有下面几种
- **StreamHandler** instances send error messages to streams (file-like objects).
- **FileHandler** instances send error messages to disk files.
- **RotatingFileHandler** instances send error messages to disk files, with support for maximum log file sizes and log file rotation.
- **TimedRotatingFileHandler** instances send error messages to disk files, rotating the log file at certain timed intervals.
- **SocketHandler** instances send error messages to TCP/IP sockets.
- **DatagramHandler** instances send error messages to UDP sockets.
- **SMTPHandler** instances send error messages to a designated email address.

#### Configuration
logging的配置大致有下面几种方式。
1. 通过代码进行完整配置，参考上面的例子，主要是getLogger方法
2. 通过代码进行简单配置，后面有例子，主要是basicConfig方法
3. 通过配置文件配置，后面有例子，主要是 `logging.config.fileConfig(filepath)`

##### logging.basicConfig

basicConfig提供了非常便捷的方式让你配置logging模块并马上开始使用，可以参考下面的例子。具体可以配置的项目请查阅[官方文档](https://docs.python.org/2/library/logging.html#logging.basicConfig)。

```python
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
```
备注： 其实你甚至可以什么都不配置直接使用默认值在控制台中打log，用这样的方式替换print方法对日后维护会有很大帮助。

##### 通过文件配置logging

如果你希望通过配置文件来管理logging，类似于log4net或者log4j的方式，可以参考这个[官方文档](https://docs.python.org/2/library/logging.config.html)。
```cfg
# logging.conf
[loggers]
keys=root

[logger_root]
level=DEBUG
handlers=consoleHandler
#,timedRotateFileHandler,errorTimedRotateFileHandler

#################################################
[handlers]
keys=consoleHandler,timedRotateFileHandler,errorTimedRotateFileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_timedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('debug.log', 'H')

[handler_errorTimedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=WARN
formatter=simpleFormatter
args=('error.log', 'H')

#################################################
[formatters]
keys=simpleFormatter, multiLineFormatter

[formatter_simpleFormatter]
format= %(levelname)s %(threadName)s %(asctime)s:   %(message)s
datefmt=%H:%M:%S

[formatter_multiLineFormatter]
format= ------------------------- %(levelname)s -------------------------
 Time:      %(asctime)s
 Thread:    %(threadName)s
 File:      %(filename)s(line %(lineno)d)
 Message:
 %(message)s

datefmt=%Y-%m-%d %H:%M:%S
```
代码中的调用。
```python
import os
filepath = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(filepath)
return logging.getLogger()
```







# <center>PyWxDump</center>

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/xaoyaoo/PyWxDump.svg?style=social&label=Star)](https://github.com/xaoyaoo/PyWxDump)

* 更新日志（发现[version_list.json](app/version_list.json)
  缺失或错误，请提交[issues](https://github.com/xaoyaoo/PyWxDump/issues))：
    * 2023.10.14 整体重构项目，优化代码，增加命令行统一操作
    * 2023.10.11 添加"3.9.5.81"版本的偏移地址[#10](https://github.com/xaoyaoo/PyWxDump/issues/10),
      感谢@[sv3nbeast](https://github.com/sv3nbeast)
    * 2023.10.09 获取key基址偏移可以根据微信文件夹获取，不需要输入key
    * 2023.10.09 优化代码，删减没必要代码，重新修改获取基址代码，加快运行速度（需要安装新的库 pymem）
    * 2023.10.07 修改获取基址内存搜索方式，防止进入死循环
    * 2023.10.07 增加了3.9.7.29版本的偏移地址
    * 2023.10.06 增加命令行解密数据库
    * 2023.09.28 增加了数据库部分解析
    * 2023.09.15 增加了3.9.7.25版本的偏移地址

# 一、项目介绍

本项目可以获取微信基本信息，以及key，通过key可以解密微信数据库，获取聊天记录，好友信息，群信息等。

该分支是[SharpWxDump](https://github.com/AdminTest0/SharpWxDump)的经过重构python语言版本，同时添加了一些新的功能。

**目录结构**

```
PyWxDump
├─ app                        # 项目代码,存放各个模块
│  ├─ analyse                     # 解析数据库
│  │  └─ parse.py                     # 解析数据库脚本，可以解析语音、图片、聊天记录等
│  ├─ bias_addr                   # 获取偏移地址
│  │  └─ get_bias_addr.py             # 获取偏移地址脚本
│  ├─ decrypted                   # 解密数据库
│  │  ├─ decrypt.py                   # 解密数据库脚本
│  │  └─ get_wx_decrypted_db.py       # 直接读取当前登录微信的数据库，解密后保存到当前目录下的decrypted文件夹中
│  ├─ wx_info                     # 获取微信基本信息
│  │  ├─ get_wx_info.py               # 获取微信基本信息脚本
│  │  └─ get_wx_db.py                 # 获取本地所有的微信相关数据库
│  └─ version_list.json           # 微信版本列表
├─ doc                        # 项目文档
│  ├─ wx数据库简述.md               # wx数据库简述
│  └─ CE获取基址.md                 # CE获取基址
├─ main.py                  # 命令行入口
├─ README.md              
└─ requirements.txt
```

<strong><big>
超级想要star，走过路过，帮忙点个[![Star](https://img.shields.io/github/stars/xaoyaoo/PyWxDump.svg?style=social&label=Star)](https://github.com/xaoyaoo/PyWxDump/)
呗，谢谢啦~</big></strong>

# 二、使用方法

## 1. 安装依赖

```shell script
pip install -r requirements.txt
```

**说明**：

1. requirements.txt中的包可能不全，如果运行报错，请自行安装缺少的包
2. 如果运行报错，请检查python版本，本项目使用的是python3.10
3. 安装pycryptodome时可能会报错，可以使用下面的命令安装，自行搜索解决方案（该包为解密的核心包）

## 2. 使用方法

### 2.1 命令行

```shell script
python main.py [模式] [参数]
#  运行模式(mode):
#    bias_addr     获取微信基址偏移
#    wx_info       获取微信信息
#    wx_db         获取微信文件夹路径
#    decrypt       解密微信数据库
#    analyse       解析微信数据库(未完成)
#    all           执行所有操作(除获取基址偏移、Analyse)
```

*示例*

以下是示例命令：

```shell script
python main.py bias_addr -h
#usage: main.py bias_addr [-h] --mobile MOBILE --name NAME --account ACCOUNT [--key KEY] [--db_path DB_PATH] [-vlp VLP]
#options:
#  -h, --help         show this help message and exit
#  --mobile MOBILE    手机号
#  --name NAME        微信昵称
#  --account ACCOUNT  微信账号
#  --key KEY          (与db_path二选一)密钥
#  --db_path DB_PATH  (与key二选一)已登录账号的微信文件夹路径
#  -vlp VLP           (可选)微信版本偏移文件路径

python main.py wx_info -h
#usage: main.py wx_info [-h] [-vlp VLP]
#options:
#  -h, --help  show this help message and exit
#  -vlp VLP    (可选)微信版本偏移文件路径

python main.py wx_db -h
#usage: main.py wx_db [-h] [-r REQUIRE_LIST] [-wf WF]
#options:
#  -h, --help            show this help message and exit
#  -r REQUIRE_LIST, --require_list REQUIRE_LIST
#                        (可选)需要的数据库名称(eg: -r MediaMSG;MicroMsg;FTSMSG;MSG;Sns;Emotion )
#  -wf WF                (可选)'WeChat Files'路径

python main.py decrypt -h
#usage: main.py decrypt [-h] -k KEY -i DB_PATH -o OUT_PATH
#options:
#  -h, --help            show this help message and exit
#  -k KEY, --key KEY     密钥
#  -i DB_PATH, --db_path DB_PATH
#                        数据库路径(目录or文件)
#  -o OUT_PATH, --out_path OUT_PATH
#                        输出路径(必须是目录),输出文件为 out_path/de_{original_name}

python main.py analyse -h
#usage: main.py analyse [-h] [--arg ARG]
#options:
#  -h, --help  show this help message and exit
#  --arg ARG   参数

python main.py all -h
#usage: main.py all [-h]
#options:
#  -h, --help  show this help message and exit
```

### 2.2 python API

```python
from app import *
# 单独使用各模块，返回值一般为字典，参数参考命令行
```

【注】:

* 关于基址使用cheat engine获取，参考[CE获取基址.md](doc/CE获取基址.md)
* 关于数据库解析，参考[wx数据库简述.md](doc/wx数据库简述.md)
* 关于更多使用方法，以及各个模块的使用方法，参考前一版本的[python1.0_README.md](doc/python1.0_README.md)

## 三、支持功能

1. 支持微信多开场景，获取多用户信息等
2. 微信需要登录状态才能获取数据库密钥

**版本差异**

1. 版本 < 3.7.0.30 只运行不登录能获取个人信息，登录后可以获取数据库密钥
2. 版本 > 3.7.0.30 只运行不登录不能获取个人信息，登录后都能获取

**利用场景**

1. 钓鱼攻击(通过钓鱼控到的机器通常都是登录状态)
2. 渗透到运维机器(有些运维机器会日常登录自己的微信)
3. 某些工作需要取证(数据库需要拷贝到本地)
4. 自行备份(日常备份自己留存)
5. 等等...............

## 四、免责声明（非常重要！！！！！！！）

本项目仅允许在授权情况下对数据库进行备份，严禁用于非法目的，否则自行承担所有相关责任。使用该工具则代表默认同意该条款;

请勿利用本项目的相关技术从事非法测试，如因此产生的一切不良后果与项目作者无关。

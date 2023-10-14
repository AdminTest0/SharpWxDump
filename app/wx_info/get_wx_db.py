# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         get_wx_db.py
# Description:  
# Author:       xaoyaoo
# Date:         2023/10/14
# -------------------------------------------------------------------------------
import os
import re
import winreg


def get_wechat_db(require_list: [list | str] = "all", msg_dir: str = None):
    if not msg_dir:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat", 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, "FileSavePath")
            winreg.CloseKey(key)
            w_dir = value
        except Exception as e:
            w_dir = "MyDocument:"

        if w_dir == "MyDocument:":
            profile = os.path.expanduser("~")
            msg_dir = os.path.join(profile, "Documents", "WeChat Files")
        else:
            msg_dir = os.path.join(w_dir, "WeChat Files")

    if not os.path.exists(msg_dir):
        return "[-] 目录不存在"

    user_dirs = {}  # wx用户目录
    files = os.listdir(msg_dir)
    for file_name in files:
        if file_name == "All Users" or file_name == "Applet" or file_name == "WMPF":
            continue
        user_dirs[file_name] = os.path.join(msg_dir, file_name)

    if isinstance(require_list, str):
        require_list = require_list.split(";")

    if "all" in require_list:
        pattern = {"all": re.compile(r".*\.db$")}
    elif isinstance(require_list, list):
        pattern = {}
        for require in require_list:
            pattern[require] = re.compile(r".*%s.*\.db$" % require)
    else:
        return "[-] 参数错误"

    # 获取数据库路径
    for user, user_dir in user_dirs.items():  # 遍历用户目录
        user_dirs[user] = {n: [] for n in pattern.keys()}
        for root, dirs, files in os.walk(user_dir):
            for file_name in files:
                for n, p in pattern.items():
                    if p.match(file_name):
                        src_path = os.path.join(root, file_name)
                        user_dirs[user][n].append(src_path)
    return user_dirs


if __name__ == '__main__':
    require_list = ["MediaMSG", "MicroMsg", "FTSMSG", "MSG", "Sns", "Emotion"]
    # require_list = "all"
    user_dirs = get_wechat_db(require_list)
    if isinstance(user_dirs, str):
        print(user_dirs)
    else:
        for user, user_dir in user_dirs.items():
            print(f"[+] {user}")
            for n, paths in user_dir.items():
                print(f"    {n}:")
                for path in paths:
                    print(f"        {path}")

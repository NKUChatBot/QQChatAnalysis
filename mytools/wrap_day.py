import os
import re

tools_path = os.path.dirname(os.path.realpath(__file__))
# 需要将此变量替换为mytools的加载路径


def wrap_day(directory):
    """
    通过g++编译器编译WrapDay.cpp程序，并调用该程序将聊天文件中一天的所有聊天记录通过一个class为wrap_day的<div>包装起来
    :param directory:所有待处理的html文件所在的源文件夹
    :return:None
    """
    for path, subdirs, files in os.walk(directory):
        # path->路径; subdirs->path路径下的子目录; files->path路径下的文件
        html_files = [os.path.join(path, f) for f in files if f.endswith(".html")]
        for html in html_files:
            if re.match(r'(\/|\?|<|>|\\|:|\*|\|)', os.path.basename(html)):
                raise Exception("Illegal filename!", html)
            if os.system(os.path.join(tools_path, "WrapDay.exe") + " %s %s" % (html, html+'.swp')) == 0:  # 退出码为0表示正常执行
                # WrapDay编译指令：g++ --std=c++11 WrapDay.cpp -o WrapDay.exe。需要g++支持regex库，至少版本4.9
                os.remove(html)
                os.rename(html+'.swp', html)
                print("%s has overwrite %s" % (html+".swp", html))


if __name__=="__main__":
    wrap_day(r'D:\mine\office\WorkPlace\GCBX\QQChatSourceFile\mytools')
import os
import re
import sys

tools_path = os.path.dirname(os.path.realpath(__file__))
# 需要将此变量替换为mytools的加载路径


def export_mht_img(directory):
    for path, subdirs, files in os.walk(directory):
        mht_files = [os.path.join(path, f) for f in files if f.endswith(".mht")]
        if not mht_files:  # 如果当前文件夹下没有mht文件，则跳过该层循环
            continue

        if [d for d in subdirs if d.find( os.path.splitext(os.path.basename(mht_files[0]))[0] ) != -1]:
            # 如果存在mht文件对应的图片文件导出文件夹
            print("This mht file's img has been export once!", file=sys.stderr)
            return False

        for mht in mht_files:
            if re.match(r'(\/|\?|<|>|\\|:|\*|\|)', os.path.basename(mht)):
                raise Exception("Illegal filename!", mht)
            os.system(os.path.join(tools_path, "QQMhtToHtml.exe") + " " + mht)
    return True


def cut_mht_tail(directory):
    part_preffix = "------=_NextPart_"  # mht文件中分割每个部分的分隔符

    for path, subdirs, files in os.walk(directory):
        mht_files = [os.path.join(path, f) for f in files if f.endswith(".mht")]
        for mht in mht_files:
            with open(mht, "r", encoding='utf-8', errors='ignore') as rf:
                raw_mht = rf.read()

            first_part = raw_mht.find(part_preffix)
            res_html = raw_mht[:raw_mht.find(part_preffix, first_part+len(part_preffix))]
            with open(os.path.splitext(mht)[0]+".html", "w", encoding='utf-8', errors='ignore') as wf:
                wf.write(res_html)
                print("Mht file has convert to Html")


def mht_to_html(directory):
    export_mht_img(directory)
    cut_mht_tail(directory)


if __name__=="__main__":
    mht_to_html(r"D:\mine\office\WorkPlace\GCBX\QQChatSourceFile\mytools")
import os
import re
import sys


def append_sufix(html, imgs, img_path):
    """
    将一个html文件<img>标签链接到对应的文件
    :param html: html文件名（包含路径）
    :param imgs: img文件名列表（不包含路径）
    :param img_path: img文件列表相对html文件的路径
    :return: None
    """
    pattern = [re.compile(r'"('+re.escape(os.path.splitext(img)[0])+r')(.*)?"') for img in imgs]  # 需要替换html文件中的内容

    res_lines = []
    with open(html, "r", encoding='utf-8', errors='ignore') as rf:
        raw_lines = rf.readlines()  # raw_lines -> 文件的原始内容

    if ''.join(raw_lines).find(imgs[0]) != -1:
        print("This file has linked once!", file=sys.stderr)
        return False

    for index, line in enumerate(raw_lines):
        for jndex, img in enumerate(imgs):
            line, rplnum = pattern[jndex].subn('"'+os.path.join(img_path, img)+'"', line)
            if rplnum != 0:  # 我们认为一个图片只有一个<img>与之链接，为了提高速度，不重复regex替换
                del imgs[jndex]
        res_lines.append(line)

        process = index / len(raw_lines)
        p_bar = int(50 * process) * '>' + int(50 * (1 - process)) * '-'
        print("[%s]%.2f" % (p_bar, process * 100) + '%', end='\r')  # 显示进度条@shesl
    print("\n")  # 换行

    with open(html+'.swp', "w", encoding='utf-8') as wf:
        wf.write(''.join(res_lines))
    os.remove(html)
    os.rename(html+".swp", html)
    return True


def link_img(directory):
    """
    将一个文件夹中的所有html文件中的<img>的src链接到生成的图片文件
    :param directory: html文件所在的顶级目录
    :return: None
    """
    for path, subdirs, files in os.walk(directory):
        # path->路径; subdirs->path路径下的子目录; files->path路径下的文件
        for f in os.listdir(os.path.dirname(path)):  # html文件所在的文件夹
            html_file = os.path.join(os.path.dirname(path), f) if f.endswith('.html') else ''  # html文件（包含路径名）
            img_files = [ff for ff in files if ff.endswith(('.jpg', '.png', '.gif'))]  # 选择可能出现的jpg、png、gif文件（不包含路径名）
            if html_file and img_files and os.path.basename(path).find(os.path.splitext(f)[0]) != -1:
                # html文件存在 and 图片文件存在 and html文件跟图片文件是一一对应的
                print("Linking-Img. Working on: "+html_file)
                append_sufix(html_file, img_files, os.path.basename(path))


if __name__ == '__main__':
    link_img(r'D:\mine\office\WorkPlace\GCBX\QQChatSourceFile\mytools')

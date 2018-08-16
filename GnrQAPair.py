import qqCovFile
import mytools
import os

# 预处理，暂时不考虑link-img的问题（速度太慢了）
mytools.mht_to_html('/RunQQChat/')
mytools.wrap_day('/RunQQChat/')

QAP = []
for path, subdirs, files in os.walk("/RunQQChat/"):
    files = [os.path.join(path, f) for f in files if f.endswith(".html")]  # 所有的html文件
    try:
        for filename in files:
            this_group = qqCovFile.load_file(filename)  # 加载html文件中的内容
            QAP = QAP + this_group.get_qa_pair(plain=True)  # 得到html文件中的所有QA对
    except Exception as e:
        print(e)
        print(filename)
        pass


with open("/RunQQChat/QAPiar.txt", "w", encoding="utf-8", errors="ignore") as wf:
    wstr = ["Q:%s\nA:%s" % (qa['Q'], '\nA:'.join(qa['A'])) for qa in QAP]
    wf.write('\n-----------------\n'.join(wstr))
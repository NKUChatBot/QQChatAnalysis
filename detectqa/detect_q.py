import re

QList = ["谁", "何", "怎", "哪", "咋", "啥", "?", "？",
         "什么", "几个", "几只", "几条", "多少",
         "请问", "有没有", "是不是", "会不会", "请教"]


def rule_base(seq):
    """
    基于规则的问题检测方法
    :param seq: 待检测的语句
    :return: 表征是否为问题的boolean值
    """
    for line in seq.split("\n"):
        if re.match(r'.*(呢|吗|？|\?)$', line):
            return True
        for item in QList:
            if line.find(item) != -1:
                return True
    return False


if __name__=='__main__':
    print("Rule Base Module")
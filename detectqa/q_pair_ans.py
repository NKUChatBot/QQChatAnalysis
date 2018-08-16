import re
import jieba


def rule_base(question, answer):
    """
    基于规则的检测问题答案是否匹配
    :param question:传入的问题字符串
    :param answer:传入的答案字符串
    :return:若传入问题大难匹配，则返回True
    """
    if question.find("是谁") > 0:
        major = jieba.lcut(question[:question.find("是谁")])[-1]
        if re.match("(.*)?(" + re.escape(major)+")(是([^谁]+))", answer):
            return True
    elif question.find("是什么") > 0:
        major = jieba.lcut(question[:question.find("是什么")])[-1]
        if re.match("(.*)?(" + re.escape(major) + ")(是([^什么]+))", answer):
            return True
    elif question.find("有几个") > 0:
        major = jieba.lcut(question[:question.find("有几个")])[-1]
        if re.match("(.*)?(" + re.escape(major)+")(有([^几]+)个)", answer):
            return True
    elif question.find("在哪") > 0:
        major = jieba.lcut(question[:question.find("在哪")])[-1]
        if re.match("(.*)?(" + re.escape(major) + ")(在([^哪]+))", answer):
            return True
    return False

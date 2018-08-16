
AdList = ["http://", "https://", "@全体成员"]


def rule_base(seq):
    """
    基于规则的问题检测方法
    :param seq: 待检测的语句
    :return: 表征是否为问题的boolean值
    """
    if len(seq) > 80:
        # 这个长度是通过简单的统计方法得到的，需要进一步机器学习的方式计算
        return True
    for line in seq.split("\n"):
        for item in AdList:
            if line.find(item) != -1:
                return True
    return False


if __name__=='__main__':
    print("Rule Base Module")
# coding: utf-8
# 分析的QQ聊天文文件的python模块

import re
import math
from datetime import datetime, timedelta, tzinfo
from lxml import etree

import detectqa
import detectad


class UTC(tzinfo):  # datetime中没有实例化tzinfo
    """自己实例化的UTC，用于tzinfo的实例化"""
    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


class qqChat(object):
    """
    用于存储分析单个消息的class

    成员变量：
    Person：消息的发送者，由Alias和Id组成，Alias是昵称，ID一般为QQ号，有的情况还会存在头衔Title；
    Time：Python的datetime类，指明这条qq消息发送的时间；
    Text：指明这条消息的发送内容。
    """
    def __init__(self, byWho, atWhen, sayWhat):
        """发言人、发言时间（该类中不存储日期）、说话内容三个字符串作为参数"""
        self.Person = byWho
        try:
            [_, self.Title, self.Alias, self.ID, _] = re.split(r'^(【.*】)?(.*)\((.*)\)$', self.Person)
            # 将Person分解成Alias和Id，ID通常为QQ号。开头结尾会出现空字符串
        except Exception:
            [_, self.Title, self.Alias, self.ID, _] = re.split(r'^(【.*】)?(.*)<(.*)&get;$', self.Person)  # 有出现以<>分割的id

        self.Time = datetime.strptime(atWhen,'%H:%M:%S').time() if isinstance(atWhen, str) else atWhen
        # 将字符串类型的Time转化为python的time模块能处理的类型
        self.Text = sayWhat
        pass

    def __str__(self):
        return '{0.Person}\t{1}\n\t{0.Text}'.format(self,self.Time.strftime('%Y-%m-%d,%H:%M:%S')) if \
            self.Time.tzinfo else '{0.Person}\t{1}\n\t{0.Text}'.format(self,self.Time.strftime('%H:%M:%S'))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.Person == other.Person and self.Text == other.Person and self.Time == other.Time

    def __ne__(self, other):
        return self.Person != other.Person or self.Text != other.Person or self.Time != other.Time

    def is_sys_meg(self):
        """如果这段消息是来自系统消息，返回True"""
        return self.ID == '10000'

    def is_xiaobing_bot(self):
        """如果这段对话是QQ小冰说的，返回True"""
        return self.ID == '2854196306'

    def is_question(self):
        """如果这段消息是一个问题，返回True"""
        return detectqa.rule_detect_q(self.Text)

    def is_advertise(self):
        """如果这段消息是广告，则返回True"""
        return detectad.rule_base(self.Text)

    def find_answer(self, chat_list):
        """
        在本条记录为问题时，用与寻找答案的函数
        :param chat_list: 一个聊天记录的list，寻找答案的来源，不能包含该self本身
        :return:一个qqChat类的list，即为self的回答所有可能值
        """
        chat_list = sorted(chat_list, key=lambda chat: chat.Time)

        delta = 0  # 表征两条消息之间的间隔
        prob_ans = []  # 可能的答案
        for chat in chat_list:
            if delta > 40:  # delta需要优化
                break
            delta = delta + 1
            if chat.ID == self.ID or chat.Time < self.Time or chat.is_sys_meg() or chat.is_xiaobing_bot():
                continue

            if math.log((chat.Time-self.Time).days*86400 + (chat.Time-self.Time).seconds + 1, 10) * delta < 5:
                # 表示5分钟内，2条之内消息都可以作为回答临界。此处模型需要优化
                prob_ans.append(chat)
            elif chat.Text.find('@'+self.Alias if self.Alias else '@ ') != -1:
                if chat.Text.replace('@'+self.Alias, '').strip() != '':
                    prob_ans.append(chat)
            elif detectqa.rule_pair_qa(self.Text, chat.Text):
                prob_ans.append(chat)

        return prob_ans if prob_ans else None


class qqConv(object):
    """用于存储分析一段对话的class"""
    def __init__(self, ChatList, onWhen):
        """传入一个qqChat的List和一个字符串"""
        self.Conv = sorted(ChatList, key=lambda chat:chat.Time)
        self.Day = datetime.strptime(onWhen,'%Y-%m-%d').date()
        pass

    def __str__(self):
        res = self.Day.strftime('%Y-%m-%d')
        for item in self.Conv:
            res += "\n%s"%str(item)
        return res

    def __repr__(self):
        return str(self)

    def add_date(self):
        """
        返回一个同时包含date与time的qqChat的list
        """
        result = []
        for chat in self.Conv:
            date_time = datetime.combine(self.Day, chat.Time).replace(tzinfo=UTC(8))
            result.append(qqChat(chat.Person, date_time, chat.Text))
        return result


class qqGroup(object):
    """用与存储分析多个qqConv，直接对应一个QQ导出的聊天文件"""
    def __init__(self, ConvList, GroupName):
        """传入一个按天存储的qqConv的list和群名"""
        self.Group = sorted(ConvList, key=lambda cov:cov.Day)  # 按天存储的聊天记录
        self.Name = GroupName

    def __str__(self):
        res = ""
        for item in self.Group:
            res += "\n\n%s"%str(item)
        return res

    def merge_day(self):
        """
        返回一个同时包含所有qqConv中所有qqChat的list
        """
        all_conv = []
        for oneDay in self.Group:
            for chat in oneDay.add_date():
                all_conv.append(chat)
        return all_conv

    def get_qa_pair(self, plain=False):
        """
        得到在该群聊天记录中，所有匹配的QA对
        :param plain: 为True时返回值为平凡文本（qqChat.Text），默认值为False
        :return:一个表征QA对的list，每个元素是一个含有Q与A两个键的dict字典
        """
        this_group = self.merge_day()

        print("Get Q-A Pairs from group: %s" % self.Name)
        res = []
        for index, chat in enumerate(this_group):
            process = index / len(this_group)
            p_bar = int(50 * process) * '>' + int(50 * (1 - process)) * '-'
            print("[%s]%.2f" % (p_bar, process * 100) + '%', end='\r')  # 显示进度条@shesl

            if chat.is_sys_meg() or chat.is_xiaobing_bot():
                continue
            if chat.is_advertise() or not chat.is_question():
                continue
            else:
                ans = chat.find_answer(this_group[index+1:])
                if ans:
                    ans = [i.Text.replace("@" + chat.Alias, '').strip().replace("\n", "。") for i in ans] if plain else ans
                    ques = re.sub(r"(@(.*)?[ |\n|\r])", "", chat.Text).strip().replace("\n", "。") if plain else chat
                    res.append({'Q': ques, 'A': ans})
        print("")  # 结束换行
        return res


def load_day(DayRoot):
    """
    以一个lxml的html树的节点为传入值，返回一个包含该天对话的所有qqChat类的list
    """
    chat_date = DayRoot.xpath('.//tr[1]/td/text()')[0].split(': ')[1]
    chat_list = [qqChat(''.join(chas.xpath('./div/div/text()')), ''.join(chas.xpath('./div/text()')),
        '\n'.join(chas.xpath('./div/font/text()'))) for chas in DayRoot.xpath('.//tr/td')[1:]]

    return qqConv(chat_list, chat_date)


def load_file(filename):
    """以一个字符串类型的filename为传入值，以html形式通过lxml库读取filename的内容，返回一个qqGroup类"""
    with open(filename, "r",encoding='utf-8') as rf:
        TreeRoot = etree.HTML(rf.read())
    GName = ''.join(TreeRoot.xpath('//save/table[1]/tr[3]//text()')).split(":", 1)[1]
    WrapDays = TreeRoot.xpath('//div[@class="wrap_day"]')
    return qqGroup([load_day(wrap) for wrap in WrapDays], GroupName=GName)


if __name__=='__main__':
    filepos = 'D:/mine/office/WorkPlace/GCBX/QQChatSourceFile/专业知识/2019沪江网校考研集结23/2019沪江网校考研集结23.html'
    getToRead = load_file(filepos)
    with open("temp.txt", "w", encoding='utf-8') as w:
        w.write(str(getToRead))

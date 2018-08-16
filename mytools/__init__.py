
from mytools.plot_density import plot_density
from mytools.link_img import link_img
from mytools.wrap_day import wrap_day
from mytools.mht_to_html import mht_to_html


def pre_exe(directory):
    """预处理函数，传入一个文件夹，预处理该文件夹下所有的mht文件"""
    mht_to_html(directory)
    link_img(directory)
    wrap_day(directory)

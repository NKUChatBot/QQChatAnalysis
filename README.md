# QQ聊天文件分析

## 1. Mht2Html.sh

- 一个将Mht转化为Html文件的bash脚本
- 使用`./Mht2Html.sh $folder`命令可以运行，会将folder文件夹以及其子文件夹下的所有mht文件转化为html文件
1. 脚本首先调用QQMhtToHtml.exe提取图片，生成临时tphtml文件与mht文件中的图片会存在与一个新建的文件夹下
    - <a href="https://github.com/Baozisoftware/QQMhtToHtml">QQMhtToHtml.exe</a>
2. 该bash脚本会调用CutFileTail的Python程序，截断tphtml文件后的base64部分，留下含tag的html文本部分
    - CutFileTail.py &rarr; 接受三个输入参数：输入文件名，输出文件名，截断标志字符串

## 2. LinkImg.sh

- 该bash脚本脚本会遍历之前提取的图片，并通过调用RplSubStr.py，将html文件中的<image>的src链接到生成的文件中
  - RplSubStr.py &rarr; 接受三个参数：处理文件的文件名，引号内的不包含扩展名的文件名，替换的文件名以及扩展名。比如：
  - 输入文件内容以及文件名 &rarr; `<image src = "ImageFile.dat"></image> # HtmlFile.html`
  - 输入命令 &rarr; `pyhton RplSubStr.py HtmlFile.html ImageFile ImageFile.jpg`
  - 输出文件内容以及文件名 &rarr; `<image src = "ImageFile.jpg"></image> # HtmlFile.html`

## 3. WrapDay.sh

- 该bash脚本通过g++编译器编译WrapDay.cpp程序，并调用该程序将聊天文件中一天的所有聊天记录通过一个class为wrap_day的div包装起来
  - WrapDay.cpp &rarr; 可以接受两个参数为输入文件名与输出文件名（若不满两个，会从标准输入中读入）
  - WrapDay.cpp通过c++11的regex库，识别文件开头与结束

## Other

1. **`recovery.sh`** &rarr; 恢复备份的所有的html文件
2. **`backup.sh`** &rarr; 备份所有的html文件
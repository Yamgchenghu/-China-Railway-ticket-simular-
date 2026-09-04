import pygame
import tkinter as tk
import multiprocessing
from multiprocessing import Manager
import sys
import os
import time
import pyperclip
from pypinyin import lazy_pinyin



bbh = "3.0.11  260726  最终开源版"
data_max_need_lines = 65

###作者不再更新，以下注释内容写于2026.07.26(火车票根生成器定稿14月)
"""
1. 本系统通过files/dlc.py库支持运行，该库拥有以下功能:
    pygame文字显示
        1.fontupload(a,b,c)
            功能：向系统导入字体
            参数：
                a 字符串 文件路径（相对/绝对）
                b 整数 字体大小
                c 整数 字体序号（默认0号，0~无穷）
            返回值：
                没有
            *注：后续需要使用output和moutput需要先调用fontupload函数导入字体，字体序号别太大会导致列表增加一堆空值
        2.output(screen,a,(r,g,b),(x,y),t,n)
            功能：在指定位置以指定字体显示文字
            参数：
                screen pygame.Surface 屏幕表面
                a 字符串 要显示的文字
                (r,g,b) 整数*3 文体颜色（各0~255，不可以16进制表示）
                (x,y) 整数*2 文字模块左上角位置
                t 整数 透明度（0~255，越小越看不见，默认255）
                n 整数 字体序号（默认0号，0~无穷，必须导入过，否则终端会刷屏报错）
            返回值：
                没有
            *注：如果字符串中没有控制字符，建议使用output节省性能
        3.mlength(a,b)
            功能：计算在moutput模式下执行含基础指令的字符串的长度
            参数：
                a 字符串 要计算的字符串
                b 整数 字体序号（默认0号，0~无穷，必须导入过，否则终端会刷屏报错）
            返回值：
                整数 字符串横向长度
            *注：适用于居中对齐场景（更耗性能）
        4.csckg(a,b,c)
            功能：测试output模式下的长宽高
            参数：
                a 字符串 要计算的字符串
                b 整数 字体序号（默认0号，0~无穷，必须导入过，否则终端会刷屏报错）
                c 整数 长度或宽度（0：横向长度，1：纵向宽度，其他：列表返回）
            返回值：
                整数 字符串横向长度或纵向高度 或 列表[整数,整数] 字符串横向长度和纵向高度
            *注：适用于居中对齐场景
        5.moutput(screen,a,(r,g,b),(x,y),t,n)
            功能：在指定位置以指定样式显示文字
            参数：
                screen pygame.Surface 屏幕表面
                a 字符串 要显示的文字
                (r,g,b) 整数*3 文体颜色（各0~255，不可以16进制表示）
                (x,y) 整数*2 文字模块左上角位置
                t 整数 透明度（0~255，越小越看不见，默认255）
                n 整数 字体序号（默认0号，0~无穷，必须导入过，否则终端会刷屏报错）
            返回值：
                没有
            *注：本质是逐字符for循环迭代并用output函数渲染，遇到控制字符执行指令，因此性能损耗是output的很多倍，取决于字符长度
            **常用指令
                *移动类
                    #x000 设置横向坐标（必须跟3位整数，<100的首位加0）
                    #x+0000 设置横向坐标（必须跟4位整数）
                    #y0000 设置纵向坐标（必须跟3位整数，<1000的首位加0）
                    #x+=000 设置横向坐标向右偏移（必须跟3位整数，<100的首位加0）
                    #y+=000 设置纵向坐标向下偏移（必须跟3位整数，<100的首位加0）
                    #x-=000 设置横向坐标向左偏移（必须跟3位整数，<100的首位加0）
                    #y-=000 设置纵向坐标向上偏移（必须跟3位整数，<100的首位加0）
                    #n 直接换行（自动计算列高并将横轴移动至函数设定横坐标位置）
                *颜色类
                    #R 红色 （255，0，0）
                    #G 绿色 （0，255，0）
                    #B 蓝色 （0，0，255）
                    #W 白色 （255，255，255）
                    #P 粉色 （255，130，104）
                    #Y 黄色 （255，255，0）
                    #O 橙色 （255，128，0）
                    #Z 紫色 （255，0，255）
                    #D 淡紫 （218，112，214）
                    #L 淡蓝 （173，216，230）
                    #C 淡绿 （152，251，152）
                    #H 灰色 （120，120，120）
                    #l 天蓝 （123，213，231）
                    #c255255255 自定义颜色（必须9位连续数字，每3位范围000~255，不支持16进制）
                    ### 恢复初始颜色（在moutput函数内设置的颜色）
                *切换字体
                    #0 切换至第0号字体（该版本支持0~39，需要增加可在dlc.py中手动增加。首位不加0）
                *《火车票根生成器》专属
                    #零000 在字符周围自动画一个大圈（此处000为半径长度，首位加0）
                    #一00 在字符中间以00号字体绘制一条删除线（用于￥符号，00可不填，不填默认读取当前的num值，若填写首位须加0）
                *调整透明度
                    #tm=000 调整透明度 （000~255，首位加0，不支持16进制）
                *占位符
                    $ 占位符 隔绝控制字符与实际输出字符以免发生意外
                    #$ 取消占位符 强制输出$（以当前所有状态） （beta）


"""
def resource_path(relative_path, is_inside=0):##打包时用·获取绝对路径
    if hasattr(sys, '_MEIPASS') and is_inside == 1:
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def mopen(file_path, mode='r', encoding='utf-8', is_inside=0):#自动填充绝对路径，传入相对路径以绝对路径方式打开
    return open(resource_path(file_path, is_inside=is_inside), mode, encoding=encoding)

try:
    import files.dlc as dlc##导入dlc.py
except ImportError:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(current_dir, "dlc"))
    import files.dlc as dlc

backup_dir = os.path.join(os.path.dirname(resource_path("data.txt")), "备份")##为编辑系统创建备份（不需要的备份文件请手动删除）
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def load_data(shared_data):##读取data.txt存档文件（车票信息）
    with mopen(resource_path("data.txt")) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == "$":
                line = ""
            while len(shared_data) <= i:
                shared_data.append("")
            shared_data[i] = line
    
    backup_file = os.path.join(backup_dir, f"data_{time.strftime('%Y%m%d%H%M%S')}.txt")
    if 1:                                 ##不需要的把这一行改成0（如果不好使就改回来）
        with mopen(backup_file, 'w') as f:##自动创建备份
            for i in range(len(shared_data)):
                try:
                    line = shared_data[i]
                    if line[-1] != "\n":
                        f.write(line + '\n')
                    else:
                        f.write(line)
                except:
                    f.write(str(shared_data[i]))

def save_data(shared_data):##保存存档文件（车票信息）
    data_copy = list(shared_data)
    for i in range(len(data_copy)):
        if data_copy[i] == "" or data_copy[i] == "\n":
            data_copy[i] = "$"
    
    with mopen(resource_path("data.txt"), 'w') as f:
        for line in data_copy:
            try:
                if line[-1] != "\n":
                    f.write(line + '\n')
                else:
                    f.write(line)
            except:
                f.write(line)

def run_edit_window(shared_data, refresh_queue):###多线程执行原edit.exe/edit.py窗口
    pygame.init()##初始化pygame程序（别删）
    screen = pygame.display.set_mode((540, 340))##设置screen大小（540*340，单位像素【初始版本为540*307】）
    pygame.display.set_caption("火车票根生成器-编辑系统  <修改版>   v" + bbh)##编辑系统标题
    tick = pygame.time.Clock()##帧率限制器（勿删）
    
    if "导入字体":
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17)##读取 ttf/simw.ttf 字体，以17字号加载至字体库第0号
        dlc.fontupload(resource_path("ttf/simw.ttf"), 14, 1)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17, 2)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 24, 3)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17, 4)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 13, 5)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17, 10)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17, 12)
        dlc.fontupload(resource_path("ttf/simw.ttf"), 17, 15)
    
    
    dengji = ["G","D","C","S","Z","K","T","L","Y"]
    
    page = "FW"
    flips = 0
    tmd_ztcsjm = -40
    tmd_ztcsjm_zf = 2
    sfxx_pmks3 = ["",""]
    sfxx_pmks6 = ["",""]
    user_input_num = ""
    paste_need = ""
    pst_time = 0  #粘贴时间
    npt = 0
    paste = ""
    excepts_count = 0
    cfz_pmks6 = ""
    ddz_pmks6 = ""
    list_num_ci = []
    
    ##快速选择的站点列表
    stns = [["上海","上海西","上海虹桥","上海南","上海松江","金山北","安亭北","安亭西","","",""],
            ["北京","北京西","北京南","北京北","北京东","北京朝阳","八达岭","大兴机场","","",""],
            ["广州","广州东","广州南","广州北","广州西","广州白云","","乌鲁木齐",""],
            ["深圳","深圳东","深圳西","深圳北","深圳机场","深圳机场北","","西宁",""],
            ["东莞","东莞西","东莞东","东莞南","","","莆田","涵江","","",""],
            ["杭州","杭州东","杭州南","杭州西","","","徐州","徐州东","","",""],
            ["重庆","重庆东","重庆南","重庆北","","","南通","南通西","","",""],
            ["兰州","兰州西","兰州东","兰州新区","","","无锡","无锡东","","",""],
            ["成都","成都东","成都南","成都西","","","合肥","合肥南","","",""],
            ["长春","长春西","长春南","","","天津","天津南","天津西","","",""],
            ["苏州","苏州北","苏州南","","","南京","南京南","拉萨","","",""],
            ["金华","金华南","","上饶","","郑州","郑州东","郑州西","","",""]]
    
    ###<1>至<\1>处为ai生成的代码，用于同步数据，作者看不懂，慎动
    def get_data(index, default=""):
        try:
            val = shared_data[index]
            return val if val is not None else default
        except:
            return default
    
    def set_data(index, value):
        while len(shared_data) <= index:
            shared_data.append("")
        shared_data[index] = value
        refresh_queue.put('data_updated')
    
    def get_fcsj_lst():
        try:
            return get_data(22, "2025/10/01/00/00").split("/")
        except:
            return ["2025","10","01","00","00"]
    ###<\1>
    running = True
    while running:
        try:
            flips += 1.5

            ###首页<点击任意处开始>控件呼吸效果
            tmd_ztcsjm += tmd_ztcsjm_zf
            if tmd_ztcsjm > 220 or tmd_ztcsjm < 40 and flips >= 125:##在40透明和125透明之间来回
                tmd_ztcsjm_zf *= -1   ##是渐显还是渐隐
            
            screen.fill((255,255,255))
            
            try:##读取 picts/base{num}.png 并渲染（底纹随存档调整而调整）
                base_pic_type = get_data(54, '0')
                if base_pic_type != '0' and base_pic_type != '0\n':
                    if base_pic_type == '3' and page != "M3":
                        base_img = pygame.image.load(resource_path(f"picts/base{1}.png"))
                    else:
                        base_img = pygame.image.load(resource_path(f"picts/base{base_pic_type}.png"))
                    screen.blit(base_img, (0, 0))
            except:##读取不到？底纹空白
                pass
            ##原作者版权标（加密）
            dlc.moutput(screen,"#p23 70 32 33 20 36 33 20 33 30 20 33 33 20 33 35 20 33 30 20 33 32 20 33 38 20 33 31 20 33 39 20 33 32 20 34 32 20 37 41 44 39 20 33 43 20 32 44 20 38 32 42 31 20 39 36 45 38 20 36 38 35 30 20 32 44 20 33 45 20 35 32 33 36 20 34 46 35 43 20 32 30 20 32 30 20 35 31 34 44 20 38 44 33 39 20 35 46 30 30 20 36 45 39 30 20 32 30 20 32 30 20 38 42 46 37 20 35 32 46 46 20 35 30 31 32 20 35 33 35 36 23#",(100,100,100),(270-305//2,310))
            #存读档按钮
            dlc.moutput(screen,"#c000235178存档  #R读档",(100,100,100),(440,10))
            #分割线
            pygame.draw.rect(screen,(0,128,168),(0,35,550,2))

            ##首页
            if page == "FW":
                dlc.moutput(screen,"#H编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                
                dlc.moutput(screen,"#B欢迎使用#R中国铁路#B火车票模拟生成系统",(100,100,100),((270-dlc.mlength("欢迎使用#R中国铁路火车票模拟生成系统",num=3)//2),70),num=3)
                # 错误提示区域
                error_message = ""  # 这里可以存储错误信息
                if error_message:
                    dlc.moutput(screen,"#R" + error_message,(255,0,0),((270-dlc.mlength(error_message,num=1)//2),95),num=1)
                dlc.moutput(screen,"#D中国铁路在2025年10月1日全面取消纸质车票",(100,100,100),((270-dlc.mlength("中国铁路在2025年10月1日全面取消纸质车票",num=0)//2),115),num=0,tm=min(flips-250,255))
                dlc.moutput(screen,"#Z于此而来的是伴随我们多年的纸质车票的消逝",(100,100,100),((270-dlc.mlength("于此而来的是伴随我们多年的纸质车票的消逝",num=0)//2),135),num=0,tm=min(flips-450,255))
                dlc.moutput(screen,"#D一张小小的车票，承载着多年的旅途记忆",(100,100,100),((270-dlc.mlength("一张小小的车票，承载着多年的旅途记忆",num=0)//2),155),num=0,tm=min(flips-650,255))
                dlc.moutput(screen,"#Z为了纪念以往的车票，使其在数字世界继续焕发生机",(100,100,100),((270-dlc.mlength("为了纪念以往的车票，使其在数字世界继续焕发生机",num=0)//2),175),num=0,tm=min(flips-850,255))
                dlc.moutput(screen,"#O<中国铁路火车票模拟生成系统>###诞生了",(100,100,100),((270-dlc.mlength("<中国铁路火车票模拟生成系统>诞生了",num=0)//2),195),num=0,tm=min(flips-1050,255))
                dlc.moutput(screen,"#R点按任意位置进入系统",(100,100,100),((270-dlc.mlength("点按任意位置进入系统",num=0)//2),240),num=0,tm=tmd_ztcsjm)
            
            ##<编辑车次>页
            elif page == "M1":
                data10 = get_data(10)
                if len(data10) == 3 and "\n" in data10:
                    set_data(10, data10[0] + "  " + data10[1])
                ##若出发站（↑）、到达站（↓）为2个字，则为他们添加中间的空格隔开。
                data18 = get_data(18)
                if len(data18) == 3 and "\n" in data18:
                    set_data(18, data18[0] + "  " + data18[1])
                ##第一页亮起
                dlc.moutput(screen,"#B编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                ##显示定点编辑按钮
                dlc.moutput(screen,"#R车票编号#x100#R"+get_data(4),(100,100,100),(10,40))
                dlc.moutput(screen,"#Z检票口#x100###"+get_data(7),(100,100,100),(10,60))
                dlc.moutput(screen,"#P出发站#x100###"+get_data(10),(100,100,100),(10,80))
                if get_data(10)[0:3] == "#10":
                    dlc.moutput(screen,"#O站名花体显示[#G√#O]",(100,100,100),(310,80))
                else:
                    dlc.moutput(screen,"#H站名花体显示[    ]",(100,100,100),(310,80))
                dlc.moutput(screen,"#Z终点站#x100###"+get_data(18),(100,100,100),(10,100))
                dlc.moutput(screen,"#P车次#x100###"+get_data(15),(100,100,100),(10,120))
                dlc.moutput(screen,"#Z出发时间#x100###"+get_data(22),(100,100,100),(10,140))
                dlc.moutput(screen,"#P票价#x100###"+get_data(27),(100,100,100),(10,160))
                dlc.moutput(screen,"#Z座位#x100###"+get_data(25),(100,100,100),(10,180))
                data30 = get_data(30)
                if data30 == "" or data30 == "None":
                    dlc.moutput(screen,"#P车票类型#x100###"+"#D无",(100,100,100),(10,200))
                else:
                    dlc.moutput(screen,"#P车票类型#x100###"+data30,(100,100,100),(10,200))
                dlc.moutput(screen,"#Z席别#x100###"+get_data(33),(100,100,100),(10,220))
            
            ## 选择车站类通用展示（实际输入根据page不同而不同）
            elif page in ["S1", "S2", "SZ", "TP"]:
                dlc.moutput(screen,"#D编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                dlc.moutput(screen,"#Z提供部分站点可以选择，若无，可按CTRL+V读取剪切板",(100,100,100),((540-dlc.mlength("提供部分站点可以选择，若无，可按CTRL+V读取剪切板",num=0))//2,40))
                for i in range(len(stns)):
                    for j in range(len(stns[i])):
                        dlc.moutput(screen,"#P"+stns[i][j],(100,100,100),(10+63*j,60+20*i),num=1)
            ##设置左上角编号
            elif page == "BH":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                dlc.moutput(screen,"#Z车票编号#x100#O<#R"+get_data(4)+"#O>",(100,100,100),(10,40))
                for i in range(10):
                    dlc.moutput(screen,str(i),(240,140,60),(50+30*i,80),num=0)
                dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
                for i in range(15):
                    dlc.moutput(screen,chr(65+i),(180,60,220),(50+30*i,120),num=0)
                for i in range(11):
                    dlc.moutput(screen,chr(80+i),(180,60,220),(50+30*i,150),num=0)
                dlc.moutput(screen,"#R<清除>",(240,140,60),(400,150),num=0)
            
            ##检票口信息（可以点击输入，也可以直接在tkinter输入后点击粘贴）
            elif page == "CI":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))

                dlc.moutput(screen,"#L检票口#x100#O<#R"+get_data(7)+"#O>#x370#1点此粘贴插入自定义检票口",(100,100,100),(10,40))
                for i in range(10):
                    dlc.moutput(screen,str(i),(240,140,60),(50+30*i,80),num=0)
                dlc.moutput(screen,"A#x380B",(240,140,60),(350,80),num=0)
                dlc.moutput(screen,"#R<清除>#x480<退格>",(240,140,60),(420,80),num=0)
                dlc.moutput(screen,"一#x100二#x150三#x200楼#x250候车室#x350检票口",(40,140,180),(50,120),num=0)
                ########这里的都是显示效果，真正起效得往下翻，到响应那里同步更改
                ########很重要，很重要，很重要（要不然就是空有按钮没有效果）
                dlc.moutput(screen,"<点>#x080<空格>#x150东#x200南#x250西#x300北#x350广场#x400进站",(40,140,180),(30,160),num=0)
            
            ##设置车次信息（就是C3859、T11、1461等）
            elif page == "CC":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                dlc.moutput(screen,"#Z车次#x100#O<#R"+get_data(15)+"#O>",(100,100,100),(10,40))
                for i in range(10):
                    dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
                dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
                for i in range(9):
                    dlc.moutput(screen,"#L"+dengji[i],(240,140,60),(50+30*i,120),num=0)
                dlc.moutput(screen,"#R<清除>",(240,140,60),(400,120),num=0)
            
            #时间（早期版本在edit.py里面密密麻麻的设置按钮，现在改成调整按钮了<要不然2078年一过就不管用了>|那些列表我也不知道还在哪里有用，删了如果不影响运行，就删了吧）
            elif page == 'TI':
                fcsj_lst = get_fcsj_lst()
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))

                dlc.moutput(screen,"#Z发车时间#x100#O<#R"+get_data(22)+"#O>",(100,100,100),(10,40))
                dlc.moutput(screen,"#R"+fcsj_lst[0]+"#x103←←#x163←#x310→#x360→→",(100,100,100),(210,90),num=1)
                dlc.moutput(screen,"#Z"+fcsj_lst[1]+"#x120←#x360→",(100,100,100),(210,130),num=1)
                dlc.moutput(screen,"#R"+fcsj_lst[2]+"#x103←←#x163←#x310→#x360→→",(100,100,100),(210,170),num=1)
                dlc.moutput(screen,"#Z"+fcsj_lst[3]+"#x120←#x360→",(100,100,100),(210,210),num=1)
                dlc.moutput(screen,"#R"+fcsj_lst[4]+"#x103←←#x163←#x310→#x360→→",(100,100,100),(210,250),num=1)
            
            ##票价
            elif page == "JG":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                dlc.moutput(screen,"#Z票价#x100#O<#R"+get_data(27)+"#O>",(100,100,100),(10,40))
                for i in range(10):
                    dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
                dlc.moutput(screen,"#L<小数点>#x440#R<退格>",(240,140,60),(350,80),num=0)
            
            ##座位号（如3车004号、18车001号下铺、15车12A等）
            elif page == "ST":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,"#Z座位#x100#O<#R"+get_data(25)+"#O>",(100,100,100),(10,40))
                for i in range(10):
                    dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
                dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
                dlc.moutput(screen,"#Z加 #x100车 #x150号 #x200无座 #x250上铺 #x300中铺 #x350下铺",(240,140,60),(50,110),num=0)
                dlc.moutput(screen,"#DA #x100B #x150C #x200D #x250F #x300 #x350#R<清空>",(240,140,60),(50,140),num=0)
            
            #类别（孩学惠网微支等）（不继续更了）
            elif page == "LB":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,"#Z类别#x100#O<#R"+get_data(30)+"#O>",(100,100,100),(10,40))
                dlc.moutput(screen,"#Z<空> #x100学 #x150孩 #x200惠 #x250网 #x300微 #x350#R<退格>",(240,140,60),(50,80),num=0)
            
            #席别（一等座、二等座）
            elif page == "XB":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,"#Z席别#x100#O<#R"+get_data(33)+"#O>",(100,100,100),(10,40))
                dlc.moutput(screen,"#Z一等 #x100二等 #x150特等 #x200商务 #x250优选 #x300座 #x350#R<退格>",(240,140,60),(50,80),num=0)
                dlc.moutput(screen,"#D软 #x100硬 #x150卧 #x200动 #x250高级 #x300新 #x350空调 #x400无 #x450代",(240,140,60),(50,110),num=0)
            
            ##第2页
            elif page == "M2":
                dlc.moutput(screen,"#H编辑车次  #B编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                data36 = get_data(36)
                if "#" in data36:
                    ###通票制作功能其实可以做了，但是废弃了
                    ##因为展示系统(原main.py/main.exe的字体库与编辑系统不同，顾这里不做展示)
                    dlc.moutput(screen,"#P第一行信息#x100#B<通票>",(100,100,100),(10,40))
                else:
                    ###没有通票的话就正常展示了
                    dlc.moutput(screen,"#P第一行信息#x100###"+data36,(100,100,100),(10,40))
                dlc.moutput(screen,"#Z第二行信息#x100###"+get_data(39),(100,100,100),(10,60))
                dlc.moutput(screen,"#P身份信息$$#x100###"+get_data(42),(100,100,100),(10,80))
                dlc.moutput(screen,"#Z提示框上行#x100###"+get_data(46),(100,100,100),(10,100))
                dlc.moutput(screen,"#P提示框下行#x100###"+get_data(47),(100,100,100),(10,120))
                dlc.moutput(screen,"#Z提示框底部#x100###"+get_data(50),(100,100,100),(10,140))
            
            ##第3页
            elif page == "M3":
                dlc.moutput(screen,"#H编辑车次  #H编辑票面  #B其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                data54 = get_data(54, "1")
                if data54=="1"or data54=="1\n":
                    dlc.moutput(screen,"#P启用背景#x200#B<蓝票>#x300#H<红票>#x400#H<橙票>",(100,100,100),(10,40))
                elif data54=="2"or data54=="2\n":
                    dlc.moutput(screen,"#P启用背景#x200#H<蓝票>#x300#R<红票>#x400#H<橙票>",(100,100,100),(10,40))
                elif data54=="3"or data54=="3\n":
                    dlc.moutput(screen,"#L启用背景#x200#H<蓝票>#x300#H<红票>#x400#W<橙票>",(100,100,100),(10,40))
                else:
                    dlc.moutput(screen,"#P启用背景#x200#H<蓝票>#x300#H<红票>#x400#H<橙票>",(100,100,100),(10,40))
                if data54!="3" and data54!="3\n":##对第3个底纹这里做了颜色更改（否则看不清）（上面的懒得做）
                    data56 = get_data(56, "0")
                    if data56=="1"or data56=="1\n":
                        dlc.moutput(screen,"#Z启用QR码#x200#B[#x215√#x240]",(100,100,100),(10,60))
                    else:
                        dlc.moutput(screen,"#Z启用QR码#x200###[#x240]",(100,100,100),(10,60))
                    data58 = get_data(58, "0")
                    if data58=="1"or data58=="1\n":
                        dlc.moutput(screen,"#P旅游计次票模式#x200#B[#x215√#x240]",(100,100,100),(10,80))
                    else:
                        dlc.moutput(screen,"#P旅游计次票模式#x200###[#x240]",(100,100,100),(10,80))
                    dlc.moutput(screen,"#Z设置分辨率#x200#B>>>",(100,100,100),(10,100))
                    dlc.moutput(screen,"#P修复data.txt#x200#B",(100,100,100),(10,120))
                    dlc.moutput(screen,"#R",(100,100,100),(10,180),num=1)
                else:
                    data56 = get_data(56, "0")
                    if data56=="1"or data56=="1\n":
                        dlc.moutput(screen,"#C启用QR码#x200#B[#x215√#x240]",(100,100,100),(10,60))
                    else:
                        dlc.moutput(screen,"#C启用QR码#x200#W[#x240]",(100,100,100),(10,60))
                    data58 = get_data(58, "0")
                    if data58=="1"or data58=="1\n":
                        dlc.moutput(screen,"#L旅游计次票模式#x200#B[#x215√#x240]",(100,100,100),(10,80))
                    else:
                        dlc.moutput(screen,"#L旅游计次票模式#x200#W[#x240]",(100,100,100),(10,80))
                    dlc.moutput(screen,"#C设置分辨率#x200#B>>>",(100,100,100),(10,100))
                    dlc.moutput(screen,"#L修复data.txt#x200#B",(100,100,100),(10,120))
                    dlc.moutput(screen,"#B",(100,100,100),(10,180),num=1)
            ##感谢
            elif page == "GFMF":
                dlc.moutput(screen,"#H编辑车次  #H编辑票面  #B其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,f"感谢 @DX吴某人 提供的字体文件#n感谢 @-花雨桐- 提供源代码#n感谢 @Kumano1018 和 #H已经无法访问的维基百科#c090020180 提供的底纹图片#n#B和各火车迷默默的支持#n#Z版本：{bbh}#n#Y",(90,20,180),(10,40))
            
            elif page == "PM-KS12":#第一，第二行信息设置
                dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                if "#"in get_data(36):
                    dlc.moutput(screen,"#P第一行信息#x100#B<通票>",(100,100,100),(10,40))
                    dlc.moutput(screen,"#Z第二行信息#x100###"+get_data(39),(100,100,100),(10,60))
                else:
                    dlc.moutput(screen,"#P第一行信息#x100###"+get_data(36),(100,100,100),(10,40))
                    dlc.moutput(screen,"#Z第二行信息#x100###"+get_data(39),(100,100,100),(10,60))
                dlc.moutput(screen,"#O点按#R上方#O对应内容粘贴#P自定义内容#O，下方是部分预设（#D联系作者可加#O）",(100,100,100),(270-(dlc.mlength("点按上方对应内容粘贴自定义内容，下方是部分预设（联系作者可加）",num=1))//2,80),num=1)
                dlc.moutput(screen,"#O<报销凭证格式> #x200<原版车票格式> #x350<通票签证格式>",(100,100,100),(50,100))
                dlc.moutput(screen,"#D<始发改签> #x150#L<退票费> #x250<改签费> #x350#H<自定义通票>",(100,100,100),(50,120))
                dlc.moutput(screen,"#H<预留> #x200<预留> #x350<预留>",(100,100,100),(50,140))
            elif page == "PM-KS3":#身份信息设定
                dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                
                dlc.moutput(screen,"#P身份证号#x100###"+sfxx_pmks3[0],(100,100,100),(10,40))
                dlc.moutput(screen,"#P姓名#x100###"+sfxx_pmks3[1],(100,100,100),(10,60))
                dlc.moutput(screen,"#O输入#R姓名#O请点击姓名#P所在行#O。#5#y+=002#c240100010正版程序中，断网可正常使用本功能。",(100,100,100),(270-(dlc.mlength("输入姓名请点击姓名所在行。#5正版程序中，断网可正常使用本功能。",num=1))//2,80),num=1)
                for i in range(10):
                    dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,110),num=0)
                dlc.moutput(screen,"#ZX",(240,140,60),(400,110),num=0)
                dlc.moutput(screen,"#R<退格>#x250#c032160064<键入并退出>",(240,140,60),(150,140),num=0)
            elif page == "PM-KN":##方框内部第一第二行信息显示（民间版可以加一个国铁纪念票版式了）
                dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,"#P第一行信息#x100###"+get_data(46),(100,100,100),(10,40))
                dlc.moutput(screen,"#Z第二行信息#x100###"+get_data(47),(100,100,100),(10,60))
                dlc.moutput(screen,"#O点按#R上方#O对应内容粘贴#P自定义内容#O，下方是部分预设（#D联系作者可加#O）",(100,100,100),(270-(dlc.mlength("点按上方对应内容粘贴自定义内容，下方是部分预设（联系作者可加）",num=1))//2,80),num=1)
                dlc.moutput(screen,"#O<标准> #x150<国庆> #x250<报销> #x350#H<预留>",(100,100,100),(50,100))
                dlc.moutput(screen,"#H<预留> #x150<预留> #x250<预留> #x350<预留>",(100,100,100),(50,120))
            elif page == "PM-KD":##方框底下文字设置（老板新版都可以设置）
                dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                
                dlc.moutput(screen,"#P票据编码#x100###"+sfxx_pmks6[0],(100,100,100),(10,40))
                dlc.moutput(screen,"#Z发售站点#x100###"+sfxx_pmks6[1],(100,100,100),(10,60))
                for i in range(10):
                    dlc.moutput(screen,"#B"+str(i),(240,140,60),(50+30*i,90),num=0)
                dlc.moutput(screen,f"#l<身份证购票>",(100,100,60),(400,90),num=0)
                cfz_pmks6=get_data(10)##出发站
                ddz_pmks6=get_data(18)##到达站
                if "#12" in cfz_pmks6:
                    cfz_pmks6=cfz_pmks6[3:]
                if "  " in cfz_pmks6:
                    cfz_pmks6=cfz_pmks6[0]+cfz_pmks6[3]
                if "  " in ddz_pmks6:
                    ddz_pmks6=ddz_pmks6[0]+ddz_pmks6[3]
                dlc.moutput(screen,f"#R<退格>#x250####O<{cfz_pmks6}>#x400<{ddz_pmks6}>",(100,100,60),(100,115),num=0)##可以自动填充出发站、到达站的信息或自己选择、输入
                dlc.moutput(screen,f"#c010160080<写入并关闭>",(100,100,60),(250,140),num=0)
            
            ##选择发售站（方框底信息）
            elif page == "SZ":
                dlc.moutput(screen,"#D编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,"#Z发售站选择",(100,100,100),(10,40))
                for i in range(len(stns)):
                    for j in range(len(stns[i])):
                        dlc.moutput(screen,"#P"+stns[i][j],(100,100,100),(10+63*j,60+20*i),num=1)
            ##分辨率调试
            elif page == "fbl":
                dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
                pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
                dlc.moutput(screen,f"#Z分辨率#x100#H约#O<#R{str(int(540*float(get_data(64))))}*{str(int(340*float(get_data(64))))}#O>  #H（{get_data(64)}倍）",(100,100,100),(10,40))
                dlc.moutput(screen,"#B适配 #x090#Z 540*340 #x215 1296*816 #x340 1890*1190",(240,140,60),(10,80),num=0)
                dlc.moutput(screen,"#B更大 #x090#Z 2268*1428(2K) #x215 3132*1972(4K) #x340 0*0(自定义)",(240,140,60),(10,110),num=0)
                dlc.moutput(screen,"#B自定 #x090#R1#x1102#x1303#x1504#x1705#x1906#x2107#x2308#x2509#x2700#x290.",(240,140,60),(10,140),num=0)
            
            ################################################这里下面才是响应部分！！上面改完别忘了改下面


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:##右键（黏贴部分操作）
                        paste_content = get_data(66, "")
                        if paste_need and paste_content:
                            if paste_need == "检票口输入":
                                set_data(7, paste_content)
                                dlc.addts("已替换<检票口>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "出发站":
                                set_data(10, paste_content + "\n")
                                return0 = lazy_pinyin(paste_content)
                                return1 = "".join(return0)
                                return1 = return1[0].upper() + return1[1:]
                                set_data(12, return1)
                                dlc.addts("已替换<出发站>信息",color=(10,10,20))
                                paste_need = ""
                                page = "M1"
                            elif paste_need == "到达站":
                                set_data(18, paste_content + "\n")
                                return0 = lazy_pinyin(paste_content)
                                return1 = "".join(return0)
                                return1 = return1[0].upper() + return1[1:]
                                set_data(20, return1)
                                dlc.addts("已替换<到达站>信息",color=(10,10,20))
                                paste_need = ""
                                page = "M1"
                            elif paste_need == "外第一行":
                                set_data(36, paste_content)
                                dlc.addts("已替换<提示第一行>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "外第二行":
                                set_data(39, paste_content)
                                dlc.addts("已替换<提示第二行>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "姓名":
                                sfxx_pmks3[1] = paste_content
                                dlc.addts("已替换<姓名>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "内第一行":
                                set_data(46, paste_content)
                                dlc.addts("已替换<框内第一行>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "内第二行":
                                set_data(47, paste_content)
                                dlc.addts("已替换<框内第二行>信息",color=(10,10,20))
                                paste_need = ""
                            elif paste_need == "发售站":
                                sfxx_pmks6[1] = paste_content + " 售"
                                dlc.addts("已替换<发售站>信息",color=(10,10,20))
                                paste_need = ""
                                page = "PM-KD"
                    elif event.button == 1:##左键
                        pos = event.pos##获取鼠标所在坐标
                        
                        #通用存读档
                        if 490 < pos[0] < 540 and 10 < pos[1] < 40:
                            load_data(shared_data)
                            dlc.addts("已加载数据",color=(10,10,20))
                        elif 440 < pos[0] < 490 and 10 < pos[1] < 40:
                            save_data(shared_data)
                            dlc.addts("已保存数据",color=(10,10,20))##发出一条提示信息
                        


                        ######针对页面的点击判定
                        elif page == "FW":
                            page = "M1"
                        
                        elif page == "M1":
                            if 10 < pos[1] < 40 and 90 < pos[0] < 170:
                                page = "M2"
                                #####跳转至<M2>页（主页第二页）
                            elif 10 < pos[1] < 40 and 170 < pos[0] < 250:
                                page = "M3"
                            elif 40 < pos[1] < 60:
                                page = "BH"
                            elif 60 < pos[1] < 80:
                                page = "CI"
                            elif 80 < pos[1] < 100 and 0 < pos[0] < 300:
                                page = "S1"
                            elif 80 < pos[1] < 100 and 300 < pos[0] < 550:
                                data10 = get_data(10)
                                if data10[0:3] == "#10":
                                    set_data(10, data10[3:])
                                    ##取消出发站的#10前缀
                                    ##注意：这里#10的标记是提示展示系统站名需要更换至华文新魏字体（老红票版式）
                                else:
                                    set_data(10, "#10" + data10)##添加出发站的#10前缀
                            elif 100 < pos[1] < 120:
                                page = "S2"
                            elif 120 < pos[1] < 140:
                                page = "CC"
                            elif 140 < pos[1] < 160:
                                page = "TI"
                            elif 160 < pos[1] < 180:
                                page = "JG"
                            elif 180 < pos[1] < 200:
                                page = "ST"
                            elif 200 < pos[1] < 220:
                                page = "LB"
                            elif 220 < pos[1] < 240:
                                page = "XB"
                        
                        elif page == "S1": 
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 40 < pos[1] < 60:
                                paste_need = "出发站"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif pos[1] > 60:
                                x = (pos[1] - 60) // 20
                                y = (pos[0] - 10) // 63
                                if 0 <= x < 11 and 0 <= y < 11:
                                    set_data(10, stns[x][y] + "\n")
                                    ##利用站点列表数据将点击位置转换成站点名称，存储在第11行（出发站）
                                    return0 = lazy_pinyin(stns[x][y])
                                    ##自动转化成拼音并保存（可以手动在文txt里改）
                                    return1 = "".join(return0)
                                    return1 = return1[0].upper() + return1[1:]
                                    set_data(12, return1)
                                    dlc.addts("已输入<出发站>信息",color=(10,10,20))
                                    page = "M1"
                                    ##自动返回
                        ##这里和上面大差不差，只是存储位置变成19行（到达站）
                        elif page == "S2":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 40 < pos[1] < 60:
                                paste_need = "到达站"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif pos[1] > 60:
                                x = (pos[1] - 60) // 20
                                y = (pos[0] - 10) // 63
                                if 0 <= x < 11 and 0 <= y < 11:
                                    set_data(18, stns[x][y] + "\n")
                                    return0 = lazy_pinyin(stns[x][y])
                                    return1 = "".join(return0)
                                    return1 = return1[0].upper() + return1[1:]
                                    set_data(20, return1)
                                    dlc.addts("已输入<到达站>信息",color=(10,10,20))
                                    page = "M1"
                        
                        elif page == "BH":
                            if 10 < pos[1] < 40:
                                if len(get_data(4)) >= 7:
                                    page = "M1"
                                    sfxx_pmks6 = [get_data(50)[:14], get_data(50)[23:]]
                                    set_data(50, sfxx_pmks6[0] + get_data(4)[-7:] + "  " + sfxx_pmks6[1])
                                    set_data(50, get_data(50).replace("\n", ""))
                                else:
                                    dlc.addts("数据不合法，请直接修改\"data.txt\"",color=(240,100,20))
                            elif 70 <= pos[1] <= 100 and 0 < pos[0] < 400:
                                x = (pos[0] - 50) // 30
                                if len(get_data(4)) < 10:
                                    set_data(4, get_data(4) + str(x))
                            elif 70 <= pos[1] <= 100 and pos[0] > 400:
                                if get_data(4) != "":
                                    set_data(4, get_data(4)[:-1])
                            elif 100 <= pos[1] <= 140:
                                x = (pos[0] - 50) // 30
                                if 0 <= x < 15:
                                    if len(get_data(4)) < 10:
                                        set_data(4, get_data(4) + chr(65 + x))
                            elif 140 <= pos[1] <= 180:
                                x = (pos[0] - 50) // 30
                                if 0 <= x < 11:
                                    if len(get_data(4)) < 10:
                                        set_data(4, get_data(4) + chr(80 + x))
                                else:
                                    set_data(4, "")
                        
                        elif page == "CI":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 40 < pos[1] < 60:
                                paste_need = "检票口输入"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 70 <= pos[1] <= 120 and 50 < pos[0] < 350:
                                x = (pos[0] - 50) // 30
                                set_data(7, get_data(7) + str(x))
                            elif 70 <= pos[1] <= 120 and 410 > pos[0] > 350:
                                set_data(7, get_data(7) + chr(65 + (pos[0] - 350) // 30))
                            elif 70 <= pos[1] <= 120 and 470 > pos[0] > 420:
                                set_data(7, "")
                            elif 70 <= pos[1] <= 120 and 600 > pos[0] > 470:
                                if get_data(7) != "":
                                    set_data(7, get_data(7)[:-1])
                            elif 120 <= pos[1] <= 160 and 600 > pos[0] > 50:
                                if 100 > pos[0] > 50:
                                    set_data(7, get_data(7) + "一")
                                elif 150 > pos[0] > 100:
                                    set_data(7, get_data(7) + "二")
                                elif 200 > pos[0] > 150:
                                    set_data(7, get_data(7) + "三")
                                elif 250 > pos[0] > 200:
                                    set_data(7, get_data(7) + "楼")
                                elif 350 > pos[0] > 250:
                                    set_data(7, get_data(7) + "候车室")
                                elif 450 > pos[0] > 350:
                                    set_data(7, get_data(7) + "检票口")
                            elif 160 <= pos[1] <= 200 and 600 > pos[0] > 30:
                                if 80 > pos[0] > 30:
                                    set_data(7, get_data(7) + ".")
                                elif 150 > pos[0] > 80:
                                    set_data(7, get_data(7) + " ")
                                elif 200 > pos[0] > 150:
                                    set_data(7, get_data(7) + "东")
                                elif 250 > pos[0] > 200:
                                    set_data(7, get_data(7) + "南")
                                elif 300 > pos[0] > 250:
                                    set_data(7, get_data(7) + "西")
                                elif 350 > pos[0] > 300:
                                    set_data(7, get_data(7) + "北")
                                elif 400 > pos[0] > 350:
                                    set_data(7, get_data(7) + "广场")
                                elif 450 > pos[0] > 400:
                                    set_data(7, get_data(7) + "进站")
                        
                        elif page == "CC":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 70 <= pos[1] <= 100 and 0 < pos[0] < 400:
                                x = (pos[0] - 50) // 30
                                if len(get_data(15)) < 6:
                                    set_data(15, get_data(15) + str(x))
                            elif 70 <= pos[1] <= 100 and pos[0] > 400:
                                if get_data(15) != "":
                                    set_data(15, get_data(15)[:-1])
                            elif 100 <= pos[1] <= 140:
                                x = (pos[0] - 50) // 30
                                if 0 <= x < 9:
                                    set_data(15, dengji[x])
                                else:
                                    set_data(15, "")
                        
                        elif page == "TI":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            else:
                                fcsj_lst = get_fcsj_lst()
                                if 90 < pos[1] < 130:
                                    if 103 < pos[0] < 163:
                                        fcsj_lst[0] = str(int(fcsj_lst[0]) - 10)
                                    elif 163 < pos[0] < 213:
                                        fcsj_lst[0] = str(int(fcsj_lst[0]) - 1)
                                    elif 310 < pos[0] < 360:
                                        fcsj_lst[0] = str(int(fcsj_lst[0]) + 1)
                                    elif 360 < pos[0] < 500:
                                        fcsj_lst[0] = str(int(fcsj_lst[0]) + 10)
                                    set_data(22, fcsj_lst[0] + get_data(22)[4:])
                                elif 130 < pos[1] < 170:
                                    if 103 < pos[0] < 163:
                                        fcsj_lst[1] = sy[sy.index(fcsj_lst[1]) - 1]
                                    elif 360 < pos[0] < 500:
                                        fcsj_lst[1] = sy[sy.index(fcsj_lst[1]) + 1]
                                    set_data(22, get_data(22)[:5] + str(fcsj_lst[1]) + get_data(22)[7:])
                                elif 170 < pos[1] < 210:
                                    if 103 < pos[0] < 163:
                                        fcsj_lst[2] = r[abs(r.index(fcsj_lst[2]) - 10)]
                                    elif 163 < pos[0] < 213:
                                        fcsj_lst[2] = r[r.index(fcsj_lst[2]) - 1]
                                    elif 310 < pos[0] < 360:
                                        fcsj_lst[2] = r[r.index(fcsj_lst[2]) + 1]
                                    elif 360 < pos[0] < 500:
                                        fcsj_lst[2] = r[r.index(fcsj_lst[2]) + 10]
                                    set_data(22, get_data(22)[:8] + str(fcsj_lst[2]) + get_data(22)[10:])
                                elif 210 < pos[1] < 250:
                                    if 103 < pos[0] < 163:
                                        fcsj_lst[3] = sy[sy.index(fcsj_lst[3]) - 1]
                                    elif 360 < pos[0] < 500:
                                        fcsj_lst[3] = sy[sy.index(fcsj_lst[3]) + 1]
                                    set_data(22, get_data(22)[:11] + str(fcsj_lst[3]) + get_data(22)[13:])
                                elif 250 < pos[1] < 300:
                                    if 103 < pos[0] < 163:
                                        fcsj_lst[4] = f[abs(f.index(fcsj_lst[4]) - 10)]
                                    elif 163 < pos[0] < 213:
                                        fcsj_lst[4] = f[f.index(fcsj_lst[4]) - 1]
                                    elif 310 < pos[0] < 360:
                                        fcsj_lst[4] = f[f.index(fcsj_lst[4]) + 1]
                                    elif 360 < pos[0] < 500:
                                        fcsj_lst[4] = f[f.index(fcsj_lst[4]) + 10]
                                    set_data(22, get_data(22)[:14] + str(fcsj_lst[4]))
                        
                        elif page == "JG":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 70 <= pos[1] <= 100 and 0 < pos[0] < 350:
                                x = (pos[0] - 50) // 30
                                if len(get_data(27)) < 6:
                                    set_data(27, get_data(27) + str(x))
                            elif 70 <= pos[1] <= 100 and 440 > pos[0] > 350:
                                if len(get_data(27)) < 6:
                                    set_data(27, get_data(27) + ".")
                            elif 70 <= pos[1] <= 100 and 490 > pos[0] > 440:
                                if len(get_data(27)) > 0:
                                    set_data(27, get_data(27)[:-1])
                        
                        elif page == "ST":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            elif 70 <= pos[1] <= 100 and 0 < pos[0] < 350:
                                x = (pos[0] - 50) // 30
                                if len(get_data(25)) < 12:
                                    set_data(25, get_data(25) + str(x))##这里的0~9通过计算的方式直接写入
                            elif 70 <= pos[1] <= 100 and 450 > pos[0] > 395:
                                if len(get_data(25)) > 0:
                                    set_data(25, get_data(25)[:-1])
                            elif 140 >= pos[1] >= 110 and 50 < pos[0] < 400:
                                cin_temp = ["加","车","号","无座","上铺","中铺","下铺"]##剩下的靠列表
                                x = (pos[0] - 50) // 50
                                if x <= 6 and len(get_data(25)) < 12:
                                    set_data(25, get_data(25) + cin_temp[x])
                            elif 170 >= pos[1] >= 140 and 50 < pos[0] < 300:
                                cin_temp = ["A","B","C","D","F"]
                                x = (pos[0] - 50) // 50
                                if x <= 4 and len(get_data(25)) < 12:
                                    set_data(25, get_data(25) + cin_temp[x])
                            elif 170 >= pos[1] >= 140 and 350 < pos[0] < 400:
                                set_data(25, "")
                        
                        elif page == "LB":
                            if 10 < pos[1] < 40:
                                page = "M1"
                            else:
                                data30 = get_data(30)
                                addxg = 1 if data30 and data30 not in ["", "None", "\n", "None\n"] else 0
                                lb_dyh = ["学","孩","惠","网","微"]
                                if 80 < pos[1] < 109 and 100 < pos[0] < 350:
                                    x = (pos[0] - 100) // 50
                                    if x <= 4 and len(data30) < 7:
                                        if addxg:
                                            set_data(30, data30 + "/" + lb_dyh[x])
                                        else:
                                            set_data(30, lb_dyh[x])
                        elif page=="XB":
                            
                            if 10<pos[1]<40:
                                page="M1"
                            xb_syh=["一等","二等","特等","商务","优选","座"]
                            xb_seh=["软","硬","卧","动","高级","新","空调","无","代"]
                            if 80<pos[1]<109 and 50<pos[0]<350:
                                x=(pos[0]-50)//50       
                                if x<6 and len(get_data(33))<15:
                                    set_data(33,get_data(33)+xb_syh[x])
                                else:
                                    dlc.addts("数据超限",color=(240,100,20))
                            
                            if 80<pos[1]<110 and 350<pos[0]<400 and len(get_data(33))>0:
                                set_data(33,get_data(33)[:-1])
                            if 110<pos[1]<139 and 50<pos[0]<550:
                                x=(pos[0]-50)//50
                                if x<9 and len(get_data(33))<15:
                                    set_data(33,get_data(33)+xb_seh[x])
                                else:
                                    dlc.addts("数据超限",color=(240,100,20))
                        elif page=="M2":
                            if 10<pos[1]<40 and pos[0]<90:
                                page="M1"
                            elif 10<pos[1]<40 and 170<pos[0]<250:
                                page="M3"
                            elif 40<pos[1]<80:
                                page="PM-KS12"
                            elif 80<pos[1]<100:
                                page="PM-KS3"
                                sfxx_pmks3=get_data(42).split("    ")
                            elif 100<pos[1]<140:
                                page="PM-KN"
                            elif 140<pos[1]<160:
                                page="PM-KD"
                                sfxx_pmks6=[get_data(50)[:14],get_data(50)[23:]]
                        
                        elif page == "M3":
                            if 10 < pos[1] < 40 and pos[0] < 90:
                                page = "M1"
                            elif 10 < pos[1] < 40 and 90 < pos[0] < 170:
                                page = "M2"
                            elif 40 < pos[1] < 60:
                                data54 = get_data(54, "1")
                                if data54 == "1":
                                    set_data(54, "2")
                                elif data54 == "2":
                                    set_data(54, "3")
                                elif data54 == "3":
                                    set_data(54, "0")
                                else:
                                    set_data(54, "1")
                            elif 60 < pos[1] < 80:
                                data56 = get_data(56, "0")
                                if data56 == "1":
                                    set_data(56, "0")
                                else:
                                    set_data(56, "1")
                                    dlc.addts("请手动调整qrcode的分辨率",color=(10,10,20))
                            elif 80 < pos[1] < 100:
                                data58 = get_data(58, "0")
                                if data58 == "1":
                                    set_data(58, "0")
                                else:
                                    set_data(58, "1")
                            elif 100 < pos[1] < 120:
                                page = "fbl"
                            elif 120 < pos[1] < 140:
                                xiufudata()
                            elif 180 < pos[1] < 194:
                                page = "GFMF"
                                user_input_num = ""
                        ##感谢页
                        elif page == "GFMF":
                            if 10 < pos[1] < 40 and pos[0] < 90:
                                page = "M1"
                            elif 10 < pos[1] < 40 and 90 < pos[0] < 170:
                                page = "M2"

                        #框上第一第二行    
                        elif page=="PM-KS12":
                            if 0<pos[1]<40 and 0<pos[0]<300:
                                page="M2"
                                paste_need=""
                            elif 40<pos[1]<60:
                                ##申请粘贴信息，粘贴内容为"外第一行"
                                paste_need="外第一行"
                                npt=pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 60<pos[1]<80:
                                paste_need="外第二行"
                                npt=pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 100<pos[1]<120:
                                ##选项
                                if 50<pos[0]<200:
                                    if get_data(39)=="仅供报销使用":
                                        set_data(36, "")
                                        set_data(39, "仅供收藏使用")
                                    else:
                                        set_data(36, "")
                                        set_data(39, "仅供报销使用")
                                elif 200<pos[0]<350:
                                    set_data(36, "限乘当日当次车")
                                    set_data(39, "")
                                elif 350<pos[0]<480:
                                    if get_data(39)!="中转"and 1:
                                        set_data(36, "限乘当日当次车 随原票使用")
                                        set_data(39, "中转")
                                    else:
                                        set_data(36, "限乘当日当次车 随原票使用")
                                        set_data(39, "中转换乘 中转")
                            elif 120<pos[1]<140:
                                if 50<pos[0]<150:
                                    if get_data(36)=="":
                                        if get_data(39)!="仅供收藏使用":
                                            set_data(39, "始发改签 "+get_data(39))
                                        else:
                                            dlc.addts("收藏票不支持",color=(240,100,20))
                                    else:
                                        dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                                elif 150<pos[0]<250:
                                    if get_data(36)=="":
                                        set_data(36, "退票费")
                                        dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                                    elif get_data(39)=="":
                                        set_data(39, "退票费")
                                        dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                                    else:
                                        dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                                elif 250<pos[0]<350:
                                    if get_data(36)=="":
                                        set_data(36, "改签费")
                                        dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                                    elif get_data(39)=="":
                                        set_data(39, "改签费")
                                        dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                                    else:
                                        dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                        #框上第三行
                        elif page == "PM-KS3":
                            if 0 < pos[1] < 40 and 0 < pos[0] < 300:
                                page = "M2"
                            elif 60 < pos[1] < 80:
                                paste_need = "姓名"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 100 < pos[1] < 140:
                                x = (pos[0] - 50) // 30
                                if 0 <= x <= 9 and len(sfxx_pmks3[0]) < 18:
                                    sfxx_pmks3[0] += str(x)
                                elif 0 <= x <= 9 and len(sfxx_pmks3[0]) >= 18:
                                    sfxx_pmks3[0] = str(x)
                                elif len(sfxx_pmks3[0]) == 17 and 450 > pos[0] > 400:
                                    sfxx_pmks3[0] += "X"
                            elif 140 < pos[1] < 170:
                                if 150 < pos[0] < 250:
                                    if len(sfxx_pmks3[0]) > 0:
                                        sfxx_pmks3[0] = sfxx_pmks3[0][:-1]
                                elif 250 < pos[0] < 350:
                                    if len(sfxx_pmks3[0]) <= 17 or sfxx_pmks3[1] == "":
                                        dlc.addts("数据不合法,无法保存",color=(240,100,20))
                                    else:
                                        set_data(42, sfxx_pmks3[0] + '    ' + sfxx_pmks3[1])
                                        page = "M2"
                        
                        ##框内
                        elif page == "PM-KN":
                            if 0 < pos[1] < 40 and 0 < pos[0] < 300:
                                page = "M2"
                            elif 40 < pos[1] < 60:
                                paste_need = "内第一行"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 60 < pos[1] < 80:
                                paste_need = "内第二行"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif 100 < pos[1] < 140:
                                x = (pos[0] - 50) // 100
                                if x == 0:
                                    if get_data(46) != "买票请到12306 发货请到95306":
                                        set_data(46, "买票请到12306 发货请到95306")
                                    else:
                                        set_data(46, "买票请到95306 发货请到12306")
                                    set_data(47, "中国铁路祝您旅途愉快")
                                if x == 1:
                                    set_data(46, "欢度国庆 祝福祖国")
                                    set_data(47, "中国铁路祝您旅途愉快")
                                if x == 2:
                                    if get_data(46) != "报销凭证 遗失不补":
                                        set_data(46, "报销凭证 遗失不补")
                                    else:
                                        set_data(46, "仅供收藏 遗失不补")
                                    set_data(47, "退票改签时须交回车站")
                        #框下（框底）
                        elif page == "PM-KD":
                            if 0 < pos[1] < 40 and 0 < pos[0] < 300:
                                page = "M2"
                            elif 60 < pos[1] < 80:
                                page = "SZ"
                            elif 80 < pos[1] < 114:
                                if pos[0] < 400:
                                    x = (pos[0] - 50) // 30
                                    if 0 <= x <= 9:
                                        if len(sfxx_pmks6[0]) < 14:
                                            sfxx_pmks6[0] += str(x)
                                elif 400 < pos[0] < 500:
                                    if sfxx_pmks6[1] != "J M":
                                        sfxx_pmks6[1] = "J M"
                                    else:
                                        sfxx_pmks6[1] = "H Z"
                            elif 114 < pos[1] < 139:
                                if pos[0] < 250:
                                    if len(sfxx_pmks6[0]) > 0:
                                        sfxx_pmks6[0] = sfxx_pmks6[0][:-1]
                            elif 139 < pos[1] < 169:
                                if len(sfxx_pmks6[0]) != 14:
                                    dlc.addts("数据不合法",color=(240,100,20))
                                else:
                                    set_data(50, sfxx_pmks6[0] + get_data(4)[-7:] + "  " + sfxx_pmks6[1])
                                    set_data(50, get_data(50).replace("\n", ""))
                                    page = "M2"
                        
                        ##发售站选择逻辑
                        elif page == "SZ":
                            if 10 < pos[1] < 40:
                                page = "PM-KD"
                            elif 40 < pos[1] < 60:
                                paste_need = "发售站"
                                npt = pygame.time.get_ticks()
                                dlc.addts("请在Tkinter输入框中输入信息，鼠标右键粘贴",color=(10,10,20))
                            elif pos[1] > 60:
                                x = (pos[1] - 60) // 20
                                y = (pos[0] - 10) // 63
                                if 0 <= x < 11 and 0 <= y < 11:
                                    sfxx_pmks6[1] = stns[x][y] + " 售"
                                    page = "PM-KD"
                        
                        ##改分辨率倍数
                        elif page == "fbl":
                            if 10 < pos[1] < 40 and pos[0] < 90:
                                page = "M1"
                            elif 10 < pos[1] < 40 and 90 < pos[0] < 170:
                                page = "M2"
                            elif 80 < pos[1] < 110:
                                if 90 < pos[0] < 215:
                                    set_data(64, "1.0")
                                    dlc.addts("分辨率设置为 540*307 (1.0倍)",color=(180,10,20))
                                elif 215 < pos[0] < 340:
                                    set_data(64, "2.4")
                                    dlc.addts("分辨率设置为 1296*736 (2.4倍)",color=(180,10,20))
                                elif 340 < pos[0] < 500:
                                    set_data(64, "3.5")
                                    dlc.addts("分辨率设置为 1960*1074 (3.5倍)",color=(180,10,20))
                            elif 110 < pos[1] < 140:
                                if 90 < pos[0] < 215:
                                    set_data(64, "4.2")
                                    dlc.addts("分辨率设置为 2268*1289 (4.2倍)",color=(180,10,20))
                                elif 215 < pos[0] < 340:
                                    set_data(64, "5.8")
                                    dlc.addts("分辨率设置为 3132*1780 (5.8倍)",color=(180,10,20))
                                elif 340 < pos[0] < 500:
                                    set_data(64, "0.0")
                                    dlc.addts("分辨率清空",color=(180,10,20))
                            elif 140 < pos[1] < 170:
                                zzzzzz = (pos[0] - 90) // 20 + 1
                                if 1 <= zzzzzz <= 10:
                                    data64 = get_data(64)
                                    if data64 == "0.0":
                                        set_data(64, str(zzzzzz % 10))
                                    elif float(data64) < 2 or "." in data64:
                                        set_data(64, data64 + str(zzzzzz % 10))
                                if zzzzzz > 10:
                                    data64 = get_data(64)
                                    if data64 == "0.0":
                                        set_data(64, "0")
                                    if "." not in data64:
                                        set_data(64, data64 + ".")
                
                elif event.type == pygame.KEYDOWN:
                    ######这里部分输入支持键盘，并非全部！
                    ##还是一样，判断所属页面和响应事件执行对应逻辑
                    if page == "BH":
                        if pygame.K_0 <= event.key <= pygame.K_9:
                            x = event.key - pygame.K_0
                            if len(get_data(4)) < 10:
                                set_data(4, get_data(4) + str(x))
                        elif event.key == pygame.K_BACKSPACE:
                            if get_data(4) != "":
                                set_data(4, get_data(4)[:-1])
                        elif pygame.K_a <= event.key <= pygame.K_z:
                            x = event.key - pygame.K_a
                            if len(get_data(4)) < 10:
                                set_data(4, get_data(4) + chr(x + 65))
                    elif page == "CI":
                        if pygame.K_0 <= event.key <= pygame.K_9:
                            x = event.key - pygame.K_0
                            if len(get_data(7)) < 10:
                                set_data(7, get_data(7) + str(x))
                        elif event.key == pygame.K_BACKSPACE:
                            if get_data(7) != "":
                                set_data(7, get_data(7)[:-1])
                        elif pygame.K_a <= event.key <= pygame.K_z:
                            x = event.key - pygame.K_a
                            if len(get_data(7)) < 10 and x <= 1:
                                set_data(7, get_data(7) + chr(x + 65))
                            elif x <= 26 and x in [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_PERIOD, pygame.K_SPACE]:
                                input_check_in = ["一", "二", "三", "楼", "检票口", "候车室", ".", " "]
                                list_num_ci = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_PERIOD, pygame.K_SPACE]
                                set_data(7, get_data(7) + input_check_in[list_num_ci.index(event.key)])
                    elif page == "CC":
                        tmp_CC_ZM = [pygame.K_a, pygame.K_c, pygame.K_d, pygame.K_k, pygame.K_t, pygame.K_z, pygame.K_g, pygame.K_s, pygame.K_x, pygame.K_j, pygame.K_l, pygame.K_y]
                        if event.key == pygame.K_BACKSPACE:
                            if get_data(15) != "":
                                set_data(15, get_data(15)[:-1])
                        elif event.unicode.isdigit() or event.unicode.isspace() or event.key in tmp_CC_ZM:
                            if len(get_data(15)) < 7:
                                if event.key in tmp_CC_ZM:
                                    if event.key != pygame.K_j:
                                        set_data(15, chr(event.key - pygame.K_a + 65))
                                    else:
                                        set_data(15, get_data(15) + "J")
                                else:
                                    set_data(15, get_data(15) + event.unicode)
                    elif page == "JG":
                        if pygame.K_0 <= event.key <= pygame.K_9:
                            x = event.key - pygame.K_0
                            if len(get_data(27)) < 10:
                                set_data(27, get_data(27) + str(x))
                        elif event.key == pygame.K_BACKSPACE:
                            if get_data(27) != "":
                                set_data(27, get_data(27)[:-1])
                    elif page == "ST":
                        if event.key == pygame.K_BACKSPACE:
                            if get_data(25) != "":
                                set_data(25, get_data(25)[:-1])
                        elif event.unicode.isdigit() or event.unicode.isspace():
                            set_data(25, get_data(25) + event.unicode)
                        cin_temp = ["加", "车", "号", "无座", "上铺", "中铺", "下铺", "A", "B", "C", "D", "F"]
                        cin_temp_key = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_f]
                        if event.key in cin_temp_key:
                            set_data(25, get_data(25) + cin_temp[cin_temp_key.index(event.key)])
                    elif page == "PM-KS3":
                        if event.key == pygame.K_BACKSPACE:
                            if sfxx_pmks3[0] != "":
                                sfxx_pmks3[0] = sfxx_pmks3[0][:-1]
                        elif event.unicode.isdigit() and len(sfxx_pmks3[0]) < 18:
                            sfxx_pmks3[0] += event.unicode
                    elif page == "PM-KD":
                        if event.key == pygame.K_BACKSPACE:
                            if sfxx_pmks6[0] != "":
                                sfxx_pmks6[0] = sfxx_pmks6[0][:-1]
                        elif event.unicode.isdigit() and len(sfxx_pmks6[0]) < 14:
                            sfxx_pmks6[0] += event.unicode
                        elif pygame.K_a <= event.key <= pygame.K_z:
                            x = event.key - pygame.K_a
                            if len(sfxx_pmks6[0]) < 14:
                                sfxx_pmks6[0] += chr(x + 65)
            
            dlc.outputts(screen, 1)##展示提示（以1号字体）
            pygame.display.flip()##刷新窗口
            tick.tick(53)##每秒53帧（也控制提示文字飘动速度）
            excepts_count = 0
        
        except Exception as e:###出bug了直接跳到主页
            excepts_count += 1
            if excepts_count == 1:
                try:
                    xiufudata()
                    page = "FW"
                except:
                    pass
            if excepts_count >= 10:
                raise e
    
    pygame.quit()
##将整数转化为首位包含0的三位整数型字符串
def str03(int1, type="x+="):
    int2 = int(float(int1))
    if int2 < 10:
        return f"00{int2}"
    elif int2 < 100:
        return f"0{int2}"
    elif int2 < 1000:
        return f"{int2}"
    else:
        ##太大了（不适配2000以上）
        return f"999#{type}{str03(int2-999)}"

def run_display_window(shared_data, refresh_queue):
    pygame.init()
    
    page = "main"
    
    def get_data(index, default=""):
        try:
            val = shared_data[index]
            return val if val is not None else default
        except:
            return default
    
    try:
        fbl_multiply = float(get_data(64, "3.5"))
    except:
        fbl_multiply = 3.5
    
    fbl_y_ratio = 340/307##Y方向拉伸比例（基准分辨率从307改为340）
    
    def fy(y):
        return y/3.5*fbl_multiply*fbl_y_ratio
    
    def fx(x):
        return x/3.5*fbl_multiply
    
    tick = pygame.time.Clock()
    if page == "main":
        screen = pygame.display.set_mode((int(540 * fbl_multiply), int(340 * fbl_multiply)))
    else:
        screen = pygame.display.set_mode((540,340))
        fbl_multiply = 1
    
    pygame.display.set_caption(f"火车票根生成器 展示系统 v{bbh}")
    
    try:
        import win32gui, win32con
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)##窗口强制指定（现在可能没有用了）
    except:
        pass
    
    dlc.fontupload(resource_path("ttf/simhei-rednum.ttf"), int(28 * fbl_multiply), 0)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(74/3.5 * fbl_multiply), 1)
    dlc.fontupload(resource_path("ttf/simhei.ttf"), int(119/3.5 * fbl_multiply), 2)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(46/3.5 * fbl_multiply), 3)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(102/3.5 * fbl_multiply), 4)
    dlc.fontupload(resource_path("ttf/simhei.ttf"), int(91/3.5 * fbl_multiply), 5)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(77/3.5 * fbl_multiply), 6)
    dlc.fontupload(resource_path("ttf/simhei.ttf"), int(70/3.5 * fbl_multiply), 7)
    dlc.fontupload(resource_path("ttf/simhei.ttf"), int(53/3.5 * fbl_multiply), 8)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(70/3.5 * fbl_multiply), 9)
    dlc.fontupload(resource_path("ttf/simw.ttf"), int(112/3.5 * fbl_multiply), 10)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(67/3.5 * fbl_multiply), 11)
    dlc.fontupload(resource_path("ttf/simw.ttf"), int(70/3.5 * fbl_multiply), 12)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(84/3.5 * fbl_multiply), 13)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(25/3.5 * fbl_multiply), 14)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(81/3.5 * fbl_multiply), 15)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(49/3.5 * fbl_multiply), 16)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(63/3.5 * fbl_multiply), 17)
    dlc.fontupload(resource_path("ttf/simw.ttf"), int(53/3.5 * fbl_multiply), 18)
    dlc.fontupload(resource_path("ttf/simsun.ttf"), int(60/3.5 * fbl_multiply), 19)
    
    ten = 0
    j = 0
    
    running = True
    while running:
        try:
            while not refresh_queue.empty():
                refresh_queue.get()
            ##展示图片（无法读取则用白底）
            screen.fill((255, 255, 255))
            
            using_base_pic = int(get_data(54, "1"))
            using_QRcode = int(get_data(56, "0"))
            
            if using_base_pic >= 1:
                try:
                    if fbl_multiply == 1:
                        base_img = pygame.image.load(resource_path(f"picts/base{using_base_pic}.png"))
                    elif fbl_multiply == 2.4:
                        base_img = pygame.image.load(resource_path(f"picts/basea{using_base_pic}.png"))
                    else:
                        base_img = pygame.image.load(resource_path(f"picts/baseb{using_base_pic}.png"))
                    screen.blit(base_img, (0, 0))
                except:
                    pass
            
            if page == "main":
                ##读取数据
                red_code = get_data(4)##车票编码
                enter_gate = get_data(7)##检票口
                sta_stn_chn = get_data(10)##出发站（文字）
                sta_stn_eng = get_data(12)##出发站（拼音）
                tra_num = get_data(15)##车次
                end_stn_chn = get_data(18)##到达站（文字）
                end_stn_eng = get_data(20)##到达站（拼音）
                date_str = get_data(22, "2025/10/01/00/00")##发车时间（默认25年10月1日的0点0分0秒）
                date = date_str.split("/") ##日期列表（后续程序会调用这个）
                seat_str = get_data(25) ##座位号
                seat = seat_str.split("车") if seat_str else [""]##座位号后加工
                money = get_data(27)##钱
                midcode_str = get_data(30)##中间的标记
                midcode = midcode_str.split("/") if midcode_str else [""]##中间的标记后加工
                seatclass = get_data(33)##席别
                tips1 = get_data(36)##提示第一行（PM_KS1）
                tips2 = get_data(39)##提示第二行
                idname = get_data(42)##身份信息（第三行）
                und1 = get_data(46)##框内第一行
                und2 = get_data(47)##框内第二行
                undl = get_data(50)##框下
                lyjcp = int(get_data(58, "0"))##旅游计次票特殊版式
                hbys = get_data(60)##货币样式（可以自定义货币而非仅人民币）
                if hbys and hbys not in ["", "None", "\n", "$"]:
                    hbys = hbys.split("|")
                else:
                    hbys = ""
                if_simsun = get_data(62)
                
                if using_base_pic < 3:
                    dlc.moutput(screen, red_code, (255, 120, 120), (int(fx(111)), int(fy(42))))
                else:
                    dlc.moutput(screen, red_code, (235, 40, 30), (int(fx(111)), int(fy(42))))
                
                if enter_gate == "旅游计次票" or enter_gate == "旅游计次票\n" or lyjcp == 1:
                    dlc.moutput(screen, "旅游计次票", (0, 0, 0),
                               (int(fx(1780) - dlc.mlength("旅游计次票", 17)),
                                int(fy(49))), 255, 17)
                elif enter_gate and enter_gate not in ["$", "\n"]:
                    dlc.moutput(screen, "检票:" + enter_gate, (0, 0, 0),
                               (int(fx(1780) - dlc.mlength("检票:" + enter_gate, 17)),
                                int(fy(49))), 255, 17)
                
                if '#10' in sta_stn_chn and ten == 0:##对于早期华文新魏字体的后处理并输出
                    sta_stn_chn = sta_stn_chn[3:]
                    ten = 1
                else:
                    if ten != 1:
                        ten = 0
                
                if ten:
                    if len(sta_stn_chn) == 2:
                        sta_stn_chn = f"{sta_stn_chn[0]}  {sta_stn_chn[1]}"
                    if len(end_stn_chn) == 2:
                        end_stn_chn = f"{end_stn_chn[0]}  {end_stn_chn[1]}"
                    
                    dlc.moutput(screen, f'#y+={str03(int(fy(11)),"y+=")}' + sta_stn_chn +
                               f'#6#x+={str03(int(fx(35)),"")}#y+={str03(int(fy(14)),"")}站',
                               (0, 0, 0), (int(fx(156)), int(fy(158))), 255, 10)
                    dlc.moutput(screen, f'#y+={str03(int(fy(11)),"y+=")}' + end_stn_chn +
                               f'#6#x+={str03(int(fx(35)),"")}#y+={str03(int(fy(14)),"")}站',
                               (0, 0, 0), (int(fx(1224)), int(fy(158))), 255, 10)
                else:
                    if len(sta_stn_chn) == 2:
                        sta_stn_chn = f"{sta_stn_chn[0]}  {sta_stn_chn[1]}"
                    if len(end_stn_chn) == 2:
                        end_stn_chn = f"{end_stn_chn[0]}  {end_stn_chn[1]}"
                    
                    dlc.moutput(screen, sta_stn_chn + f'#6#x+={str03(int(fx(35)),"x+=")}#y+={str03(int(fy(25)),"")}站',
                               (0, 0, 0), (int(fx(156)), int(fy(158))), 255, 2)
                    dlc.moutput(screen, end_stn_chn + f'#6#x+={str03(int(fx(35)),"x+=")}#y+={str03(int(fy(25)),"")}站',
                               (0, 0, 0), (int(fx(1224)), int(fy(158))), 255, 2)
                ##拼音名称渲染
                dlc.moutput(screen, sta_stn_eng, (0, 0, 0), (int(fx(219)), int(fy(284))), 255, 9)
                dlc.moutput(screen, end_stn_eng, (0, 0, 0), (int(fx(1287)), int(fy(284))), 255, 9)
                ##车次
                dlc.moutput(screen, tra_num, (0, 0, 0), (int(fx(940) - dlc.mlength(tra_num, 4)//2), int(fy(161))), 255, 4)
                ##绘制箭头
                pygame.draw.line(screen, (0, 0, 0), 
                               (int(fx(940) - dlc.mlength("C3895", 4)//2), int(fy(280))),
                               (int(fx(968) + dlc.mlength("C3895", 4)//2), int(fy(280))), int(2 * fbl_multiply))
                pygame.draw.line(screen, (0, 0, 0),
                               (int(fx(968) + dlc.mlength("C3895", 4)//2 - dlc.mlength("5", 4)), int(fy(263))),
                               (int(fx(968) + dlc.mlength("C3895", 4)//2), int(fy(280))), int(2 * fbl_multiply))
                
                if lyjcp == 0:
                    dlc.moutput(screen, date[0] + f"#3#x+={str03(int(fx(18)),'x+=')}#y+={str03(int(fy(25)),'y+=')}年#x+={str03(int(fx(18)),'x+=')}#y-={str03(int(fy(25)),'y-=')}#5" + date[1] + f"#3#x+={str03(int(fx(18)),'x+=')}#y+={str03(int(fy(25)),'y+=')}月#x+={str03(int(fx(18)),'x+=')}#y-={str03(int(fy(25)),'y-=')}#5" + date[2] + f"#3#x+={str03(int(fx(18)),'x+=')}#y+={str03(int(fy(25)),'y+=')}日#x+={str03(int(fx(18)),'x+=')}#y-={str03(int(fy(25)),'y-=')}#5" + date[3] + ":" + date[4] + f"#3#x+={str03(int(fx(18)),'x+=')}#y+={str03(int(fy(25)),'y+=')}开",
                               (0, 0, 0), (int(fx(118)), int(fy(368))), 255, 5)
                    try:
                        if seat[0] and seat[0] not in ["不对号入座", "$"]:
                            if len(seat) > 1 and "号" == seat[1][-1] and j == 0:
                                seat[1] = seat[1][:-1] + f"#3#x+={str03(int(fx(14)),'x+=')}#y+={str03(int(fy(14)),'y+=')}号"
                                j = 1
                            dlc.moutput(screen, f"#y+={str03(int(fy(11)),'y+=')}{seat[0]}#3#x+={str03(int(fx(11)),'x+=')}#y+={str03(int(fy(14)),'y+=')}车#x+={str03(int(fx(11)),'x+=')}#y-={str03(int(fy(14)),'y-=')}#7{seat[1]}",
                                       (0, 0, 0), (int(fx(1238)), int(fy(368))), 255, 7)
                        elif seat[0] == "不对号入座":
                            dlc.moutput(screen, "不对号入座", (0, 0, 0), (int(fx(1238)), int(fy(368))), 255, 11)
                    except:
                        pass
                
                if "判断货币样式并输出":
                    if isinstance(hbys, str):
                        dlc.moutput(screen, f"#x+={str03(int(fx(18)),'x+=')}#y+={str03(int(fy(36)),'y+=')}%一08#y-={str03(int(fy(36)),'y-=')}#x-={str03(int(fx(18)),'x-=')}￥{money}#3#x+={str03(int(fx(11)),'x+=')}#y+={str03(int(fy(25)),'y+=')}元",
                                (0, 0, 0), (int(fx(118)), int(fy(455))), 255, 5)
                    elif isinstance(hbys, list) and hbys[0][0] == "$":
                        dlc.moutput(screen, "$", (0, 0, 0), (int(fx(118)), int(fy(455))), 255, 5)
                        dlc.moutput(screen, f"{money}#3#x+={str03(int(fx(11)),'x+=')}#y+=024{hbys[1]}",
                                (0, 0, 0), (int(fx(188)), int(fy(455))), 255, 5)
                    elif isinstance(hbys, list):
                        dlc.moutput(screen, f"{hbys[0]}{money}#3#x+={str03(int(fx(11)),'x+=')}#y+=024{hbys[1]}",
                                (0, 0, 0), (int(fx(118)), int(fy(455))), 255, 5)
                ##中部标记
                if midcode[0] and midcode[0] not in ["None", ""]:
                    if len(midcode) == 1:
                        midcode_out = f"#零{str03(int(12 * fbl_multiply),'')}" + midcode[0]
                    elif len(midcode) == 2:
                        midcode_out = f"#x-={str03(int(fx(81)),'x-=')}#零{str03(int(12 * fbl_multiply),'')}" + midcode[0] + f"  #x-={str03(int(fx(11)),'x-=')}#零{str03(int(12 * fbl_multiply),'')}" + midcode[1]
                    else:
                        midcode_out = ""
                    dlc.moutput(screen, midcode_out, (0, 0, 0), (int(fx(888)), int(fy(476))), 255, 19)

                ##席别  
                if if_simsun == "1":
                    if lyjcp == 0:
                        dlc.moutput(screen, seatclass, (0, 0, 0), (int(fx(1587) - dlc.mlength(seatclass, 11)), int(fy(455))), 255, 11)
                    else:
                        dlc.moutput(screen, "二等座", (0, 0, 0), (int(fx(1587) - dlc.mlength("二等座", 11)), int(fy(455))), 255, 11)
                else:
                    if lyjcp == 0:
                        dlc.moutput(screen, seatclass, (0, 0, 0), (int(fx(1587) - dlc.mlength(seatclass, 11)), int(fy(455))), 255, 7)
                    else:
                        dlc.moutput(screen, "二等座", (0, 0, 0), (int(fx(1587) - dlc.mlength("二等座", 11)), int(fy(455))), 255, 7)
                
                dlc.moutput(screen, tips1, (0, 0, 0), (int(fx(107)), int(fy(560))), 255, 11)
                dlc.moutput(screen, tips2, (0, 0, 0), (int(fx(107)), int(fy(665))), 255, 11)
                
                if idname:
                    ##做隐藏变*操作（未对纪念票做适配|最后更新时没有纪念票）
                    if len(idname) >= 19:
                        idname1 = f"#6$#y-={str03(int(fy(7)),'y-=')}" + idname[:10] + f"#y+={str03(int(fy(4)),'y+=')}****#y-={str03(int(fy(4)),'y-=')}" + idname[14:19] + f"#11#y+={str03(int(fy(7)),'y+=')}" + idname[19:]
                    else:
                        idname1 = f"#6$#y-={str03(int(fy(2)),'y-=')}" + idname
                    dlc.moutput(screen, idname1, (0, 0, 0), (int(fx(107)), int(fy(753))), 255, 11)
                
                ##计算线框宽度什么的并渲染
                kd = (290) / 27 * 3.5
                for i in range(27):
                    pygame.draw.line(screen, (0, 0, 0),
                                   (int(fx(205 + kd * i)), int(fy(832))),
                                   (int(fx(205 + kd * i + kd/3*2)), int(fy(832))), int(1 * fbl_multiply))
                    pygame.draw.line(screen, (0, 0, 0),
                                   (int(fx(205 + kd * i)), int(fy(962))),
                                   (int(fx(205 + kd * i + kd/3*2)), int(fy(962))), int(1 * fbl_multiply))
                
                kd2 = (140) / 4
                x2 = 1210
                for i in range(4):
                    pygame.draw.line(screen, (0, 0, 0),
                                   (int(fx(200)), int(fy(832 + kd2 * i))),
                                   (int(fx(200)), int(fy(832 + kd2 * i + kd2/3*2))), int(1 * fbl_multiply))
                    pygame.draw.line(screen, (0, 0, 0),
                                   (int(fx(x2)), int(fy(832 + kd2 * i))),
                                   (int(fx(x2)), int(fy(832 + kd2 * i + kd2/3*2))), int(1 * fbl_multiply))
                
                dlc.moutput(screen, und1, (0, 0, 0), (int(fx(730) - dlc.mlength(und1, 16)//2), int(fy(844))), 255, 16)
                dlc.moutput(screen, und2, (0, 0, 0), (int(fx(730) - dlc.mlength(und2, 16)//2), int(fy(904))), 255, 16)
                dlc.moutput(screen, undl, (0, 0, 0), (int(fx(107)), int(fy(971))), 255, 16)

               ##渲染qrcode的矢量图数据 
                if using_QRcode:
                    try:
                        qr_img = pygame.image.load(resource_path("picts/QRcode.png"))
                        screen.blit(qr_img, (int(395 * fbl_multiply), int(199 * fbl_multiply)))
                    except:
                        pass
            
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:##点击即截图
                        if page == "main":
                            idname2 = idname.replace("#12", "") if idname else ""
                            export_dir = resource_path(f"截图导出/{idname2}")
                            if not os.path.exists(export_dir):
                                os.makedirs(export_dir)
                            screenshot_path = os.path.join(export_dir, f"{time.strftime('%Y%m%d%H%M%S')}.png")
                            pygame.image.save(screen, screenshot_path)
                            dlc.addts(f"截图已保存: {screenshot_path}", color=(10, 100, 20))
            
            pygame.display.flip()
            tick.tick(20)
        
        except Exception as e:
            pass
    
    pygame.quit()

def run_tkinter_control(shared_data, refresh_queue):
    root = tk.Tk()
    root.title(f"<不要关闭此窗口> 火车票根生成器-控制面板 v{bbh}")
    root.geometry("400x300")
    
    # 创建输入框变量
    input_var = tk.StringVar()
    
    def reload_data():
        load_data(shared_data)
        refresh_queue.put('data_updated')
    
    def save_current_data():
        save_data(shared_data)
    
    tk.Label(root, text=f"火车票根生成器 控制面板", font=(None, 14)).pack(pady=10)
    
    # 输入框（替换保存当前数据上方的按钮）
    tk.Label(root, text="粘贴输入框:", font=(None, 10)).pack(pady=5)
    input_entry = tk.Entry(root, textvariable=input_var, width=30)
    input_entry.pack(pady=5)
    
    # 保存当前数据按钮
    tk.Button(root, text="保存当前数据", command=save_current_data, width=25).pack(pady=5)
    
    # 重新加载数据按钮
    tk.Button(root, text="重新加载数据 (data.txt)", command=reload_data, width=25).pack(pady=5)
    
    tk.Label(root, text="提示: 编辑窗口修改数据后会自动同步到显示窗口", fg="gray").pack(pady=20)
    
    # 定期更新shared_data中的输入框内容
    def update_input_data():
        # 使用索引66存储输入框内容
        while len(shared_data) <= 66:
            shared_data.append("")
        shared_data[66] = input_var.get()
        root.after(100, update_input_data)
    
    update_input_data()
    root.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    manager = Manager()
    shared_data = manager.list()
    refresh_queue = manager.Queue()
    
    load_data(shared_data)
    
    p_edit = multiprocessing.Process(target=run_edit_window, args=(shared_data, refresh_queue))
    p_display = multiprocessing.Process(target=run_display_window, args=(shared_data, refresh_queue))
    
    p_edit.start()
    p_display.start()
    
    run_tkinter_control(shared_data, refresh_queue)
    
    p_edit.terminate()
    p_display.terminate()
    p_edit.join()
    p_display.join()
    manager.shutdown()

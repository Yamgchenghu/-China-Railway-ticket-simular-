from audioop import add
import pygame
import time,os,sys,pyperclip
from pypinyin import lazy_pinyin,pinyin
bbh = "0.1.2  2025-09-21"
##制作pyinstaller兼容的文件打开系统(绝对路径+相对路径)
def resource_path(relative_path,is_inside=0):#取出绝对路径
    if hasattr(sys, '_MEIPASS') and is_inside==1:
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
def mopen(file_path,mode='r',encoding='utf-8',is_inside=0):
    return open(resource_path(file_path,is_inside=is_inside),mode,encoding=encoding)
try:
    import files.dlc as dlc  # 直接使用开发时的导入方式
except ImportError:
    # 极端情况处理（一般不需要）
    current_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(current_dir, "dlc"))
    import files.dlc as dlc  # 导入dlc模块

##判断绝对路径下是否有<备份>文件夹，如果没有则创建
backup_dir = os.path.join(os.path.dirname(resource_path("data.txt")), "备份")
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)


##初始化
pygame.init()

screen = pygame.display.set_mode((540,307))
pygame.display.set_caption("中国铁路火车票模拟生成系统-编辑系统       v"+bbh)
tick = pygame.time.Clock()
page = "FW"
pst_time =0
npt=0
paste_need=""
paste=""
dengji=["G","D","C","S","Z","K","T","L","Y"]
dlc.fontupload(resource_path("ttf/simw.ttf"),17)
dlc.fontupload(resource_path("ttf/simw.ttf"),14,1)
dlc.fontupload(resource_path("ttf/simw.ttf"),17,2)
dlc.fontupload(resource_path("ttf/simw.ttf"),24,3)
dlc.fontupload(resource_path("ttf/simw.ttf"),17,4)
dlc.fontupload(resource_path("ttf/simw.ttf"),13,5)
dlc.fontupload(resource_path("ttf/simw.ttf"),17,10)
dlc.fontupload(resource_path("ttf/simw.ttf"),17,12)
dlc.fontupload(resource_path("ttf/simw.ttf"),17,15)
def o():
    global data
    with mopen(resource_path("data.txt")) as f:
            data = f.readlines()

            for i in range(len(data)):
                data[i] = data[i].strip()
    #备份至新的文件（以日期时间命名）
    backup_file = os.path.join(backup_dir, f"data_{time.strftime('%Y%m%d%H%M%S')}.txt")
    with mopen(backup_file,'w') as f:
        for i in data:
            try:
                if i[-1]!="\n":
                    f.write(i+'\n')
                else:
                    f.write(i)
            except:
                f.write(i)
           
o()
def s():
    global data
    for i in range(len(data)):
        if data[i]=="" or data[i]=="\n":
            data[i]="$"


    with mopen(resource_path("data.txt"),'w') as f:
        for i in data:
            try:
                if i[-1]!="\n":
                    f.write(i+'\n')
                else:
                    f.write(i)
            except:
                f.write(i)

flips=0
tmd_ztcsjm=-40
tmd_ztcsjm_zf=2
sfxx_pmks3=["",""]
while True:
    flips+=1.5
    tmd_ztcsjm+=tmd_ztcsjm_zf
    if tmd_ztcsjm>220 or tmd_ztcsjm<40 and flips>=125:
        tmd_ztcsjm_zf*=-1
    ##右上角output显示存读档
    screen.fill((255,255,255))
    try:#强制展示base.png
        try:
            if data[54]=='1' or data[54]=='1\n':
                base_img = pygame.image.load(resource_path("picts/base.png"))
                screen.blit(base_img, (0, 0))
        except:
            base_img = pygame.image.load(resource_path("picts/base.png"))
            screen.blit(base_img, (0, 0))
    except:
        pass

    dlc.moutput(screen,"#p5F00 6E90 7248 672C FF0C 6CE8 610F 9690 79C1#",(100,100,100),(270-243//2,280))
    dlc.moutput(screen,"#c000235178存档  #R读档",(100,100,100),(440,10))
    if page=="FW":
        dlc.moutput(screen,"#H编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#B欢迎使用#R中国铁路#B火车票模拟生成系统",(100,100,100),((270-dlc.mlength("欢迎使用#R中国铁路火车票模拟生成系统",num=3)//2),70),num=3)
        dlc.moutput(screen,"           #Lby-紫潼-",(100,100,100),((460-dlc.mlength("           by-紫潼-",num=1)//2),95),num=1,tm=min(flips+60,255))
        dlc.moutput(screen,"#D中国铁路在2025年10月1日全面取消纸质车票",(100,100,100),((270-dlc.mlength("中国铁路在2025年10月1日全面取消纸质车票",num=0)//2),115),num=0,tm=min(flips-250,255))
        dlc.moutput(screen,"#Z于此而来的是伴随我们多年的纸质车票的消逝",(100,100,100),((270-dlc.mlength("于此而来的是伴随我们多年的纸质车票的消逝",num=0)//2),135),num=0,tm=min(flips-450,255))
        dlc.moutput(screen,"#D一张小小的车票，承载着多年的旅途记忆",(100,100,100),((270-dlc.mlength("一张小小的车票，承载着多年的旅途记忆",num=0)//2),155),num=0,tm=min(flips-650,255))
        dlc.moutput(screen,"#Z为了纪念以往的车票，使其在数字世界继续焕发生机",(100,100,100),((270-dlc.mlength("为了纪念以往的车票，使其在数字世界继续焕发生机",num=0)//2),175),num=0,tm=min(flips-850,255))
        dlc.moutput(screen,"#O<中国铁路火车票模拟生成系统>###诞生了",(100,100,100),((270-dlc.mlength("<中国铁路火车票模拟生成系统>诞生了",num=0)//2),195),num=0,tm=min(flips-1050,255))
        dlc.moutput(screen,"#R点按任意位置进入系统",(100,100,100),((270-dlc.mlength("点按任意位置进入系统",num=0)//2),240),num=0,tm=tmd_ztcsjm)
    if page == "M1":
        #处理站名空格
        if len(data[10])==3 and "\n" in data[10]:
            data[10]=data[10][0]+"  "+data[10][1]

        if len(data[18])==3 and "\n" in data[18]:
            data[18]=data[18][0]+"  "+data[18][1]


        dlc.moutput(screen,"#B编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#R车票编号#x100#R"+data[4],(100,100,100),(10,40))
        dlc.moutput(screen,"#Z检票口#x100###"+data[7],(100,100,100),(10,60))
        dlc.moutput(screen,"#P出发站#x100###"+data[10],(100,100,100),(10,80))
        if data[10][0:3]=="#10":
            dlc.moutput(screen,"#O站名花体显示[#G√#O]",(100,100,100),(310,80))
        else:
            dlc.moutput(screen,"#H站名花体显示[    ]",(100,100,100),(310,80))
        dlc.moutput(screen,"#Z终点站#x100###"+data[18],(100,100,100),(10,100))
        dlc.moutput(screen,"#P车次#x100###"+data[15],(100,100,100),(10,120))
        dlc.moutput(screen,"#Z出发时间#x100###"+data[22],(100,100,100),(10,140))
        dlc.moutput(screen,"#P票价#x100###"+data[27],(100,100,100),(10,160))
        dlc.moutput(screen,"#Z座位#x100###"+data[25],(100,100,100),(10,180))
        if data[30]==""or data[30]=="None":
            dlc.moutput(screen,"#P车票类型#x100###"+"#D无",(100,100,100),(10,200))
        else:
            dlc.moutput(screen,"#P车票类型#x100###"+data[30],(100,100,100),(10,200))
        dlc.moutput(screen,"#Z席别#x100###"+data[33],(100,100,100),(10,220))

    if page == "S1" or page=="S2" or page=="SZ" or page == "TP":#搜索车站通用页面

        dlc.moutput(screen,"#D编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        stns=[["上海","上海西","上海虹桥","上海南","上海松江","金山北","安亭北","安亭西","","",""],
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





        #遍历stns,输出每个列表的元素,并在每个元素前添加#P
        dlc.moutput(screen,"#Z提供部分站点可以选择，若无，可按CTRL+V读取剪切板",(100,100,100),((540-dlc.mlength("提供部分站点可以选择，若无，可按CTRL+V读取剪切板",num=0))//2,40))

        for i in range(len(stns)):
            for j in range(len(stns[i])):
                dlc.moutput(screen,"#P"+stns[i][j],(100,100,100),(10+63*j,60+20*i),num=1)
    if page == "BH":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z车票编号#x100#O<#R"+data[4]+"#O>",(100,100,100),(10,40))
        for i in range(10):
            dlc.moutput(screen,str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
        #字母A~Z输入
        for i in range(15):
            dlc.moutput(screen,chr(65+i),(180,60,220),(50+30*i,120),num=0)
        for i in range(11):
            dlc.moutput(screen,chr(80+i),(180,60,220),(50+30*i,150),num=0)
        dlc.moutput(screen,"#R<清除>",(240,140,60),(400,150),num=0)
    if page == "CI":#快速输入检票口
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#L检票口#x100#O<#R"+data[7]+"#O>#x370#1点此粘贴插入自定义检票口",(100,100,100),(10,40))
        for i in range(10):
            dlc.moutput(screen,str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"A#x380B",(240,140,60),(350,80),num=0)
        dlc.moutput(screen,"#R<清除>#x480<退格>",(240,140,60),(420,80),num=0)
        dlc.moutput(screen,"一#x100二#x150三#x200楼#x250候车室#x350检票口",(40,140,180),(50,120),num=0)
        dlc.moutput(screen,"<点>#x080<空格>#x150东#x200南#x250西#x300北#x350广场#x400进站",(40,140,180),(30,160),num=0)
    if page =="CC":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z车次#x100#O<#R"+data[15]+"#O>",(100,100,100),(10,40))
        for i in range(10):
            dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
        
        for i in range(9):
            dlc.moutput(screen,"#L"+dengji[i],(240,140,60),(50+30*i,120),num=0)
        dlc.moutput(screen,"#R<清除>",(240,140,60),(400,120),num=0)
    if page == 'TI':#时间
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z发车时间#x100#O<#R"+data[22]+"#O>",(100,100,100),(10,40))
        dlc.moutput(screen,"#R年:",(100,100,100),(10,80))

        for i in range(25,43):
            i2=str(i)
            dlc.moutput(screen,"#P"+i2,(100,100,100),(50+25*(i-24),60),num=1)
        for i in range(43,61):
            i2=str(i)
            dlc.moutput(screen,"#P"+i2,(100,100,100),(50+25*(i-42),80),num=1)
        for i in range(61,79):
            i2=str(i)
            dlc.moutput(screen,"#P"+i2,(100,100,100),(50+25*(i-60),100),num=1)

        dlc.moutput(screen,"#D月:",(100,100,100),(10,124))
        for i in range(1,13):
            i2=str(i)
            dlc.moutput(screen,"#Z"+i2,(100,100,100),(50+25*i,124),num=1)
        dlc.moutput(screen,"#B日:",(100,100,100),(10,160))
        for i in range(1,16):
            i2=str(i)
            dlc.moutput(screen,"#L"+i2,(100,100,100),(50+27*i,150))
        for i in range(16,32):
            i2=str(i)
            dlc.moutput(screen,"#L"+i2,(100,100,100),(50+27*(i-15),170))
        dlc.moutput(screen,"时:",(100,100,100),(10,200))
        for i in range(12):
            dlc.moutput(screen,i,(100,100,100),(76+26*i,190))
        for i in range(12,24):
            dlc.moutput(screen,i,(100,100,100),(76+26*(i-12),210))
        dlc.moutput(screen,"分:",(100,100,100),(10,260))
        for i in range(20):
            dlc.moutput(screen,i,(100,100,100),(70+20*i,240),num=1)
        for i in range(20,40):
            dlc.moutput(screen,i,(100,100,100),(70+20*(i-20),260),num=1)
        for i in range(40,60):
            dlc.moutput(screen,i,(100,100,100),(72+20*(i-40),280),num=1)
    if page == "JG":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z票价#x100#O<#R"+data[27]+"#O>",(100,100,100),(10,40))
        for i in range(10):
            dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"#L<小数点>#x440#R<退格>",(240,140,60),(350,80),num=0)
    if page == "ST":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z座位#x100#O<#R"+data[25]+"#O>",(100,100,100),(10,40))
        for i in range(10):
            dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=0)
        dlc.moutput(screen,"#Z加 #x100车 #x150号 #x200无座 #x250上铺 #x300中铺 #x350下铺",(240,140,60),(50,110),num=0)
        dlc.moutput(screen,"#DA #x100B #x150C #x200D #x250F #x300 #x350#R<清空>",(240,140,60),(50,140),num=0)
    if page == "LB":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z类别#x100#O<#R"+data[30]+"#O>",(100,100,100),(10,40))
        dlc.moutput(screen,"#Z<空> #x100学 #x150孩 #x200惠 #x250网 #x300微 #x350#R<退格>",(240,140,60),(50,80),num=0)
        dlc.moutput(screen,"#H<预留> #x100<预留> #x150<预留> #x200<预留> #x250<预留> #x300<预留> #x350<预留>",(240,140,60),(50,110),num=0)
        dlc.moutput(screen,"#H<预留> #x100<预留> #x150<预留> #x200<预留> #x250<预留> #x300<预留> #x350<预留>",(240,140,60),(50,140),num=0)
    if page == "XB":
        dlc.moutput(screen,"#D编辑车次  #H编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#Z席别#x100#O<#R"+data[33]+"#O>",(100,100,100),(10,40))
        dlc.moutput(screen,"#Z一等 #x100二等 #x150特等 #x200商务 #x250优选 #x300座 #x350#R<退格>",(240,140,60),(50,80),num=0)
        dlc.moutput(screen,"#D软 #x100硬 #x150卧 #x200动 #x250高级 #x300新 #x350空调 #x400无 #x450代",(240,140,60),(50,110),num=0)
        dlc.moutput(screen,"#H与 #x100普客 #x150普快 #x200特快 #x250差 #x300 #x350",(240,140,60),(50,140),num=0)
    if page == "M2":
        dlc.moutput(screen,"#H编辑车次  #B编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        if "#"in data[36]:
            dlc.moutput(screen,"#P第一行信息#x100#B<通票>",(100,100,100),(10,40))
        else:
            dlc.moutput(screen,"#P第一行信息#x100###"+data[36],(100,100,100),(10,40))
        dlc.moutput(screen,"#Z第二行信息#x100###"+data[39],(100,100,100),(10,60))
        dlc.moutput(screen,"#P身份信息$$#x100###"+data[42],(100,100,100),(10,80))
        dlc.moutput(screen,"#Z提示框上行#x100###"+data[46],(100,100,100),(10,100))
        dlc.moutput(screen,"#P提示框下行#x100###"+data[47],(100,100,100),(10,120))
        dlc.moutput(screen,"#Z提示框底部#x100###"+data[50],(100,100,100),(10,140))
        
    if page == "PM-KS12":#第一，第二行信息
        dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        if "#"in data[36]:
            dlc.moutput(screen,"#P第一行信息#x100#B<通票>",(100,100,100),(10,40))
            dlc.moutput(screen,"#Z第二行信息#x100###"+data[39],(100,100,100),(10,60))
        else:
            dlc.moutput(screen,"#P第一行信息#x100###"+data[36],(100,100,100),(10,40))
            dlc.moutput(screen,"#Z第二行信息#x100###"+data[39],(100,100,100),(10,60))
        dlc.moutput(screen,"#O点按#R上方#O对应内容粘贴#P自定义内容#O，下方是部分预设（#D联系作者可加#O）",(100,100,100),(270-(dlc.mlength("点按上方对应内容粘贴自定义内容，下方是部分预设（联系作者可加）",num=1))//2,80),num=1)
        dlc.moutput(screen,"#O<报销凭证格式> #x200<原版车票格式> #x350<通票签证格式>",(100,100,100),(50,100))
        dlc.moutput(screen,"#D<始发改签> #x150#L<退票费> #x250<改签费> #x350#H<自定义通票>",(100,100,100),(50,120))
        dlc.moutput(screen,"#H<预留> #x200<预留> #x350<预留>",(100,100,100),(50,140))
    if page == "PM-KS3":#身份信息
        dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        
        dlc.moutput(screen,"#P身份证号#x100###"+sfxx_pmks3[0],(100,100,100),(10,40))
        dlc.moutput(screen,"#P姓名#x100###"+sfxx_pmks3[1],(100,100,100),(10,60))
        dlc.moutput(screen,"#O输入#R姓名#O请点击姓名#P所在行#O。#5#y+=002#c240100010正版程序中，断网可正常使用本功能。",(100,100,100),(270-(dlc.mlength("输入姓名请点击姓名所在行。#5正版程序中，断网可正常使用本功能。",num=1))//2,80),num=1)
        for i in range(10):
            dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,110),num=0)
        dlc.moutput(screen,"#ZX",(240,140,60),(400,110),num=0)
        dlc.moutput(screen,"#R<退格>#x250#c032160064<键入并退出>",(240,140,60),(150,140),num=0)
    if page == "PM-KN":
        dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#P第一行信息#x100###"+data[46],(100,100,100),(10,40))
        dlc.moutput(screen,"#Z第二行信息#x100###"+data[47],(100,100,100),(10,60))
        dlc.moutput(screen,"#O点按#R上方#O对应内容粘贴#P自定义内容#O，下方是部分预设（#D联系作者可加#O）",(100,100,100),(270-(dlc.mlength("点按上方对应内容粘贴自定义内容，下方是部分预设（联系作者可加）",num=1))//2,80),num=1)
        dlc.moutput(screen,"#O<标准> #x150<国庆> #x250<报销> #x350#H<预留>",(100,100,100),(50,100))
        dlc.moutput(screen,"#H<预留> #x150<预留> #x250<预留> #x350<预留>",(100,100,100),(50,120))
    if page == "PM-KD":
        dlc.moutput(screen,"#H编辑车次  #D编辑票面  #H其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        
        dlc.moutput(screen,"#P票据编码#x100###"+sfxx_pmks6[0],(100,100,100),(10,40))
        dlc.moutput(screen,"#Z发售站点#x100###"+sfxx_pmks6[1],(100,100,100),(10,60))
        for i in range(10):
            dlc.moutput(screen,"#B"+str(i),(240,140,60),(50+30*i,90),num=0)
        dlc.moutput(screen,f"#l<身份证购票>",(100,100,60),(400,90),num=0)
        cfz_pmks6=data[10]
        ddz_pmks6=data[18]
        if "#12" in cfz_pmks6:
            cfz_pmks6=cfz_pmks6[3:]
        if "  " in cfz_pmks6:
            cfz_pmks6=cfz_pmks6[0]+cfz_pmks6[3]
        if "  " in ddz_pmks6:
            ddz_pmks6=ddz_pmks6[0]+ddz_pmks6[3]
        dlc.moutput(screen,f"#R<退格>#x250####O<{cfz_pmks6}>#x400<{ddz_pmks6}>",(100,100,60),(100,115),num=0)
        dlc.moutput(screen,f"#c010160080<写入并关闭>",(100,100,60),(250,140),num=0)
    if page == "M3":
        dlc.moutput(screen,"#H编辑车次  #H编辑票面  #B其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        if data[54]=="1"or data[54]=="1\n":
            dlc.moutput(screen,"#P启用背景#x100#B[#x115√#x140]",(100,100,100),(10,40))
        else:
            dlc.moutput(screen,"#P启用背景#x100###[#x140]",(100,100,100),(10,40))
        
        if data[56]=="1"or data[56]=="1\n":
            dlc.moutput(screen,"#Z启用QR码#x100#B[#x115√#x140]",(100,100,100),(10,60))
        else:
            dlc.moutput(screen,"#Z启用QR码#x100###[#x140]",(100,100,100),(10,60))
        dlc.moutput(screen,"#R开源代码，如遇倒卖者请退款！#B注意隐私安全",(100,100,100),(10,100),num=1)
    if page == "GFMF":
        dlc.moutput(screen,"#H编辑车次  #H编辑票面  #B其他信息",(100,100,100),(10,10))
        pygame.draw.rect(screen,(0,128,168),(0,35,550,2))
        dlc.moutput(screen,"#R该版本无需维权",(100,100,100),(10,40))
        dlc.moutput(screen,user_input_num,(100,100,100),(10,110))
        for i in range(10):
            dlc.moutput(screen,"#P"+str(i),(240,140,60),(50+30*i,80),num=0)
        dlc.moutput(screen,"#R<退格>",(240,140,60),(400,80),num=1)
        dlc.moutput(screen,"#P<空>",(240,140,60),(360,80),num=1)
        













    for e in pygame.event.get():
        if e.type == pygame.KEYUP:
            if e.key==118:
                paste=pyperclip.paste()
                pst_time=not pst_time
                if npt!=pst_time:
                    if paste_need=="检票口输入":
                        data[7]+=paste
                        dlc.addts("已插入<检票口>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="出发站":
                        data[10]=paste+"\n"
                        return0=lazy_pinyin(data[10])
                        return1=""
                        for i in return0:
                            return1+=i
                        #把return1的第一个字母大写
                        return1=return1[0].upper()+return1[1:]
                        data[12]=return1
                        dlc.addts("已输入<出发站>信息",color=(10,10,20))
                        dlc.addts(f"出发站：<{data[10]}>",dlc.flips+25,color=(10,10,20))
                        paste_need=""
                        page="M1"

                    elif paste_need=="到达站":
                        data[18]=paste+"\n"
                        return0=lazy_pinyin(data[18])
                        return1=""
                        for i in return0:
                            return1+=i
                        #把return1的第一个字母大写
                        return1=return1[0].upper()+return1[1:]
                        data[20]=return1

                        dlc.addts("已输入<到达站>信息",color=(10,10,20))
                        dlc.addts(f"到达站：<{data[18]}>",dlc.flips+25,color=(10,10,20))
                        paste_need=""
                        page="M1"
                    elif paste_need=="外第一行":
                        data[36]=paste+"\n"
                        dlc.addts("已输入<提示第一行>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="外第二行":
                        data[39]=paste+"\n"
                        dlc.addts("已输入<提示第二行>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="姓名":
                        sfxx_pmks3[1]=paste
                        dlc.addts("已输入<姓名>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="内第一行":
                        data[46]=paste+"\n"
                        dlc.addts("已输入<框内第一行>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="内第二行":
                        data[47]=paste+"\n"
                        dlc.addts("已输入<框内第二行>信息",color=(10,10,20))
                        paste_need=""
                    elif paste_need=="发售站":
                        sfxx_pmks6[1]=paste+" 售"
                        dlc.addts("已输入<发售站>信息",color=(10,10,20))
                        paste_need=""
                        page="PM-KD"



        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if 490<e.pos[0]<540 and 10<e.pos[1]<40:
                    o()
                elif 440<e.pos[0]<490 and 10<e.pos[1]<40:
                    s()
                elif page=="FW":
                    page="M1"
                elif page=="M1":
                    if 10<e.pos[1]<40 and 90<e.pos[0]<170:
                        page="M2"
                    elif 10<e.pos[1]<40 and 170<e.pos[0]<250:
                        page="M3"
                    elif 40<e.pos[1]<60:
                        page="BH"
                    elif 60<e.pos[1]<80:
                        page="CI"
                    elif 80<e.pos[1]<100 and 0<e.pos[0]<300:
                        page = "S1"
                    elif 80<e.pos[1]<100 and 300<e.pos[0]<550:
                        if data[10][0:3]=="#10":
                            data[10]=data[10][3:]
                        else:
                            data[10]="#10"+data[10]

                    elif 100<e.pos[1]<120:
                        page="S2"
                    elif 120<e.pos[1]<140:
                        page="CC"
                    elif 140<e.pos[1]<160:
                        page="TI"
                    elif 160<e.pos[1]<180:
                        page="JG"
                    elif 180<e.pos[1]<200:
                        page="ST"
                    elif 200<e.pos[1]<220:
                        page="LB"
                    elif 220<e.pos[1]<240:
                        page="XB"



                elif page=="S1":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if 40<e.pos[1]<60:
                        paste_need="出发站"
                        npt=pst_time
                        dlc.addts("请粘贴输入<出发站>信息",color=(10,10,20))
                    if 60<e.pos[1]:
                        x=(e.pos[1]-60)//20
                        y=(e.pos[0]-10)//63
                        if 0<=x<11 and 0<=y<11:
                            data[10]=stns[x][y]+"\n"
                            return0=lazy_pinyin(data[10])
                            return1=""
                            for i in return0:
                                return1+=i
                            #把return1的第一个字母大写
                            return1=return1[0].upper()+return1[1:]
                            data[12]=return1

                            dlc.addts("已输入<出发站>信息",color=(10,10,20))
                            dlc.addts(f"出发站：<{data[10]}>",dlc.flips+25,color=(10,10,20))

                            paste_need=""
                            page="M1"
                elif page == "S2":#到达站
                    if 10<e.pos[1]<40:
                        page="M1"
                    if 40<e.pos[1]<60:
                        paste_need="到达站"
                        npt=pst_time
                        dlc.addts("请粘贴输入<到达站>信息",color=(10,10,20))
                    if 60<e.pos[1]:
                        x=(e.pos[1]-60)//20
                        y=(e.pos[0]-10)//63
                        if 0<=x<11 and 0<=y<11:
                            data[18]=stns[x][y]+"\n"
                            return0=lazy_pinyin(data[18])
                            return1=""
                            for i in return0:
                                return1+=i
                            #把return1的第一个字母大写
                            return1=return1[0].upper()+return1[1:]
                            data[20]=return1
                            dlc.addts("已输入<到达站>信息",color=(10,10,20))
                            dlc.addts(f"到达站：<{data[18]}>",dlc.flips+25,color=(10,10,20))
                            paste_need=""
                            page="M1"
                elif page=="BH":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if e.pos[1]>=70 and e.pos[1]<=100 and 0<e.pos[0]<400:
                        x=(e.pos[0]-50)//30
                        if len(data[4])<10:
                            data[4]+=str(x)
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=70 and e.pos[1]<=100 and e.pos[0]>400:
                        if data[4]!="":
                            data[4]=data[4][:-1]
                        else:
                            dlc.addts("数据为空",color=(240,100,20))
                    if e.pos[1]>=100 and e.pos[1]<=140:
                        ##输入字母
                        x=(e.pos[0]-50)//30
                        if 0<=x<15:
                            if len(data[4])<10:
                                data[4]+=chr(65+x)
                            else:
                                dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=140 and e.pos[1]<=180:
                        
                        ##输入字母
                        x=(e.pos[0]-50)//30
                        if 0<=x<11:
                            if len(data[4])<10:
                                data[4]+=chr(80+x)
                            else:
                                dlc.addts("数据超限",color=(240,100,20))
                        else:
                            data[4]=""
                elif page=="CI":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if 40<e.pos[1]<60:
                        paste_need="检票口输入"
                        npt=pst_time
                        dlc.addts("请粘贴插入<检票口>信息",color=(10,10,20))
                        dlc.addts("此功能不会替换现有数据，若需替换请点按<删除>按钮",dlc.flips+25,color=(250,134,10))

                    if e.pos[1]>=70 and e.pos[1]<=120 and 50<e.pos[0]<350:
                        x=(e.pos[0]-50)//30
                        data[7]+=str(x)
                    if e.pos[1]>=70 and e.pos[1]<=120 and 410>e.pos[0]>350:
                        data[7]+=chr(65+(e.pos[0]-350)//30)
                    if e.pos[1]>=70 and e.pos[1]<=120 and 470>e.pos[0]>420:
                        data[7]=""
                    if e.pos[1]>=70 and e.pos[1]<=120 and 600>e.pos[0]>470:
                        if data[7]=="":
                            dlc.addts("数据为空",color=(240,100,20))
                        else:
                            data[7]=data[7][:-1]
                    if e.pos[1]>=120 and e.pos[1]<=160 and 600>e.pos[0]>50:
                        if 100>e.pos[0]>50:
                            data[7]+="一"
                        elif 150>e.pos[0]>100:
                            data[7]+="二"
                        elif 200>e.pos[0]>150:
                            data[7]+="三"
                        elif 250>e.pos[0]>200:
                            data[7]+="楼"
                        elif 350>e.pos[0]>250:
                            data[7]+="候车室"
                        elif 450>e.pos[0]>350:
                            data[7]+="检票口"
                    if e.pos[1]>=160 and e.pos[1]<=200 and 600>e.pos[0]>30:
                        if 80>e.pos[0]>30:
                            data[7]+="."
                        elif 150>e.pos[0]>80:
                            data[7]+=" "
                        elif 200>e.pos[0]>150:
                            data[7]+="东"
                        elif 250>e.pos[0]>200:
                            data[7]+="南"
                        elif 300>e.pos[0]>250:
                            data[7]+="西"
                        elif 350>e.pos[0]>300:
                            data[7]+="北"
                        elif 400>e.pos[0]>350:
                            data[7]+="广场"
                        elif 450>e.pos[0]>400:
                            data[7]+="进站"
                elif page=="CC":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if e.pos[1]>=70 and e.pos[1]<=100 and 0<e.pos[0]<400:
                        x=(e.pos[0]-50)//30
                        if len(data[15])<6:
                            data[15]+=str(x)
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=70 and e.pos[1]<=100 and e.pos[0]>400:
                        if data[15]!="":
                            data[15]=data[15][:-1]
                        else:
                            dlc.addts("数据为空",color=(240,100,20))
                    if e.pos[1]>=100 and e.pos[1]<=140:
                        ##输入字母
                        x=(e.pos[0]-50)//30
                        if 0<=x<9:
                            data[15]=dengji[x]
                        else:
                            data[15]=""
                elif page=="TI":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if e.pos[1]>=60:
                        if e.pos[1]<80:
                            x=(e.pos[0]-50)//25+2024
                            data[22]=str(x)+data[22][4:]
                        elif e.pos[1]<101:
                            x=(e.pos[0]-50)//25+2042
                            data[22]=str(x)+data[22][4:]
                        elif e.pos[1]<121:
                            x=(e.pos[0]-50)//25+2060
                            data[22]=str(x)+data[22][4:]
                        elif e.pos[1]<140:
                            x=(e.pos[0]-50)//25
                            if x<=12:
                                if x>=10:
                                    data[22]=data[22][:5]+str(x)+data[22][7:]
                                else:
                                    data[22]=data[22][:5]+"0"+str(x)+data[22][7:]
                        elif e.pos[1]<171:
                            x=(e.pos[0]-50)//27
                            if x<=16:
                                if x>=10:
                                    data[22]=data[22][:8]+""+str(x)+data[22][10:]
                                else:
                                    data[22]=data[22][:8]+"0"+str(x)+data[22][10:]
                        elif e.pos[1]<190:
                            x=(e.pos[0]-50)//27+15
                            if x<=31:
                                if x>=10:
                                    data[22]=data[22][:8]+""+str(x)+data[22][10:]
                                else:
                                    data[22]=data[22][:8]+"0"+str(x)+data[22][10:]
                        elif e.pos[1]<210:
                            x=(e.pos[0]-50)//26-1
                            if x<=11:
                                if x>=10:
                                    data[22]=data[22][:11]+""+str(x)+data[22][13:]
                                else:
                                    data[22]=data[22][:11]+"0"+str(x)+data[22][13:]
                        elif e.pos[1]<240:
                            x=(e.pos[0]-50)//26+11
                            if x<=23:
                                if x>=10:
                                    data[22]=data[22][:11]+""+str(x)+data[22][13:]
                                else:
                                    data[22]=data[22][:11]+"0"+str(x)+data[22][13:]
                        elif e.pos[1]<260:
                            x=(e.pos[0]-50)//20-1
                            if x<=19:
                                if x>=10:
                                    data[22]=data[22][:14]+""+str(x)
                                else:
                                    data[22]=data[22][:14]+"0"+str(x)
                        elif e.pos[1]<280:
                            x=(e.pos[0]-50)//20+19
                            if x<=39:
                                if x>=10:
                                    data[22]=data[22][:14]+""+str(x)
                        elif e.pos[1]<300:
                            x=(e.pos[0]-50)//20+39
                            if x<=59:
                                if x>=10:
                                    data[22]=data[22][:14]+""+str(x)
                elif page=="JG":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if e.pos[1]>=70 and e.pos[1]<=100 and 0<e.pos[0]<350:
                        x=(e.pos[0]-50)//30
                        if len(data[27])<6:
                            data[27]+=str(x)
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=70 and e.pos[1]<=100 and 440>e.pos[0]>350:
                        if len(data[27])<6:
                            data[27]+="."
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=70 and e.pos[1]<=100 and 490>e.pos[0]>440:
                        if len(data[27])>0:
                            data[27]=data[27][:-1]
                        else:
                            dlc.addts("数据为空",color=(240,100,20))
                elif page=="ST":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if e.pos[1]>=70 and e.pos[1]<=100 and 0<e.pos[0]<350:
                        x=(e.pos[0]-50)//30
                        if len(data[25])<12:
                            data[25]+=str(x)
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if e.pos[1]>=70 and e.pos[1]<=100 and 450>e.pos[0]>395:
                       if len(data[25])>0:
                           data[25]=data[25][:-1]
                       else:
                           dlc.addts("数据为空",color=(240,100,20))
                    if 140>=e.pos[1]>=110 and 50<e.pos[0]<400:
                        cin_temp=["加","车","号","无座","上铺","中铺","下铺"]
                        x=(e.pos[0]-50)//50
                        if x<=6 and len(data[25])<12:
                            data[25]+=cin_temp[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if 170>=e.pos[1]>=140 and 50<e.pos[0]<300:
                        cin_temp=["A","B","C","D","F"]
                        x=(e.pos[0]-50)//50
                        if x<=4 and len(data[25])<12:
                            data[25]+=cin_temp[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if 170>=e.pos[1]>=140 and 350<e.pos[0]<400:
                        data[25]=""
                elif page=="LB":
                    if 10<e.pos[1]<40:
                        page="M1"
                    if data[30]!=""and data[30]!="None" and data[30]!="\n" and data[30]!="None\n":
                        addxg=1
                    else:
                        addxg=0
                    lb_dyh=["学","孩","惠","网","微"]
                    lb_deh=["","","","","","",""]
                    lb_dsh=["","","","","","",""]
                    if 80<e.pos[1]<109 and 100<e.pos[0]<350:
                        x=(e.pos[0]-100)//50
                        if x<=4 and len(data[30])<7:
                            if addxg:
                                data[30]+="/"+lb_dyh[x]
                            else:
                                data[30]=lb_dyh[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if 80<e.pos[1]<110 and 50<e.pos[0]<100:
                        data[30]="None"
                    if 80<e.pos[1]<110 and 350<e.pos[0]<400 and len(data[30])>2 and data[30]!="None":
                        data[30]=data[30][:-2]
                    if 110<e.pos[1]<140 and 50<e.pos[0]<400:
                        x=(e.pos[0]-50)//50
                        if x<=7 and len(data[30])<7:
                            if addxg:
                                data[30]+="/"+lb_deh[x]
                            else:
                                data[30]=lb_deh[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    if 140<e.pos[1]<170 and 50<e.pos[0]<400:
                        x=(e.pos[0]-50)//50
                        if x<=7 and len(data[30])<7:
                            if addxg:
                                data[30]+="/"+lb_dsh[x]
                            else:
                                data[30]=lb_dsh[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                elif page=="XB":
                    if 10<e.pos[1]<40:
                        page="M1"
                    xb_syh=["一等","二等","特等","商务","优选","座"]
                    xb_seh=["软","硬","卧","动","高级","新","空调","无","代"]
                    if 80<e.pos[1]<109 and 50<e.pos[0]<350:
                        x=(e.pos[0]-50)//50
                        if x<6 and len(data[33])<15:
                            data[33]+=xb_syh[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    
                    if 80<e.pos[1]<110 and 350<e.pos[0]<400 and len(data[33])>0:
                        data[33]=data[33][:-1]
                    if 110<e.pos[1]<139 and 50<e.pos[0]<550:
                        x=(e.pos[0]-50)//50
                        if x<9 and len(data[33])<15:
                            data[33]+=xb_seh[x]
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                elif page=="M2":
                    if 10<e.pos[1]<40 and e.pos[0]<90:
                        page="M1"
                    elif 10<e.pos[1]<40 and 170<e.pos[0]<250:
                        page="M3"
                    elif 40<e.pos[1]<80:
                        page="PM-KS12"
                    elif 80<e.pos[1]<100:
                        page="PM-KS3"
                        sfxx_pmks3=data[42].split("    ")
                    elif 100<e.pos[1]<140:
                        page="PM-KN"
                    elif 140<e.pos[1]<160:
                        page="PM-KD"
                        sfxx_pmks6=[data[50][:14],data[50][23:]]
                elif page=="PM-KS12":
                    if 0<e.pos[1]<40 and 0<e.pos[0]<300:
                        page="M2"
                        paste_need=""
                    elif 40<e.pos[1]<60:
                        ##申请粘贴信息，粘贴内容为"外第一行"
                        paste_need="外第一行"
                        npt=pst_time
                        dlc.addts("请粘贴输入<提示第一行>信息",color=(10,10,20))
                    elif 60<e.pos[1]<80:
                        paste_need="外第二行"
                        npt=pst_time
                        dlc.addts("请粘贴输入<提示第二行>信息",color=(10,10,20))
                    elif 100<e.pos[1]<120:
                        ##选项
                        if 50<e.pos[0]<200:
                            if data[39]=="仅供报销使用":
                                data[36]=""
                                data[39]="仅供收藏使用"
                            else:
                                data[36]=""
                                data[39]="仅供报销使用"
                        elif 200<e.pos[0]<350:
                            data[36]="限乘当日当次车"
                            data[39]=""
                        elif 350<e.pos[0]<480:
                            data[36]="限乘当日当次车 随原票使用"
                            data[39]="中转"
                    elif 120<e.pos[1]<140:
                        if 50<e.pos[0]<150:
                            if data[36]=="":
                                if data[39]!="仅供收藏使用":
                                    data[39]="始发改签 "+data[39]
                                else:
                                    dlc.addts("收藏票不支持",color=(240,100,20))
                            else:
                                dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                        elif 150<e.pos[0]<250:
                            if data[36]=="":
                                data[36]="退票费"
                                dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                            elif data[39]=="":
                                data[39]="退票费"
                                dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                            else:
                                dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                        elif 250<e.pos[0]<350:
                            if data[36]=="":
                                data[36]="改签费"
                                dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                            elif data[39]=="":
                                data[39]="改签费"
                                dlc.addts("如有错误，欢迎指正！",color=(240,100,20))
                            else:
                                dlc.addts("无法匹配格式，请手动输入！",color=(240,100,20))
                elif page=="PM-KS3":
                    if 0<e.pos[1]<40 and 0<e.pos[0]<300:
                        page="M2"
                        paste_need=""    
                    elif 60<e.pos[1]<80: 
                        paste_need="姓名"
                        npt=pst_time
                        dlc.addts("请粘贴输入<乘车人姓名>信息",color=(10,10,20))
                    elif 100<e.pos[1]<140:
                        x=(e.pos[0]-50)//30
                        if 0<=x<=9 and len(sfxx_pmks3[0])<18:
                            if len(sfxx_pmks3[0])==6 and (x!=1 and x!=2):
                                dlc.addts("数据不合法",color=(240,100,20))
                            elif len(sfxx_pmks3[0])==7 and ((sfxx_pmks3[0][6]=='2' and x>2) or (sfxx_pmks3[0][6]=='1' and x<9)):
                                dlc.addts("数据不合法",color=(240,100,20))
                            else:
                                sfxx_pmks3[0]+=str(x)
                        elif 0<=x<=9 and len(sfxx_pmks3[0])>=18:
                            sfxx_pmks3[0]=str(x)
                        elif  len(sfxx_pmks3[0])==17 and 450>e.pos[0]>400:
                            sfxx_pmks3[0]+="X"
                    elif 140<e.pos[1]<170:
                        if 150<e.pos[0]<250:
                            if len(sfxx_pmks3[0])>0:
                                sfxx_pmks3[0]=sfxx_pmks3[0][:-1]
                            else:
                                dlc.addts("数据为空",color=(240,100,20))
                        elif 250<e.pos[0]<350:
                            if len(sfxx_pmks3[0])<=17 or sfxx_pmks3[1]=="":
                                dlc.addts("数据不合法,无法保存",color=(240,100,20))
                                continue
                            data[42]=sfxx_pmks3[0]+'    '+sfxx_pmks3[1]
                            page="M2"
                            paste_need=""
                elif page=="PM-KN":
                    if 0<e.pos[1]<40 and 0<e.pos[0]<300:
                        page="M2"
                        paste_need=""    
                    elif 40<e.pos[1]<60:
                        ##申请粘贴信息，粘贴内容为"外第一行"
                        paste_need="内第一行"
                        npt=pst_time
                        dlc.addts("请粘贴输入<框内第一行>信息",color=(10,10,20))
                    elif 60<e.pos[1]<80:
                        paste_need="内第二行"
                        npt=pst_time
                        dlc.addts("请粘贴输入<框内第二行>信息",color=(10,10,20))
                    elif 100<e.pos[1]<140:
                        x=(e.pos[0]-50)//100
                        if x==0:
                            if data[46]!="买票请到12306 发货请到95306":
                                data[46]="买票请到12306 发货请到95306"
                            else:
                                data[46]="买票请到95306 发货请到12306"
                            data[47]="中国铁路祝您旅途愉快"
                        if x==1:
                            data[46]="欢度国庆 祝福祖国"
                            data[47]="中国铁路祝您旅途愉快"
                        if x==2:
                            if data[46]!="报销凭证 遗失不补":
                                data[46]="报销凭证 遗失不补"
                            else:
                                data[46]="仅供收藏 遗失不补"
                            data[47]="退票改签时须交回车站"
                elif page=="PM-KD":
                    if 0<e.pos[1]<40 and 0<e.pos[0]<300:
                        page="M2"
                        paste_need=""
                    if 60<e.pos[1]<80:
                        page="SZ"
                        paste_need=""
                    if 80<e.pos[1]<114:
                        if e.pos[0]<400:
                            x=(e.pos[0]-50)//30
                            if 0<=x<=9:
                                if len(sfxx_pmks6[0])<14:
                                    sfxx_pmks6[0]+=str(x)
                                else:
                                    dlc.addts("数据超限",color=(240,100,20))
                        elif 400<e.pos[0]<500:
                            if sfxx_pmks6[1]!="J M":
                                sfxx_pmks6[1]="J M"
                            else:
                                sfxx_pmks6[1]="H Z"
                    if 114<e.pos[1]<139:
                        if e.pos[0]<250:
                            if len(sfxx_pmks6[0])>0:
                                sfxx_pmks6[0]=sfxx_pmks6[0][:-1]
                            else:
                                dlc.addts("数据为空",color=(240,100,20))
                        elif 250<e.pos[0]<350:
                            sfxx_pmks6[1]=cfz_pmks6+" 售"
                        elif 350<e.pos[0]<450:
                            sfxx_pmks6[1]=ddz_pmks6+" 售"
                    if 139<e.pos[1]<169:
                        if len(sfxx_pmks6[0])!=14:
                            dlc.addts("数据不合法",color=(240,100,20))
                            continue
                        data[50]=sfxx_pmks6[0]+data[4][-7:]+"  "+sfxx_pmks6[1]
                        data[50]=data[50].replace("\n","")
                        page="M2"
                        paste_need=""
                elif page=="SZ":
                    if 10<e.pos[1]<40:
                        page="PM-KD"
                        paste_need=""
                    if 40<e.pos[1]<60:
                        paste_need="发售站"
                        npt=pst_time
                        dlc.addts("请粘贴输入<发售站>信息",color=(10,10,20))
                    if 60<e.pos[1]:
                        x=(e.pos[1]-60)//20
                        y=(e.pos[0]-10)//63
                        if 0<=x<11 and 0<=y<11:
                            sfxx_pmks6[1]=stns[x][y]+" 售"

                            paste_need=""
                            page="PM-KD"
                                
                elif page=="M3":
                    if 10<e.pos[1]<40 and e.pos[0]<90:
                        page="M1"
                    elif 10<e.pos[1]<40 and 90<e.pos[0]<170:
                        page="M2"
                    elif 40<e.pos[1]<60:
                        if data[54]=="1":
                            data[54]="0"
                        else:
                            data[54]="1"
                    elif 60<e.pos[1]<80:
                        if data[56]=="1":
                            data[56]="0"
                        else:
                            data[56]="1"
                    elif 100<e.pos[1]<114:
                        page="GFMF"
                        user_input_num=""
                elif page=="GFMF":
                    if 10<e.pos[1]<40 and e.pos[0]<90:
                        page="M1"
                    elif 10<e.pos[1]<40 and 90<e.pos[0]<170:
                        page="M2"
                    elif e.pos[1]>=70 and e.pos[1]<=100 and 0<e.pos[0]<400:
                        x=(e.pos[0]-50)//30
                        if x<10:
                            user_input_num+=str(x)
                        elif x<12:
                            user_input_num+=" "
                        else:
                            dlc.addts("数据超限",color=(240,100,20))
                    elif e.pos[1]>=70 and e.pos[1]<=100 and e.pos[0]>400:
                        if user_input_num!="":
                            user_input_num=user_input_num[:-1]
                        else:
                            dlc.addts("数据为空",color=(240,100,20))
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_BACKSPACE:
                if user_input_num!="":
                    user_input_num=user_input_num[:-1]
            elif e.key==pygame.K_SPACE:
                    user_input_num+=" "
            
            elif e.unicode.isdigit() or e.unicode.isspace():
                    user_input_num+=e.unicode
            elif e.unicode.isalpha():
                    user_input_num+=e.unicode.upper()  





    dlc.outputts(screen,1)
    pygame.display.flip()
    tick.tick(53)


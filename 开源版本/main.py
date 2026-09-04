##火车票票根生成器
j=0
minus_num=20
using_QRcode = 0
using_base_pic=1

import pygame
import time,os,sys,pyperclip
bbh = "1.1.0   2025-09-27"
##制作pyinstaller兼容的文件打开系统(绝对路径+相对路径)
def resource_path(relative_path,is_inside=0):
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

##初始化
pygame.init()

##字体
dlc.fontupload(resource_path("ttf/simhei.ttf"),28)
dlc.fontupload(resource_path("ttf/simsun.ttf"),21,1)
dlc.fontupload(resource_path("ttf/simhei.ttf"),34,2)
dlc.fontupload(resource_path("ttf/simsun.ttf"),13,3)#宋体，13大小
dlc.fontupload(resource_path("ttf/simsun.ttf"),29,4)
dlc.fontupload(resource_path("ttf/simhei.ttf"),26,5)
dlc.fontupload(resource_path("ttf/simsun.ttf"),22,6)
dlc.fontupload(resource_path("ttf/simhei.ttf"),20,7)#黑体，20大小
dlc.fontupload(resource_path("ttf/simhei.ttf"),15,8)
dlc.fontupload(resource_path("ttf/simsun.ttf"),20,9)
dlc.fontupload(resource_path("ttf/simw.ttf"),32,10)
dlc.fontupload(resource_path("ttf/simsun.ttf"),19,11)
dlc.fontupload(resource_path("ttf/simw.ttf"),20,12)
dlc.fontupload(resource_path("ttf/simsun.ttf"),24,13)
dlc.fontupload(resource_path("ttf/simsun.ttf"),7,14)
dlc.fontupload(resource_path("ttf/simsun.ttf"),23,15)
dlc.fontupload(resource_path("ttf/simsun.ttf"),14,16)
dlc.fontupload(resource_path("ttf/simsun.ttf"),18,17)
dlc.fontupload(resource_path("ttf/simw.ttf"),15,18)
dlc.fontupload(resource_path("ttf/simsun.ttf"),17,19)
def o():
    global red_code,enter_gate,sta_stn_chn,sta_stn_eng,tra_num,end_stn_chn,end_stn_eng,date,seat,money,midcode,seatclass,tips1,tips2,idname,und1,und2,undl,using_base_pic,using_QRcode
    global lyjcp,hbys,if_simsun
    with mopen(resource_path("data.txt")) as f:
            data = f.readlines()

            for i in range(len(data)):
                data[i] = data[i].strip()
            red_code = data[4]#车票红编码
            enter_gate = data[7]#检票口

            sta_stn_chn = data[10]#起点（中文）
            sta_stn_eng = data[12]#起点（英文）
            tra_num = data[15]#车次
            end_stn_chn = data[18]#终点（中文）
            end_stn_eng = data[20]#终点（英文）
            date = data[22].split("/")#日期
            
            seat = data[25].split("车")#座位
            money = data[27]#价格
            try:
                midcode = data[30].split("/")#中间编码
            except:
                midcode = ["",""]
            seatclass = data[33]
            tips1 = data[36]
            tips2 = data[39]
            idname = data[42]
            und1=data[46]
            und2=data[47]
            undl = data[50]
            using_base_pic=int(data[54])
            using_QRcode=int(data[56])
            lyjcp=int(data[58])
            hbys=data[60]
            if hbys!="" and hbys!="None" and hbys!="\n" and hbys !="$":
                hbys=hbys.split("|")
            if_simsun=data[62]
o()
tick=pygame.time.Clock()
screen = pygame.display.set_mode((540,307))
pygame.display.set_caption(f"中国铁路火车票模拟生成系统      v{bbh}")
ten=0
try:
    open(resource_path("files/隐私确认.txt"))
    page = "main"
except:
    page = "privacy"
ten=0
while 1:
    
    
    #screen.fill((135,206,250))
    screen.fill((255,255,255))
    if using_base_pic>=1:
        try:
            screen.blit(pygame.image.load(resource_path(f"picts/base{using_base_pic}.png")), (0, 0))
        except:
            pass

    if page == "main":
        #pygame.draw.rect(screen, (20, 120, 213), (0,  298,600, 45)) ##底部深蓝色条带
        if using_base_pic<3:
            dlc.moutput(screen,red_code,(255,90,90),(23,12))
        else:
            dlc.moutput(screen,red_code,(235,40,30),(23,12))

        if enter_gate=="旅游计次票" or enter_gate=="旅游计次票\n" or lyjcp==1:
            dlc.moutput(screen,"旅游计次票",(0,0,0),(500-dlc.mlength("旅游计次票",17),14),255,17)
        elif enter_gate!="" and enter_gate!="$" and enter_gate!="\n":
            dlc.moutput(screen,"检票:"+enter_gate,(0,0,0),(500-dlc.mlength("检票:"+enter_gate,17),14),255,17)
        #dlc.moutput(screen,"检票:"+enter_gate,(0,0,0),(510-dlc.mlength("检票:"+enter_gate,1),14),255,17)
        if '#10' in sta_stn_chn and ten==0:
            sta_stn_chn = sta_stn_chn[3:]
            ten=1
        else:
            if ten!=1:
                ten=0
        
        if ten:
            if len(sta_stn_chn)==2:
                sta_stn_chn = f"{sta_stn_chn[0]}  {sta_stn_chn[1]}"
            if len(end_stn_chn)==2:
                end_stn_chn = f"{end_stn_chn[0]}  {end_stn_chn[1]}"
            
            dlc.moutput(screen,'#y+=003'+sta_stn_chn+"#6#x+=010#y+=004站",(0,0,0),(36,45),255,10)
            dlc.moutput(screen,'#y+=003'+end_stn_chn+"#6#x+=010#y+=004站",(0,0,0),(341,45),255,10)
        else:
            if len(sta_stn_chn)==2:
                sta_stn_chn = f"{sta_stn_chn[0]}  {sta_stn_chn[1]}"
            if len(end_stn_chn)==2:
                end_stn_chn = f"{end_stn_chn[0]}  {end_stn_chn[1]}"
            
            dlc.moutput(screen,sta_stn_chn+"#6#x+=010#y+=007站",(0,0,0),(36,45),255,2)
            dlc.moutput(screen,end_stn_chn+"#6#x+=010#y+=007站",(0,0,0),(341,45),255,2)
        dlc.moutput(screen,sta_stn_eng,(0,0,0),(54,81),255,9)
        dlc.moutput(screen,sta_stn_eng,(0,0,0),(53,81),255,9)
        dlc.moutput(screen,end_stn_eng,(0,0,0),(358,81),255,9)
        dlc.moutput(screen,end_stn_eng,(0,0,0),(359,81),255,9)
        dlc.moutput(screen,tra_num,(0,0,0),(260-dlc.mlength(tra_num,4)//2,46),255,4)
        dlc.moutput(screen,tra_num,(0,0,0),(261-dlc.mlength(tra_num,4)//2,46),255,4)
        #箭头
        pygame.draw.line(screen, (0, 0, 0), (260-dlc.mlength("C3895",4)//2, 80), (268+dlc.mlength("C3895",4)//2, 80), 2)
        pygame.draw.line(screen, (0, 0, 0), (268+dlc.mlength("C3895",4)//2-dlc.mlength("5",4), 75), (268+dlc.mlength("C3895",4)//2, 80), 2)
        if lyjcp==0:
            dlc.moutput(screen,date[0]+"#3#x+=005#y+=007年#x+=005#y-=007#5"+date[1]+"#3#x+=005#y+=007月#x+=005#y-=007#5"+date[2]+"#3#x+=005#y+=007日#x+=005#y-=007#5"+date[3]+":"+date[4]+"#3#x+=005#y+=007开",(0,0,0),(25,105),255,5)
            try:
                if seat[0]!="不对号入座" and seat[0]!="$":
                    if "号"==seat[1][-1] and j==0:
                        seat[1] = seat[1][:-1]+f"#3#x+=004#y+=004号"
                        j=1
                    dlc.moutput(screen,"#y+=003"+seat[0]+"#3#x+=003#y+=004车#x+=003#y-=004#7"+seat[1],(0,0,0),(345,105),255,7)
                elif seat[0]=="不对号入座":
                    dlc.moutput(screen,"不对号入座",(0,0,0),(345,105),255,11)
            except:
                dlc.moutput(screen,seat[0],(0,0,0),(345,105),255,11)
        if type(hbys) == type("1"):
            dlc.moutput(screen,"#x+=005#y+=010%一08#y-=010#x-=005￥"+money+"#3#x+=003#y+=007元",(0,0,0),(25,130),255,5)
        elif hbys[0][0]=="$":
            dlc.output(screen,"$",(0,0,0),(25,130),255,5)
            dlc.moutput(screen,money+"#3#x+=003#y+=007"+hbys[1],(0,0,0),(45,130),255,5)
        else:
            dlc.moutput(screen,hbys[0]+money+"#3#x+=003#y+=007"+hbys[1],(0,0,0),(25,130),255,5)
        ##中部标记
        if midcode[0]!="None"and midcode[0]!="" :
            if len(midcode)==1:
                midcode="#零012"+midcode[0]
            elif len(midcode)==2:
                midcode = "#x-=023#零012"+midcode[0]+"  #x-=004#零012"+midcode[1]
            elif len(midcode)==3:
                midcode = "#x-=046#零012"+midcode[0]+"  #x+=002#零012"+midcode[1]+"  #x+=002#零012"+midcode[2]
            elif len(midcode)==4:
                midcode = "#x-=069#零012"+midcode[0]+"  #x+=004#零012"+midcode[1]+"   #x+=004#零012"+midcode[2]+"   #x+=004#零012"+midcode[3]
            dlc.moutput(screen,midcode,(0,0,0),(245,134),255,19)
        else:
            dlc.moutput(screen,"      ",(0,0,0),(245,130),255,11)
        if if_simsun=="1":
            if lyjcp==0:
                dlc.moutput(screen,seatclass,(0,0,0),(445-dlc.mlength(seatclass,11),130),255,11)
            else:
                dlc.moutput(screen,"二等座",(0,0,0),(445-dlc.mlength("二等座",11),130),255,11)
        else:
            if lyjcp==0:
                dlc.moutput(screen,seatclass,(0,0,0),(445-dlc.mlength(seatclass,11),130),255,7)
            else:
                dlc.moutput(screen,"二等座",(0,0,0),(445-dlc.mlength("二等座",11),130),255,7)
        dlc.moutput(screen,tips1,(0,0,0),(22,160),255,11)
        dlc.moutput(screen,tips2,(0,0,0),(22,190),255,11)
        dlc.moutput(screen,tips1,(0,0,0),(22.8,160),255,11)
        dlc.moutput(screen,tips2,(0,0,0),(22.8,190),255,11)
        ## idname打码 
        
        idname1="#6$#y-=002"+idname[:10]+"#y+=001****#y-=001"+idname[14:19]+"#11#y+=002"+idname[19:]
        dlc.moutput(screen,idname1,(0,0,0),(22,215),255,11)
        dlc.moutput(screen,idname1,(0,0,0),(22.3,215),255,11)
        dlc.moutput(screen,"-#x+=003"*minus_num,(0,0,0),(50,225),255,15)
        dlc.moutput(screen,"-#x+=003"*minus_num,(0,0,0),(50,269),255,15)
        for i in range(7):
            dlc.moutput(screen,"|#x047#y+=010"*4,(0,0,0),(47,242),255,14)
            dlc.moutput(screen,"|#x347#y+=010"*4,(0,0,0),(347,242),255,14)
            dlc.moutput(screen,"|#x046#y+=010"*4,(0,0,0),(46,242),255,14)
            dlc.moutput(screen,"|#x346#y+=010"*4,(0,0,0),(346,242),255,14)

        dlc.moutput(screen,und1,(0,0,0),(200-dlc.mlength(und1,16)//2,244),255,16)
        dlc.moutput(screen,und2,(0,0,0),(200-dlc.mlength(und2,16)//2,261),255,16)

        dlc.moutput(screen,undl,(0,0,0),(22,286),255,16)
        
        if using_QRcode:
            qr_img = pygame.image.load(resource_path("picts/QRcode.png"))
            screen.blit(qr_img, (395, 199))
    if page=="privacy":
        page="main"
    for e in pygame.event.get():
        

        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 3:
                o()
                ten=0
                j=0
            if e.button == 1:
                if page=="privacy":
                    page="main"
                    with open(resource_path("files/隐私确认.txt"),"w") as f:
                        pass

    pygame.display.flip()
    tick.tick(20)
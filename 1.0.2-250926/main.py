##火车票票根生成器
j=0
minus_num=20
using_QRcode = 0
using_base_pic=1

import pygame
import time,os,sys,pyperclip
bbh = "0.0.8   2025-09-18"
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
dlc.fontupload(resource_path("ttf/simsun.ttf"),13,3)
dlc.fontupload(resource_path("ttf/simsun.ttf"),29,4)
dlc.fontupload(resource_path("ttf/simhei.ttf"),26,5)
dlc.fontupload(resource_path("ttf/simsun.ttf"),22,6)
dlc.fontupload(resource_path("ttf/simhei.ttf"),20,7)
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
    if using_base_pic==1:
        screen.blit(pygame.image.load(resource_path("picts/base.png")), (0, 0))

    if page == "main":
        #pygame.draw.rect(screen, (20, 120, 213), (0,  298,600, 45)) ##底部深蓝色条带
        dlc.moutput(screen,red_code,(255,90,90),(23,12))
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
        pygame.draw.line(screen, (0, 0, 0), (260-dlc.mlength("C3895",4)//2, 80), (268+dlc.mlength("C3895",4)//2, 80), 2)
        pygame.draw.line(screen, (0, 0, 0), (268+dlc.mlength("C3895",4)//2-dlc.mlength("5",4), 75), (268+dlc.mlength("C3895",4)//2, 80), 2)
        dlc.moutput(screen,date[0]+"#3#x+=005#y+=007年#x+=005#y-=007#5"+date[1]+"#3#x+=005#y+=007月#x+=005#y-=007#5"+date[2]+"#3#x+=005#y+=007日#x+=005#y-=007#5"+date[3]+":"+date[4]+"#3#x+=005#y+=007开",(0,0,0),(25,105),255,5)
        if "号"==seat[1][-1] and j==0:
            seat[1] = seat[1][:-1]+f"#3#x+=004#y+=004号"
            j=1
        dlc.moutput(screen,"#y+=003"+seat[0]+"#3#x+=003#y+=004车#x+=003#y-=004#7"+seat[1],(0,0,0),(345,105),255,7)
        dlc.moutput(screen,"#x+=005#y+=010%一08#y-=010#x-=005￥"+money+"#3#x+=003#y+=007元",(0,0,0),(25,130),255,5)
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
        dlc.moutput(screen,seatclass,(0,0,0),(445-dlc.mlength(seatclass,11),130),255,11)
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
        dlc.moutput(screen,"|#x047#y+=010"*4,(0,0,0),(47,242),255,14)
        dlc.moutput(screen,"|#x347#y+=010"*4,(0,0,0),(347,242),255,14)

        dlc.moutput(screen,und1,(0,0,0),(200-dlc.mlength(und1,16)//2,244),255,16)
        dlc.moutput(screen,und2,(0,0,0),(200-dlc.mlength(und2,16)//2,261),255,16)

        dlc.moutput(screen,undl,(0,0,0),(22,286),255,16)
        
        if using_QRcode:
            qr_img = pygame.image.load(resource_path("picts/QRcode.png"))
            screen.blit(qr_img, (395, 199))
    if page=="privacy":
        page="main"
        
        dlc.moutput(screen,dlc.EAD_YNK("9690 79C1 653F 7B56")[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK("9690 79C1 653F 7B56")[0],num=12)//2,38),255,12)
        __="4E3A 4FDD 8BC1 6570 636E 5B89 5168 FF0C 8BF7 4ECE 0023 0052 0042 7AD9 0040 002D 7D2B 6F7C 002D 0023 0023 0023 4E0B 8F7D 5B98 65B9 7248"
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,63),255,18)
        __="70B9 51FB 8FDB 5165 7A0B 5E8F 4EE3 8868 60A8 540C 610F 4EE5 4E0B 5185 5BB9 FF1A"
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,88),255,18)
        __='0031 002E 0020 4E0D 5F97 5C06 6B64 8F66 7968 7528 4F5C 4E58 8F66 FF0C 62A5 9500 7B49 7528 9014'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,113),255,18)
        __='0032 002E 0020 4E0D 5F97 5411 522B 4EBA 51FA 552E 6B64 7A0B 5E8F 6216 5176 4F5C 54C1'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,138),255,18)
        __='0033 002E 0020 4E0D 5F97 4EE5 6B64 4F5C 54C1 505A 51FA 67D0 4E9B 8FDD 6CD5 884C 4E3A'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,163),255,18)
        __='672C 7A0B 5E8F 7531 94C1 8DEF 7231 597D 8005 81EA 53D1 5236 4F5C FF0C 5176 4F5C 54C1 82E5 53D1 751F 6CD5 5F8B 7EA0 7EB7 FF0C 4F5C 8005 6982 4E0D 8D1F 8D23'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,188),255,18)
        __='82E5 60A8 4F7F 7528 7684 662F 5B98 65B9 7A0B 5E8F FF0C 7CFB 7EDF 5C06 4E0D 4F1A 4E0A 4F20 60A8 7684 4E2A 4EBA 9690 79C1 3002'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,213),255,18)
        __='82E5 60A8 4E0D 653E 5FC3 FF0C 8BF7 65AD 7F51 4F7F 7528'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,238),255,18)
        __='611F 8C22 60A8 7684 7406 89E3 548C 652F 6301'
        dlc.moutput(screen,dlc.EAD_YNK(__)[0],(0,0,0),(270-dlc.mlength(dlc.EAD_YNK(__)[0],num=18)//2,263),255,18)
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
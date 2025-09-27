#格式："名字"：[[xmin,xmax],[ymin,ymax],type]
import pygame,math
pygame.init()
font=[]
def pd(x, y, ranges):
    return (ranges[0][0] <= x <= ranges[0][1]) and (ranges[1][0] <= y <= ranges[1][1])
def fontupload(a,size,num=0):
      global font
      if len(font)<num+1:
            for i in range(num+1-len(font)):
                  font.append(None)
      font[num]=pygame.font.Font(a,size)
      #print(font)
      return pygame.font.Font(a,size)
      
def output(screen,words='',color=(255,255,255),place=(0,0),tm=255,num=0):
      try:
            text = font[num].render(words, True, color) 
            text.set_alpha(tm)
            # 修复坐标类型问题，转换为整数元组
            screen.blit(text, place)
            return screen
      except Exception as e:
            print(e)
            #pass
      
def csckg(text,num=0,long1 = 0):
      global font
      if long1 == 0:
            try:
                  long1 = font[num].size(text)[0]
            except:
                  long1 = 1
      elif long1 == 1:
            long1 = font[num].size(text)[1]
      else:
            long1 = font[num].size(text)
      return long1
color=[]
def rgb(r,g,b):
      color.append((r,g,b))
def mouselineupload(方案):
      color=[]
      pos=[]
      for i in range(15):
            pos.append((0,0))
      if 方案==1:
            rgb(218, 62, 78)
            rgb(222, 46, 85)
            rgb(225, 23, 94)
            rgb(226, 0, 104)
            rgb(225, 0, 115)
            rgb(220, 0, 127)
            rgb(215, 0, 139)
            rgb(209, 0, 151)
            rgb(202, 0, 164)
            rgb(194, 0, 179)
            rgb(185, 0, 196)
            rgb(172, 0, 216)
            rgb(152, 0, 233)
            rgb(124, 26, 249)
      elif 方案==2:
            rgb(98, 109, 209)
            rgb(70, 121, 219)
            rgb(17, 132, 225)
            rgb(0, 142, 226)
            rgb(0, 151, 215)
            rgb(0, 158, 208)
            rgb(0, 166, 203)
            rgb(0, 173, 198)
            rgb(0, 180, 192)
            rgb(0, 188, 184)
            rgb(0, 196, 175)
            rgb(0, 202, 162)
            rgb(47, 207, 150)
            rgb(90, 211, 138)
      elif 方案==3:
            rgb(38, 192, 97)
            rgb(68, 188, 82)
            rgb(88, 183, 68)
            rgb(104, 178, 54)
            rgb(118, 173, 41)
            rgb(130, 167, 28)
            rgb(142, 161, 13)
            rgb(152, 155, 0)
            rgb(162, 149, 0)
            rgb(171, 142, 0)
            rgb(179, 135, 0)
            rgb(187, 127, 9)
            rgb(193, 120, 21)
            rgb(199, 112, 31)
      else:
            print('[red]方案错误[/red]')
pos=[]
def mouselineoutput(screen):
      del pos[0]
      pos.append(pygame.mouse.get_pos())
      for i in range(len(pos)-1):
            pygame.draw.line(screen, color[i], pos[i],pos[i+1], width=3)

def contains_profanity(text):
    fucklst=['ck','F','sb','SB','傻','煞笔','大聪明','虾','头','wx','qq','QQ','WX','id','ID','Id','微信','QQ号','微信号','QQ号码','微信号码','微信号','eggy','110','12306','666','十','灵']
    for i in fucklst:
        if i in text:
            return True
    return False

nowmusic = ""
def pdmusic(music):
    global nowmusic
    if nowmusic == music:
        return False
    else:
        nowmusic = music
        return True

def sjpd(str,str2):
      y1=str[:4] 
      y2=str2[:4]
      m1=str[5:7]
      m2=str2[5:7]
      d1=str[8:10]
      d2=str2[8:10]
      h1=str[11:13]
      h2=str2[11:13]
      mi1=str[14:16]
      mi2=str2[14:16]
      if y1>y2:
            return 1
      elif y1<y2:
            return -1
      elif m1>m2:
            return 1
      elif m1<m2:
            return -1
      elif d1>d2:
            return 1
      elif d1<d2:
            return -1
      elif h1>h2:
            return 1
      elif h1<h2:
            return -1
      elif mi1>mi2:
            return 1
      elif mi1<mi2:
            return -1
      else:
            return 0
def health_circle_jdt(screen,x,y,large,now,max,healthcolor=(255,0,0),bgcolor=(100,100,100)):
    # 处理满进度时的精度问题
    now -= 1e-19
    end_angle = math.pi*2 * (((max-now) / max) ) 
    # 调整为从底部开始顺时针增长
    pygame.draw.arc(screen, healthcolor, (x - large-10, y - large-10, (large+10)*2, (large+10)*2), 
                   math.pi/2,          # 起始角度（底部6点钟方向）
                   math.pi/2 - 1e-6,width=10)  # 结束角度（顺时针方向）
    pygame.draw.arc(screen, bgcolor, (x - large-10, y - large-10, (large+10)*2, (large+10)*2), 
                   math.pi/2,          # 起始角度（底部6点钟方向）
                   math.pi/2 + end_angle,  # 结束角度（顺时针方向）
                   width=10)
def mlength(words,num):
      x = 0
      xmax = 0
      i = 0
      colorset = ["#R","#G","#B","#Y","#W","#P","#O","#L","#D","#C","#Z"]
      while i < len(words):
            try:
                  if words[i] + words[i + 1] in colorset:
                        i += 2
                  elif words[i:i + 3] == '###':
                        i+=3
                  elif words[i] + words[i + 1] == '#y':
                        i+=6
                  elif words[i] + words[i + 1] == '#c':
                        i += 11
                  elif words[i] + words[i + 1] == '#n':
                        xmax = max(xmax,x)
                        x = 0
                        i += 2
                  elif words[i] + words[i + 1] == '#0':
                        num = 0
                        i += 2
                  elif words[i] + words[i + 1] == '#1':
                        num = 1
                        i += 2
                  elif words[i] + words[i + 1] == '#2':
                        num = 2
                        i += 2
                  elif words[i] + words[i + 1] == '#3':
                        num = 3
                        i += 2
                  elif words[i] + words[i + 1] == '#4':
                        num = 4
                        i +=  2
                  elif words[i] + words[i + 1] == '#5':
                        num = 5
                        i += 2
                  else:
                        x+=csckg(words[i],num,0)
                        i+=1
            except:
                  x+=csckg(words[i],num,0)
                  i+=1
      xmax = max(xmax,x)
      return xmax

def moutput(sc,words='',colorcs=(255,255,255),place=(0,0),tm=255,num=0):
      words=str(words)
      global screen 
      screen = sc
      x = int(place[0]) if place[0] != "#M" else (1440-mlength(words,num))//2
      y = int(place[1])
      color = colorcs
      i = 0
      yp=30
      words += "      "
      JINGp=0
      JINGp_start=-1
      while i < len(words):
            try:
                  if words[i:i + 2] == '#p':
                        JINGp=1
                        JINGp_start=i+2
                        i+=2
                        ##在剩余区域内取出第一个'#',如果没有则取出到字符串结束
                        i=words[i:].find('#')+JINGp_start+1
                        moutput(screen,EAD_YNK(words[JINGp_start:i-1])[0],color,(x,y))
                        JINGp_start=-1
                        continue
                  
                        continue
                  elif words[i:i + 4] == '#y+=':
                              y+=int(words[i+4:i+7])
                              i+=7
                  elif words[i:i + 4] == '#x+=':
                              x+=int(words[i+4:i+7])
                              i+=7
                  elif words[i:i + 4] == '#tm=':
                              tm=int(words[i+4:i+7])
                              i+=7
                  elif words[i:i + 4] == '#y-=':
                              y-=int(words[i+4:i+7])
                              i+=7
                  elif words[i:i + 4] == '#x-=':
                              x-=int(words[i+4:i+7])
                              i+=7
                  
                  elif words[i] + words[i + 1] == '#R':
                        color = (255, 0, 0)
                        i += 2
                  elif words[i] + words[i + 1] == '#G':
                        color = (0, 255, 0)
                        i += 2
                  elif words[i] + words[i + 1] == '#B':
                        color = (0, 0, 255)
                        i += 2
                  elif words[i] + words[i + 1] == '#Y':
                        color = (255, 255, 0)
                        i += 2
                  elif words[i] + words[i + 1] == '#W':
                        color = (255, 255, 255)
                        i += 2
                  elif words[i] + words[i + 1] == '#P':
                        #粉色
                        color = (255,130,104)
                        i += 2
                  elif words[i] + words[i + 1] == '#O':
                        #橙色
                        color = (255,128,0)
                        i += 2
                  elif words[i] + words[i + 1] == '#L':
                        #淡蓝色
                        color = (173,216,230)
                        i += 2
                  elif words[i] + words[i + 1] == '#D':
                        #淡紫色
                        color = (218,112,214)
                        i += 2
                  elif words[i] + words[i + 1] == '#C':
                        #淡绿色
                        color = (152,251,152)
                        i += 2
                  elif words[i] + words[i + 1] == '#Z':
                        #紫色
                        color = (255,0,255)
                        i += 2
                  elif words[i] + words[i + 1] == '#H':
                        #紫色
                        color = (120,120,120)
                        i += 2
                  elif words[i] + words[i + 1] == '#l':
                        color = (123,213,231)
                        i += 2
                  elif words[i] + words[i + 1] == '#x':
                        if words[i+2] != '+':
                              x=int(words[i+2:i+5])
                              i+=5
                        else:
                              x=int(words[i+3:i+7])
                              i+=7
                  elif words[i] + words[i + 1] + words[i+2] == '###':
                        color = colorcs
                        i += 3
                  elif words[i] + words[i + 1]== '#c':
                        color = (int (words[i + 2 : i + 5]), int (words[i + 5 : i + 8]), int (words[i + 8 : i + 11]))
                        i += 11
                  elif words[i] + words[i + 1] == '#n':
                        y+=yp
                        x=place[0]
                        i += 2
                  elif words[i] + words[i + 1] == '#y':
                        yp = int(words[i + 2 : i + 6])
                        i += 6
                  elif words[i] + words[i + 1] == '#0':
                        num = 0
                        i += 2
                  elif words[i:i + 3] == '#10':
                        num = 10
                        i += 3
                  elif words[i:i + 3] == '#11':
                        num = 11
                        i += 3
                  elif words[i:i + 3] == '#12':
                        num = 12
                        i += 3
                  elif words[i:i + 3] == '#13':
                        num = 13
                        i += 3
                  elif words[i:i + 3] == '#14':
                        num = 14
                        i += 3
                  elif words[i:i + 3] == '#15':
                        num = 15
                        i += 3
                  elif words[i:i + 3] == '#16':
                        num = 16
                        i += 3
                  elif words[i] + words[i + 1] == '#1':
                        num = 1
                        i += 2
                  elif words[i] + words[i + 1] == '#2':
                        num = 2
                        i += 2
                  elif words[i] + words[i + 1] == '#3':
                        num = 3
                        i += 2
                  elif words[i] + words[i + 1] == '#4':
                        num = 4
                        i += 2
                  elif words[i] + words[i + 1] == '#5':
                        num = 5
                        i += 2
                  elif words[i] + words[i + 1] == '#6':
                        num = 6
                        i += 2
                  elif words[i] + words[i + 1] == '#7':
                        num = 7
                        i += 2
                  elif words[i] + words[i + 1] == '#8':
                        num = 8
                        i += 2
                  elif words[i] + words[i + 1] == '#9':
                        num = 9
                        i += 2 
                  elif words[i] + words[i + 1] == '#零':
                        try:
                              pygame.draw.circle(screen, color, (int(x)+csckg("人",num)//2, int(y)+csckg("人",num,1)//2),int(words[i+2:i+5]), 2)
                        except Exception as e:
                              print(e)
                              #pygame.draw.circle(screen, color, (int(x), int(y)), (int(words[i+3:i+7]),int(words[i+3:i+7])), 1)
                        i+=5
                  
                  elif words[i] + words[i + 1] == '%一':
                        try:
                              output(screen,'一',color,(int(x),int(y)),tm,int(words[i+2:i+4]))
                              i+=4
                        except:
                              output(screen,'一',color,(int(x),int(y)),tm,num)
                              i+=2

                  elif words[i] == '$':
                        i+=1
                  
                  else:
                        output(screen,words[i],color,(int(x),int(y)),tm,num)
                        x+=csckg(words[i],num,0)
                        i+=1
            except:
                  output(screen,words[i],color,(int(x),int(y)),tm,num)
                  x+=csckg(words[i],num,0)
                  i+=1
方框提示 = []
提示 = []
flips = 0
def outputts(screen,nums):
    global flips,提示,方框提示
    flips+=0.5
    #print(提示)
    for tsnr in 提示:
        if int(flips-tsnr[1])>0:
            #print(tsnr)
            output(screen, tsnr[0], tsnr[2], ( 270 - csckg(tsnr[0],nums)//2,int((flips-tsnr[1])**0.93*-1.8+150)),255-(flips-tsnr[1])**1.12 if flips-tsnr[1] < 255 else 0,nums)#提示字符输出采用非线性移动增加美观度
    for tsnr in 提示:
         if flips-tsnr[1]>300:
             提示.remove(tsnr)
"""
    if 方框提示 != []:
        # 主框体装饰
        pygame.draw.rect(screen, (128,128,128), (290,190,500,340))  # 深红色底框
        pygame.draw.rect(screen, (178,178,198), (300,200,480,320), 4)  # 金色主框
        
        # 屋檐装饰元素
        for i in range(0, 441, 40):  # 顶部瓦当图案
            pygame.draw.polygon(screen, (178,178,198), [
                (310+i, 200), (320+i, 190), 
                (330+i, 200), (320+i, 210)
            ], 3)
        # 中间纹样分隔线
        pygame.draw.line(screen, (178,178,198), (300,260), (780,260), 2)
        pygame.draw.line(screen, (178,178,198), (300,520-40), (780,520-40), 2)
        fontupload("files/0.ttf", 31,1)
        output(screen, 方框提示[0], (255,0,0), (int(540 - csckg(方框提示[0],1))//2,200),235,1)
        output(screen, "退出提示", (15,180,70), (493,482),235,1)
        moutput(screen, 方框提示[1], (0,0,0), ((320,300)),215,1)#moutput()函数在output()函数的基础上增加了便捷改色和换行等功能，可以直接使用
        
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif el.type == pygame.KEYDOWN:
                if el.key == pygame.K_ESCAPE:
                    方框提示 = []
            elif el.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                if pd(mousex,mousey,[[0,1080],[480,520]]) or not(pd(mousex,mousey,[[300,780],[260,520]])):
                    方框提示 = []
"""
def addts(text='',pos_flips=None,color=(128,0,255)):
      global 提示,flips
      if pos_flips == None:
            pos_flips = flips
      提示.append([text,pos_flips,color])
      #print(提示)
"""
def addtsbox(text,text2):#text2可含各类快捷控制字符
      global 方框提示
      方框提示.append(text)
      方框提示.append(text2)
"""
def text_output_yes():
      print("连接完成")


def encode_to_unicode(text):
    """将文本编码为Unicode十六进制表示"""
    result = []
    for char in text:
        # 获取字符的Unicode编码并格式化为4位十六进制（大写）
        hex_code = format(ord(char), '04X')
        result.append(hex_code)
    return ' '.join(result)

def decode_from_unicode(hex_str):
    """将Unicode十六进制表示解码为文本"""
    # 分割十六进制字符串
    hex_codes = hex_str.split()
    result = []
    for hex_code in hex_codes:
        # 将十六进制转换为整数，然后转换为字符
        char = chr(int(hex_code, 16))
        result.append(char)
    return ''.join(result)

def EAD_YNK(user_input):
      user_input = user_input.strip()
      
      if not user_input:
            
            return "输入不能为空",''
    
      # 尝试解码
      try:
            # 检查输入是否可能是Unicode编码（包含空格分隔的十六进制数）
            if ' ' in user_input or len(user_input) >= 4:
                  decoded = decode_from_unicode(user_input)

                  
                  # 对解码结果进行编码
                  encoded = encode_to_unicode(user_input)

            else:
                  # 如果输入很短且没有空格，可能是单个字符
                  # 尝试将其视为十六进制编码
                  decoded = chr(int(user_input, 16))

                  
                  # 对解码结果进行编码
                  encoded = encode_to_unicode(user_input)

      
      except:
            decoded ="ERR"
            encoded = encode_to_unicode(user_input)
      return decoded , encoded

	




if __name__ == "__main__":
      fontupload("ttf/simw.ttf",17)
      print(mlength("B站<紫潼>独立制作，完全免费",num=0))
      while 1:
            print(EAD_YNK(input()))
import random
# import pyperclip
from rpze.basic.inject import InjectedGame,ConnectedContext
from rpze.iztest.operations import enter_ize
from rpze.structs.game_board import get_board
from rpze.structs.plant import PlantType
from rpze.iztest.plant_modifier import set_puff_x_offset
from rpze.rp_extend import HookPosition
def ROW(s):
    ans=(ord(s)-65)//5
    return ans#读取某个植物的行数
def COL(s):
    ans=(ord(s)-65)%5
    return ans#读取某个植物的列数
R=((8,8,8,8,8,8,8,8,3,22,4,6,6,0,28,34,18,5,17,10,37,29,31,21,21),#综合
   (8,8,8,8,8,8,8,8,22,28,28,28,7,34,34,34,18,5,5,5,37,31,21,21,21),#控制
   (8,8,8,8,8,8,8,8,4,4,4,4,6,6,6,17,17,17,10,10,10,10,21,21,21),#即死
   (8,8,8,8,8,8,8,8,5,5,5,5,5,5,5,5,5,28,28,28,28,7,7,7,7),#输出
   (8,8,8,8,8,8,8,8,4,4,4,4,4,4,4,4,4,6,6,6,6,6,6,6,6),#爆炸
   (8,8,8,8,8,8,8,8,21,21,21,21,21,21,21,21,21,29,29,29,29,29,29,29,29),#倾斜
   (8,8,8,8,8,8,8,8,10,10,10,10,10,10,10,10,10,31,31,31,31,31,31,31,31),#穿刺
   (8,8,8,8,8,8,8,8,13,13,13,13,13,13,13,13,13,13,13,13,1,1,1,1,1))#回复
#如控制，其植物顺序为（小喷*8，火树*1，裂荚*3，双发*1，玉米*3，三线*1，冰豆*3，伞叶*1，磁铁*1，地刺*3）
#前八个植物统一为小喷，在布阵时改为小向
A=(0,0,0,1,1,2)#A类阵的概率
B=(3,4,5,6,7)#B类阵的概率
Y=(A,A,A,A,B)#主题概率
Min=(8,7,4,4,3,3,2,2,2,2)#花数下限
Max=(8,7,6,5,5,5,4,4,4,4)#花数上限
Dresscircle=[2,3,4,7,8,9,12,13,14,17,18,19,22,23,24]#前三列，即坚果和火树合规位
Joke=('FGKLPQUWEDTIORMYNXJSBVACH','DFGLMPQUCRVWSOTXEHINBAJKY','BCDEVWXYKLMNFGHPQRIJOTASU','ABFGKLPQEJOTUVWXYCHMRDINS',\
      'ABCDUVWXEJKLMNOTYFGHIPQRS','ABKLPQUVFGHIJMRSTCDENOWXY','ABCDEFGHMNORSTWXYIJKLPQUV','ABFGPQUVCDEHIJRSTWXYKLMNO')
Score=[0,0,0,-0.5,0,0.75,0.25,6.75]
while True:
    print('扣1生成自然布阵码，扣2生成整活布阵码，扣0开始冲关！')
    firstinput=input()
    if firstinput=='1' or firstinput=='2':
        print('你想打几关？（请输入一个1——100的整数）')
        wantstreak=input()
        try:
            int(wantstreak)
            S=''#以下为布阵的代码
            if firstinput=='2':
                print('是否锁定主题？0综合，1控制，2即死，3输出，4爆炸，5倾斜，6穿刺，7回复。其他任意键不锁定。')
                themeinput=input()
                print('是否锁定花数？0锁定最小花数（地狱模式），1锁定最大花数（零度模式）。其他任意键不锁定。')
                flowerinput=input()
                print('是否锁定最优开局？0开启。其他任意键不锁定。')
                placeinput=input()
                print('是否锁定小喷偏移？0~9开启对应偏移。其他任意键不锁定。')
                puffinput=input()
            for i in range(0,int(wantstreak)):#对于关卡数的循环
                if i==0:#确定主题
                    theme=random.choice(A)#第一关必定为A类阵，在三个主题中按概率取随机
                else:
                    theme=random.choice(random.choice(Y))#之后的关卡，AB八二开取随机，确定AB后再按概率确定主题
                if firstinput=='2':
                    if themeinput in ['0','1','2','3','4','5','6','7']:
                        theme=int(themeinput)
                    else:
                        pass
                if i<10:
                    flowernum=random.randint(Min[i],Max[i])#前十关确定花数，在花数下限和上限间取随机
                else:
                    flowernum=random.randint(1,3)#十关后确定花数
                if firstinput=='2':
                    if flowerinput=='0':
                        if i<10:
                            flowernum=Min[i]
                        else:
                            flowernum=1
                    elif flowerinput=='1':
                        if i<10:
                            flowernum=Max[i]
                        else:
                            flowernum=3
                    else:
                        pass
                Vacant=list(range(0,25))#空位表，如0是0-0，4是4-0，18是3-3等
                Place=[]#植物位置表，对应方法同空位
                for j in range(0,8):#对于空位的循环
                    m=random.choice(Vacant)#从场上空位中随机挑一个，记为m
                    Place.append(m)#将m扔进植物顺序中
                    Vacant.remove(m)#将m从空位中删除，下同
                if theme==0:
                    m=random.choice(list(set(Vacant)&set(Dresscircle)))#为保证火树和坚果合规，原本的空位改为空位与前三列的交集
                    Place.append(m)
                    Vacant.remove(m)
                    m=random.choice(list(set(Vacant)&set(Dresscircle)))#综合执行两次
                    Place.append(m)
                    Vacant.remove(m)
                elif theme==1:
                    m=random.choice(list(set(Vacant)&set(Dresscircle)))#控制执行一次，其余不执行
                    Place.append(m)
                    Vacant.remove(m)
                while Vacant!=[]:
                    m=random.choice(Vacant)
                    Place.append(m)
                    Vacant.remove(m)
                X=str(theme)+str(flowernum)#布阵码前两位为主题（0综合，1控制，2即死，3输出，4爆炸，5倾斜，6穿刺，7回复）和花数（1-8）
                if firstinput=='2':
                    if placeinput=='0' and i==0:
                        X=X+Joke[theme]
                    else:
                        for j in range(0,25):
                            X=X+str(chr(Place[j]+65))
                else:
                    for j in range(0,25):
                        X=X+str(chr(Place[j]+65))#将布阵码的植物位置部分转为大写字母，利于字符串的读写
                for j in range(0,8-flowernum):
                    puffexcursion=random.randint(0,9)#设置小喷横偏移，0表示偏移量-5，9表示+4
                    if firstinput=='2':
                        if puffinput in ['0','1','2','3','4','5','6','7','8','9']:
                            puffexcursion=int(puffinput)
                        else:
                            pass
                    X=X+str(puffexcursion)
                S=S+X+'.'#隔开每一关方便读写
            S=S+'HOOCCOOH'#草酸，防伪标志，灵魂
            print(S)
            print('已复制至剪贴板！')
            # pyperclip.copy(S)
        except ValueError:
            print('输入不合法！')
            continue
    elif firstinput=='0':
        print('请复制布阵码！')
        W=input()
        if W.find('.HOOCCOOH')==-1:
            print('输入不合法！请检查！')
        else:
            P=[]
            while W[1]!='O':
                P.append(W[0:35-int(W[1])])
                W=W[36-int(W[1]):]#将布阵码逐关分割
            with InjectedGame(r"D:\桌面\pvz\pvz_v1.0.0.1051_EN\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe",False) as game:
                ctler=game.controller
                ctler.open_hook(HookPosition.CHALLENGE_I_ZOMBIE_SCORE_BRAIN)#禁止游戏自然生成关卡
                enter_ize(ctler)
                board=get_board(ctler)
                ctler.write_i32(True, 0x6a9ec0, 0x768 ,0x55f1)
                flag=-1
                with ConnectedContext(ctler):
                    while True:
                        if ctler.read_i32(0x6a9ec0, 0x768, 0x160, 0x6c)!=flag:
                            sun=ctler.read_i32(0x6a9ec0, 0x768, 0x5560)
                            flag=ctler.read_i32(0x6a9ec0, 0x768, 0x160, 0x6c)
                            if flag==0:
                                score=74.25
                            elif flag==1:
                                score=72.25
                            else:
                                score=score+int(L[1])+Score[int(L[0])]+(s-sun)/200-3.75
                            print('已通过',flag,'关，阳光',sun,'，算分',score,'！')
                            L=P[flag]
                            U=list(R[int(L[0])])
                            s=sun
                            for i in range(0,int(L[1])):
                                U[i]=1#改小喷为小向
                            #for plant in~board.plant_list:
                                #plant.die()#清除植物，为方便跳关预览用，本身不必要
                            #ctler.skip_frames()
                            for i in range(0,25):
                                n=board.iz_new_plant(ROW(L[i+2]),COL(L[i+2]),U[i])
                                if i in range(int(L[1]),8):
                                    set_puff_x_offset(n,int(L[34-i])-5)#设置小喷偏移
                        #else:
                         #   ctler.skip_frames()#丑陋的死循环，检测过关的扳机

    else:
        print('输入不合法，请再试一次！')

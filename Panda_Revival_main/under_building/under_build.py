#地下建築のルール
#基準座標はエリアのx,zが最小になる位置にする.(その方がやりやすい)
#y座標は床が0になる位置にする.
#transformを利用し,移動させる
#処理順
#各建築物関数→基準作成→各建築物の実体

from gdpc import Editor, Block, geometry, Transform
from under_building.Block_check import block_check,colored
import time
import random


def base_transform(coor,base_coor,rotation):
    #用途:基本座標を回転を加味して移動させる.
    #Minecraft座標系の移動
    #move_coor:eastを向いている時の座標の移動値
    trans_coor=[0,0,0]
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]

    trans_coor[0]=base_coor[0]+x
    trans_coor[1]=base_coor[1]+y
    trans_coor[2]=base_coor[2]+z

    return trans_coor


def under_build_base(editor,coor,rotation,size,wall_Block = "stone"):
    #用途:エリアのぶち抜きと壁の作成
    #coor:基準座標 coor=[x,y,z]
    #rotation:向き,transformに使用
    #size:エリアの大きさを格納した変数 size=[x,y,z]
    #wall_block:壁の材質(変更したい場合のみ入力)
    #道は後で作るので気にしない
    #方策:石で埋めて,空間を確保
    
    
    geometry.placeCuboid(editor,[-1 ,0,-1],[size[0],size[1]+2,size[2]],Block(wall_Block))
    geometry.placeCuboid(editor,[0 ,1,0],[size[0]-1,size[1],size[2]-1],Block("air"))

def fix_rotation(b_lota,c_lota):
    #用途:b_lota(建築に使用する方角)とc_lota(コマンドに使用する方角)を修正する
    #回転数を加算
    templota=b_lota+c_lota
    c_lota=templota%4
    return c_lota

def place_frame(editor,coor,base_coor,rotation,direction,item):
    #用途:フレームの設置
    #direction:向き(NASWで入力)
    #rotation:設置系の向き

    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"
    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"): #右向き
            place_dire=3 
        elif(direction=="west"): #後ろ向き
            place_dire=4 
        elif(direction=="north"): #左向き
            place_dire=2 
        elif(direction=="east"): #正面
            place_dire=5 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):#右向き
            place_dire=4 
        elif(direction=="west"):#後ろ向き
            place_dire=2 
        elif(direction=="north"):#左向き
            place_dire=5 
        elif(direction=="east"):#正面
            place_dire=3 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):
            place_dire=2 
        elif(direction=="west"):
            place_dire=5 
        elif(direction=="north"):
            place_dire=3 
        elif(direction=="east"):
            place_dire=4 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=5
        elif(direction=="west"):
            place_dire=3
        elif(direction=="north"):
            place_dire=4
        elif(direction=="east"):
            place_dire=2
    if item:
        NBT=f"{{Facing:{place_dire},Item:{{id:{item}}}}}"
    else:
        NBT=f"{{Facing:{place_dire}}}"

    editor.runCommand(f"summon item_frame {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")

def place_stand(editor,coor,base_coor,rotation,direction,boots="",leggings="",chestplate="",helmet=""):
    #用途:アーマースタンドの設置
    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"

    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"): #右向き
            place_dire=0 
        elif(direction=="west"): #後ろ向き
            place_dire=90  
        elif(direction=="north"): #左向き
            place_dire=180 
        elif(direction=="east"): #正面
            place_dire=-90 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):
            place_dire=90 
        elif(direction=="west"):
            place_dire=180 
        elif(direction=="north"):
            place_dire=-90 
        elif(direction=="east"):
            place_dire=0 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):#右向き
            place_dire=180 
        elif(direction=="west"):#後ろ向き
            place_dire=-90 
        elif(direction=="north"):#左向き
            place_dire=0 
        elif(direction=="east"):#正面
            place_dire=90 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=-90 #west
        elif(direction=="west"):
            place_dire=0 #north
        elif(direction=="north"):
            place_dire=90 #east
        elif(direction=="east"):
            place_dire=180 #south

    if boots:
        boots=f"id:\"{boots}\",Count:1b"
    if leggings:
        leggings=f"id:\"{leggings}\",Count:1b"
    if chestplate:
        chestplate=f"id:\"{chestplate}\",Count:1b"
    if helmet:
        helmet=f"id:\"{helmet}\",Count:1b"
    NBT=f"{{Rotation:[{place_dire}f,0f],ArmorItems:[{{{boots}}},{{{leggings}}},{{{chestplate}}},{{{helmet}}}]}}"
    #print(NBT)
    editor.runCommand(f"summon armor_stand {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")


def place_frame_up(editor,coor,base_coor,rotation,item,inv=False):
    #用途:フレームの設置
    #direction:向き(NASWで入力)
    #rotation:設置系の向き
    #上方向へ設置.
    #inv:透明化
    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"
    place_dire=1
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
    if item:
        if inv:
            NBT=f"{{Facing:{place_dire},Item:{{id:{item}}},Invisible:1b}}"
        else:
            NBT=f"{{Facing:{place_dire},Item:{{id:{item}}}}}"
    else:
        if inv:
            NBT=f"{{Facing:{place_dire},Invisible:1b}}"
        else:
            NBT=f"{{Facing:{place_dire}}}"
    editor.runCommand(f"summon item_frame {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")



def place_door(editor,coor,facing,hinge,types="birch"):
    #用途:ドアの設置
    #typeには材質をいれる
    block_type=types+"_door"
    data_low=Block(block_type,{"facing":facing,"half":"lower","hinge":hinge})
    data_up=Block(block_type,{"facing":facing,"half":"upper","hinge":hinge})
    editor.placeBlock(coor,data_low)
    editor.placeBlock([coor[0],coor[1]+1,coor[2]],data_up)

def place_bed(editor,coor,facing,color="red"):
    #用途:ベッドの設置
    #coorは足側を入力する
    #facing=ベット自体の向き

    bed_color=color+"_bed"
    x=0
    z=0
    if(facing=="south"): #右向き
        z=1
    elif(facing=="west"): #後ろ向き
        x=-1
    elif(facing=="north"): #左向き
        z=-1
    elif(facing=="east"): #正面
        x=1

    editor.placeBlock(coor,Block(bed_color,{"facing":facing,"part":"foot"}))
    editor.placeBlock([coor[0]+x,coor[1],coor[2]+z],Block(bed_color,{"facing":facing,"part":"head"}))

def place_pot(editor,coor,content="none"):
    #content:中身
    if(content != "none"):
        block="potted_"+content
    else:
        block="flower_pot"
    editor.placeBlock(coor,Block(block))


def place_paint(editor,coor,base_coor,rotation,direction,name):
    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"):
            place_dire=0 
        elif(direction=="west"):
            place_dire=1 
        elif(direction=="north"):
            place_dire=2 
        elif(direction=="east"):
            place_dire=3 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):
            place_dire=1 
        elif(direction=="west"):
            place_dire=2 
        elif(direction=="north"):
            place_dire=3 
        elif(direction=="east"):
            place_dire=0 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):
            place_dire=2 
        elif(direction=="west"):
            place_dire=3 
        elif(direction=="north"):
            place_dire=0 
        elif(direction=="east"):
            place_dire=1 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=3
        elif(direction=="west"):
            place_dire=0
        elif(direction=="north"):
            place_dire=1
        elif(direction=="east"):
            place_dire=2

    editor.runCommand(f"summon painting {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {{facing:{place_dire},variant:{name}}}")




def place_frame(editor,coor,base_coor,rotation,direction,item):
    #用途:フレームの設置
    #direction:向き(NASWで入力)
    #rotation:設置系の向き

    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"
    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"): #右向き
            place_dire=3 
        elif(direction=="west"): #後ろ向き
            place_dire=4 
        elif(direction=="north"): #左向き
            place_dire=2 
        elif(direction=="east"): #正面
            place_dire=5 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):#右向き
            place_dire=4 
        elif(direction=="west"):#後ろ向き
            place_dire=2 
        elif(direction=="north"):#左向き
            place_dire=5 
        elif(direction=="east"):#正面
            place_dire=3 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):
            place_dire=2 
        elif(direction=="west"):
            place_dire=5 
        elif(direction=="north"):
            place_dire=3 
        elif(direction=="east"):
            place_dire=4 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=5
        elif(direction=="west"):
            place_dire=3
        elif(direction=="north"):
            place_dire=4
        elif(direction=="east"):
            place_dire=2
    if item:
        NBT=f"{{Facing:{place_dire},Item:{{id:{item}}}}}"
    else:
        NBT=f"{{Facing:{place_dire}}}"

    editor.runCommand(f"summon item_frame {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")


def summon_animal(editor,coor,base_coor,rotation,animal,name=False):
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
    if(name==False):
        editor.runCommand(f"summon {animal} {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z}")
    elif(name=="panda"):
        panda_name=panda_name_list()
        editor.runCommand(f"summon {animal} {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {{CustomName:{panda_name}}}")
    else:
        editor.runCommand(f"summon {animal} {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {{CustomName:{name}}}")

    
def panda_name_list():
    #用途:パンダの名前を渡す

    panda_name_list=["Meilin","Xiaobo","Baozi","Lingling","Xuebao","Zhuzhu","Lianhua","Feifei","Haitao","Qiqi",
    "Yuelong","Meifeng","Xiaotao","Shuangshuang","Huahua","Zhenzhen","Dongmei","Huanhuan","Longwei","Yinyin",
    "Xiangxiang","Tianbao","Nianzu","Lanlan","Chunhua","Guangli","Pingping","Rongrong","Mingliang","Yunbao",
    "Zhaozhao","Haoran","Fengyi","Qiaoqiao","Jingjing","Xinxin","Lulu","Changle","Ruomei","Boqin"]

    panda_name=random.choice((panda_name_list))
    return panda_name
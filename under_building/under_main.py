#考え方
#都市の中心(建築エリアの中心ではない)から,建築マップの中央方向に向けて階段掘り
#地下建築の中央エリアのため,適応性を多少無視して建築する

from gdpc import Editor, Block, geometry, Transform
from Block_check import block_check,colored
import time
from under_base import under_basement

editor=Editor(buffering=True,bufferLimit=1024)


#座標系

XS=900
YS=0
ZS=900
XL,YL,ZL=128,256,128
coor_basis=[XS,YS,ZS]

command_build_area= f"setbuildarea {XS} {-64} {ZS} {XS+XL} {YS+YL} {ZS+ZL}"

editor.runCommand(command_build_area)
worldSlice = editor.loadWorldSlice()




def main_shaft_part(editor,coor,height):
    stairsBlock = Block("cobblestone_stairs", {"facing": "west", "half": "bottom","waterlogged":"false"})
    #トロッコを通すよう
    editor.placeBlock([0+coor[0],-2+coor[1],-3],Block("stone"))
    #階段本体
    geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-2),(0+coor[0],-1+coor[1],3),stairsBlock)
    geometry.placeCuboid(editor,(0+coor[0],0+coor[1],-3),(0+coor[0],height+coor[1],3),Block("air"))
    geometry.placeCuboid(editor,(0+coor[0],height+coor[1],-3),(0+coor[0],height+coor[1],3),Block("stone"))

def main_shaft_wall(editor,coor,height,torch_count):
    log_block_y=Block("spruce_log", {"axis": "y"})
    log_block_z=Block("spruce_log", {"axis": "z"})
    geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-4),(0+coor[0],height+coor[1],-4),Block("stone"))
    geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],4),(0+coor[0],height+coor[1],4),Block("stone"))
    if(torch_count%4 ==0):
        editor.placeBlock([0+coor[0],1+coor[1],-3],Block("wall_torch",{"facing":"south"}))
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-4),(0+coor[0],height+coor[1],-4),log_block_y)
        editor.placeBlock([0+coor[0],1+coor[1],3],Block("wall_torch",{"facing":"north"}))
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],4),(0+coor[0],height+coor[1],4),log_block_y)
        geometry.placeCuboid(editor,(0+coor[0],height+coor[1],-3),(0+coor[0],height+coor[1],3),log_block_z)


def main_shaft_floar(editor):
    geometry.placeCuboid(editor,(-1,-1,-3),(-3,-1,3),Block("polished_diorite"))

def main_shaft_rail_floar(editor):
    editor.placeBlock([-1,0,-3],Block("powered_rail",{"shape":"east_west"}))
    editor.placeBlock([-3,0,-3],Block("stone"))
    editor.placeBlock([-2,0,-3],Block("powered_rail",{"shape":"east_west"}))
    editor.placeBlock([-3,1,-3],Block("birch_button",{"face":"floor","facing":"west"}))

def main_shaft_rail(editor,boost_count):
    if(boost_count%3==1):
        editor.placeBlock([0+coor[0],-1+coor[1],-3],Block("powered_rail",{"shape":"ascending_west"}))
        editor.placeBlock([0+coor[0],-2+coor[1],-3],Block("stone"))
        editor.placeBlock([0+coor[0],-4+coor[1],-3],Block("stone"))
        editor.placeBlock([-1+coor[0],-3+coor[1],-3],Block("stone"))
        editor.placeBlock([1+coor[0],-3+coor[1],-3],Block("stone"))
        editor.placeBlock([0+coor[0],-3+coor[1],-4],Block("stone"))
        editor.placeBlock([0+coor[0],-3+coor[1],-2],Block("stone"))
        editor.placeBlock([0+coor[0],-3+coor[1],-3],Block("redstone_torch"))
    else:
        editor.placeBlock([0+coor[0],-1+coor[1],-3],Block("rail",{"shape":"ascending_west"}))

def under_center_base_air(editor,coor,size):
    z_size=size[2]//2

    geometry.placeCuboid(editor,(0+coor[0]+1 ,0+coor[1]-1,-z_size),(0+coor[0]+size[0]+1,coor[1]+size[1],z_size),Block("air"))


def under_center_base_frame(editor,coor,size):
    z_size=size[2]//2
    geometry.placeCuboid(editor,(0+coor[0] ,0+coor[1]-2,-z_size-1),(0+coor[0]+size[0]+2,coor[1]+size[1]+2,z_size+1),Block("stone"))




SEA_LEVEL=62#海抜の高さ
DEEP_LAYER=-20#深層岩の出現する高さ (y=8)


city_center=[1000,173,1000] #一時的に決定.

#一応city_centerがbuild_area内にあるかの確認.多分最終的にはいらない

if(coor_basis[0] > city_center[0] or coor_basis[0]+XL< city_center[0] or 
   coor_basis[2] > city_center[2] or coor_basis[2]+ZL< city_center[2]):
    print("center is not in build area")
    exit()

map_center=[XS+XL/2,SEA_LEVEL,ZS+ZL/2] #マップの中央部分.Y座標は使わないけれど取得方法に注意する

#方向と距離の取得
under_xl=map_center[0]-city_center[0]
under_zl=map_center[2]-city_center[2]

#トンネルを掘る方向の決定. 入口からトンネル方向を向いた時の方角

if(abs(under_xl) >= abs(under_zl)):
    if(under_xl >= 0):
        tunnel_direction= 0 #"east"
    else:
        tunnel_direction= 2 #"west"
else:
    if(under_zl >= 0):
        tunnel_direction= 3 #"south"
    else:
        tunnel_direction= 1 #"north"

#坑道の掘り方
#1*5マスで掘る
#高さ:床面(1):階段 2-4空気 5:石

block_check(city_center,"red")
rotation=tunnel_direction
transform=Transform(translation=city_center, rotation=rotation)
editor.transform.push(transform)
coor=[0,0,0]
main_shaft_floar(editor)
main_shaft_rail_floar(editor)


stairs_count=50
size=[13,7,13]
height=6
for i in range(stairs_count):
    if(i==stairs_count-1): #処理が最後なら部屋を作る
        under_center_base_frame(editor,coor,size)
        under_center_base_air(editor,coor,size)
    main_shaft_part(editor,coor,height)
    main_shaft_wall(editor,coor,height,i)
    main_shaft_rail(editor,i)
    coor[0]+=1
    coor[1]-=1
print(coor)

coor[2]=coor[2]-6

under_basement(editor,coor,0,[29,10,13])

#一層建築物の設置
#とりあえずbaseの設置
#向きに注意



editor.transform.pop(transform)

editor.flushBuffer()



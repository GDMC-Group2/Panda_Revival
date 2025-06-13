#考え方
#都市の中心(建築エリアの中心ではない)から,建築マップの中央方向に向けて階段掘り
#地下建築の中央エリアのため,適応性を多少無視して建築する


#単体実行時読み込みファイル(技術的限界)
from gdpc import Editor, Block, geometry, Transform
from under_building.Block_check import block_check,colored
from under_building.under_build import base_transform,fix_rotation
from under_building.under_base import under_basement
from under_building.under_city import under_city
from under_building.under_farm import under_farm_big
from under_building.under_plantation import under_plantation
from under_building.under_bamboo_farm import under_bamboo_farm
from under_building.warehouse import Warehouse
from under_building.under_barrack import under_barrack
from under_building.under_blacksmith import under_blacksmith

#


def main_shaft_part(editor,coor,height):
    stairsBlock = Block("cobblestone_stairs", {"facing": "west", "half": "bottom","waterlogged":"false"})
    #トロッコを通すよう
    #editor.placeBlock([0+coor[0],-2+coor[1],-3],Block("stone"))
    #階段本体
    geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-3),(0+coor[0],-1+coor[1],3),stairsBlock)
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

def main_shaft_entrance_part(editor,coor):
    y_max=-2
    stairsBlock = Block("cobblestone_stairs", {"facing": "west", "half": "bottom","waterlogged":"false"})
    geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-3),(0+coor[0],-1+coor[1],3),stairsBlock)
    geometry.placeCuboid(editor,(0+coor[0],0+coor[1],-3),(0+coor[0],y_max,3),Block("air"))


def main_shaft_entrance_wall(editor,coor,torch_count):
    log_block_y=Block("spruce_log", {"axis": "y"})
    y_max=-3
    if(torch_count>2):
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-4),(0+coor[0],y_max,-4),Block("stone"))
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],4),(0+coor[0],y_max,4),Block("stone"))
    if(torch_count%4 == 0 and torch_count != 0):
        editor.placeBlock([0+coor[0],1+coor[1],-3],Block("wall_torch",{"facing":"south"}))
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],-4),(0+coor[0],y_max,-4),log_block_y)
        editor.placeBlock([0+coor[0],1+coor[1],3],Block("wall_torch",{"facing":"north"}))
        geometry.placeCuboid(editor,(0+coor[0],-1+coor[1],4),(0+coor[0],y_max,4),log_block_y)


def main_shaft_entrance_deco(editor):
    geometry.placeCuboid(editor,(1,-3,-4),(8,-3,-4),Block("red_concrete"))
    geometry.placeCuboid(editor,(1,-3,4),(8,-3,4),Block("red_concrete"))
    geometry.placeCuboid(editor,(1,-2,-4),(7,-2,-4),Block("birch_fence"))
    geometry.placeCuboid(editor,(1,-2,4),(7,-2,4),Block("birch_fence"))


def main_shaft_floar(editor):
    geometry.placeCuboid(editor,(-1,-1,-3),(-3,-1,3),Block("polished_diorite"))

def main_shaft_rail_floar(editor):
    editor.placeBlock([-1,0,-3],Block("powered_rail",{"shape":"east_west"}))
    editor.placeBlock([-3,0,-3],Block("stone"))
    editor.placeBlock([-2,0,-3],Block("powered_rail",{"shape":"east_west"}))
    editor.placeBlock([-3,1,-3],Block("birch_button",{"face":"floor","facing":"west"}))

def main_shaft_rail(editor,coor,boost_count):
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




def under_main(editor,city_center):

    #想定していた決定方法
    
    # map_center=[XS+XL/2,62,ZS+ZL/2] #マップの中央部分.Y座標は使わないけれど取得方法に注意する

    # #方向と距離の取得
    # under_xl=map_center[0]-city_center[0]
    # under_zl=map_center[2]-city_center[2]

    # #トンネルを掘る方向の決定. 入口からトンネル方向を向いた時の方角

    # if(abs(under_xl) >= abs(under_zl)):
    #     if(under_xl >= 0):
    #         tunnel_direction= 0 #"east"
    #     else:
    #         tunnel_direction= 2 #"west"
    # else:
    #     if(under_zl >= 0):
    #         tunnel_direction= 3 #"north"
    #     else:
    #         tunnel_direction= 1 #"south"



    #今回は北向きに固定する
    tunnel_direction=3
    #坑道の掘り方
    #1*5マスで掘る
    #高さ:床面(1):階段 2-4空気 5:石


    #block_check(city_center,"red")
    rotation=tunnel_direction
    
    #with内部のrotationは,引継ぎが発生する
    #基準向きから見てどちらかで考える

    with editor.pushTransform(Transform(city_center,rotation=rotation)):
        coor=[0,0,0]
        base_coor=[0,0,0]
        #main_shaft_floar(editor)
        #main_shaft_rail_floar(editor)


        stairs_count=50
        size=[13,7,13]
        height=6

        for i in range(stairs_count):
            # if(i==stairs_count-1): #処理が最後なら部屋を作る
            #     under_center_base_frame(editor,coor,size)
            #     under_center_base_air(editor,coor,size)
            if(i>8):
                main_shaft_part(editor,coor,height)
                main_shaft_wall(editor,coor,height,i)
            else:
                main_shaft_entrance_part(editor,coor)
                main_shaft_entrance_wall(editor,coor,i)
            coor[0]+=1
            coor[1]-=1
        coor[2]=coor[2]-6
        main_shaft_entrance_deco(editor)

        base_coor=base_transform(coor,city_center,rotation)
        b_rota=0
        c_rota=fix_rotation(b_rota,rotation)
        under_basement(editor,coor,base_coor,b_rota,c_rota,[29,10,13])

        #一層建築物の設置
        #とりあえずbaseの設置
        #向きに注意
        #決定論で作る
        base_coor=base_transform([49,-49,0],city_center,rotation)
        base_rota=0
        c_rota=fix_rotation(base_rota,rotation)
        set_under_first(editor,[49,-49,0],base_coor,base_rota,c_rota)

        #2階部分(city)の設置
        coor[0]=93
        coor[1]=-69
        coor[2]=-58


        base_coor=base_transform(coor,city_center,rotation)
        base_rota=0
        c_rota=fix_rotation(base_rota,rotation)
        #print(base_coor)
        under_city(editor,coor,base_coor,base_rota,c_rota)
        editor.flushBuffer()

def set_under_first(editor,coor,base_coor,base_rota,rotation):
    #用途 基準位置のbaseの[0,1,6]に移動,1層の設計を行う
        with editor.pushTransform(Transform(coor,rotation=base_rota)):
            base_coor_farm=base_transform([0,-1,13],base_coor,rotation)
            b_rota=0
            c_rota=fix_rotation(b_rota,rotation)
            under_farm_big(editor,[0,-1,13],base_coor_farm,b_rota,c_rota)
            build_tunnel(editor,[8,0,7],1,5) 

            base_coor_plan=base_transform([21,-1,50],base_coor,rotation)
            b_rota=1
            c_rota=fix_rotation(b_rota,rotation)
            under_plantation(editor,[21,-1,50],base_coor_plan,b_rota,c_rota)
            build_tunnel(editor,[16,0,41],1,8)

            base_coor_bamboo=base_transform([39,-1,21],base_coor,rotation)
            b_rota=0
            c_rota=fix_rotation(b_rota,rotation)
            under_bamboo_farm(editor,[39,-1,21],base_coor_bamboo,b_rota,c_rota)
            build_tunnel(editor,[28,0,26],0,10)

            base_coor_ware=base_transform([-22,-1,22],base_coor,rotation)
            b_rota=2
            c_rota=fix_rotation(b_rota,rotation)
            Warehouse(editor,-22,-1,24,base_coor_ware,b_rota,c_rota)
            build_tunnel(editor,[-1,0,25],2,7)

            base_coor_barrack=base_transform([6,-1,-20],base_coor,rotation)
            b_rota=3
            c_rota=fix_rotation(b_rota,rotation)
            under_barrack(editor,[6,-1,-20],base_coor_barrack,b_rota,c_rota)
            build_tunnel(editor,[6,0,-7],3,12)

            base_coor_smith=base_transform([7,-1,-37],base_coor,rotation)
            b_rota=3
            c_rota=fix_rotation(b_rota,rotation)
            under_blacksmith(editor,[7,-1,-37],base_coor_smith,b_rota,c_rota)
            build_tunnel(editor,[12,0,-32],3,4) 


def build_tunnel(editor,coor,rotation,length):
    #用途:道の作成
    with editor.pushTransform(Transform(coor,rotation=rotation)):
        #トンネルの左下を基準にする
        geometry.placeCuboid(editor,[1,0,-1],[length,2,-3],Block("stone"))
        geometry.placeCuboid(editor,[1,0,3],[length,2,5],Block("stone"))
        geometry.placeCuboid(editor,[1,3,0],[length,4,2],Block("stone"))
        geometry.placeCuboid(editor,[1,-1,0],[length,-1,2],Block("stone"))
        geometry.placeCuboid(editor,[0,0,0],[length,2,2],Block("air"))
        for i in range(length):
            if(i!=0 and i%3==0):
                editor.placeBlock([i,1,3],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
                editor.placeBlock([i,1,4],Block("torch"))
                editor.placeBlock([i,1,-1],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
                editor.placeBlock([i,1,-2],Block("torch"))










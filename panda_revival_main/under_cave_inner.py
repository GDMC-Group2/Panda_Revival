#洞窟内の整備処理
#道を引く方法
#

#
#box_build_cave_mapに松明の設置+鉱石の設置
#5*5の大きさがあれば,休憩所を設置
from gdpc import Editor, Block, geometry, Transform
import numpy as np
from skimage.morphology import skeletonize
from scipy.ndimage import convolve
import random
import math


def under_cave_inner(box_build_cave_map,coor_basis,editor,worldSlice):
    transform=Transform(translation=coor_basis, rotation=0) #向きは内部で変化させるため
    editor.transform.push(transform)

    box_build_cave_map_np=np.array(box_build_cave_map[0])
    skeleton=skeletonize(box_build_cave_map_np.astype(bool))
    #print(skeleton)
    cave_inner_path_coor_origin=np.where(skeleton==True)
    #末端作成
    kernel = np.array([[1,1,1],
                    [1,0,1],
                    [1,1,1]])
    neighbors = convolve(skeleton.astype(int), kernel, mode='constant')
    endpoints=(skeleton & (neighbors == 1))
    endpoint_coords = np.argwhere(endpoints)
    cave_inner_path_coor=[]
    #座標の記録
    for i in range(len(cave_inner_path_coor_origin[0])):
        cave_inner_path_coor.append(box_build_cave_map[1][cave_inner_path_coor_origin[0][i]][cave_inner_path_coor_origin[1][i]])


    search_count=30

    cave_inner_path(cave_inner_path_coor,editor)
    place_torch(box_build_cave_map.copy(),editor)
    set_ore_base(box_build_cave_map,editor,worldSlice)
    search_place_rest_area(box_build_cave_map,cave_inner_path_coor_origin,editor,search_count)
    

    editor.transform.pop(transform)


def scan_sphere(box_build_cave_map,scan_coor,radius,worldSlice):
    #処理内容:指定された座標を基準にした球体のエリアをスキャンする.
    x=scan_coor[0]
    y=scan_coor[1]
    z=scan_coor[2]
    #中心をずらすために移動
    xc=0.5
    yc=0.5
    zc=0.5
    #調べるエリアを決定
    xl=2*radius-1
    yl=2*radius-1
    zl=2*radius-1
    sphere_ore=[]
    for i in range(xl):
        for j in range(yl):
            for k in range(zl):
                #scan_x,scan_y,scan_z
                sx=radius-i
                sy=radius-j
                sz=radius-k
                distance=math.sqrt((xc-sx+0.5)**2+(yc-sy+0.5)**2+(zc-sz+0.5)**2)
                if(distance <= radius):
                    block=worldSlice.getBlock([x+sx,y+sy,z+sz])
                    if(block.id != "minecraft:air"):
                        sphere_ore.append([x+sx,y+sy,z+sz])
    return sphere_ore


def set_ore_base(box_build_cave_map,editor,worldSlice):
    #処理内容:スキャン箇所を決定する.
    #壁検知式
    ore_list=["coal","iron","copper","gold","redstone","emerald","lapis","diamond","amethyst"]
    wall_coor=wall_check(box_build_cave_map)
    count=int(len(wall_coor)/20) #20マスに1つにする
    print(count)
    coor_list=random.sample(wall_coor,count)
    for i in range(len(coor_list)):
        radius=random.randint(4,8)
        sphere_ore=scan_sphere(box_build_cave_map,coor_list[i],radius,worldSlice)
        ore_type=random.choice(ore_list)
        set_ore(sphere_ore,ore_type,editor)
    


def set_ore(sphere_ore,ore_type,editor):
    block_list=[]
    deep=False
    for i in range(len(sphere_ore)):
        if(sphere_ore[i][1]<4): #y座標が深層岩より下なら
            stone="cobbled_deepslate"
            deep=True
        else:
            stone="cobblestone"
        if(ore_type=="iron" or ore_type=="gold" or ore_type=="copper"):
            ore_name="raw_"+ore_type+"_block"
            block_list.append(ore_name)
        if(ore_type!="amethyst"):
            if deep:
                block_list.append("deepslate_"+ore_type+"_ore")
            else:
                block_list.append(ore_type+"_ore")
        else:
            block_list.append(ore_type+"_block")




        #配置式
        #1割の確率で設置をキャンセル
        if(random.random()<0.8):
            #2割の確率で石
            if(random.random()<0.2):
                editor.placeBlock(sphere_ore[i],Block(stone))
            #残りの確率で鉱石をランダム
            else:
                block=random.choice(block_list)
                editor.placeBlock(sphere_ore[i],Block(block))
        else:
            pass






def wall_check(box_build_cave_map):
    wall_count=3
    wall_coor=[]
    for i in range(len(box_build_cave_map[0])):#xの方
        for j in range(len(box_build_cave_map[0][0])):#zの方
            if(box_build_cave_map[0][i][j]==1): #存在する時
                count=box_build_cave_map[0][i-1][j]+box_build_cave_map[0][i+1][j]+box_build_cave_map[0][i][j-1]+box_build_cave_map[0][i][j+1]
                if(count<=wall_count):
                    wall_coor.append(box_build_cave_map[1][i][j])
    return wall_coor

def search_place_rest_area(box_build_cave_map,cave_inner_path_coor_origin,editor,search_count):
    #処理内容:洞窟を探査して建築物を設置
    #道の座標に対して,ランダムに取り出し,その座標を中心とした5*5のマスを探す
    for i in range(search_count):
        check_coor_origin=random.randint(0,len(cave_inner_path_coor_origin[0])-1)
        x_base=cave_inner_path_coor_origin[0][check_coor_origin]
        z_base=cave_inner_path_coor_origin[1][check_coor_origin]
        flag=False
        coor_base=box_build_cave_map[1][x_base][z_base].copy()
        coor_y=coor_base[1]
        for j in range(5):
            for k in range(5):
                x=x_base -2 +j
                z=z_base -2 +k
                if(box_build_cave_map[1][x][z] != 0):
                    coor=box_build_cave_map[1][x][z].copy()
                else:
                    flag=True
                    break 
                if(coor[1]!=coor_y):
                    flag=True
                    break
            if flag:
                break
        if(flag==False):
            place_rest_area(coor_base,editor) #1つのみ設置するため,1回で脱出
            return

def place_rest_area(coor_base,editor):
    #処理内容:渡された座標に建築物を設置する
    x=coor_base[0]
    y=coor_base[1]
    z=coor_base[2]
    #床面
    geometry.placeCuboid(editor,(x-2,y,z-2),(x+2,y,z+2),Block("bamboo_planks"))
    editor.placeBlock([x,y,z],Block("campfire"))
    editor.placeBlock([x-1,y,z-1],Block("bamboo_stairs",{"facing":"north","shape":"inner_left"}))
    editor.placeBlock([x-1,y,z],Block("bamboo_stairs",{"facing":"west","shape":"straight"}))
    editor.placeBlock([x-1,y,z+1],Block("bamboo_stairs",{"facing":"south","shape":"inner_right"}))
    editor.placeBlock([x,y,z-1],Block("bamboo_stairs",{"facing":"north","shape":"straight"}))
    editor.placeBlock([x,y,z+1],Block("bamboo_stairs",{"facing":"south","shape":"straight"}))
    editor.placeBlock([x+1,y,z-1],Block("bamboo_stairs",{"facing":"north","shape":"inner_right"}))
    editor.placeBlock([x+1,y,z],Block("bamboo_stairs",{"facing":"east","shape":"straight"}))
    editor.placeBlock([x+1,y,z+1],Block("bamboo_stairs",{"facing":"east","shape":"inner_right"}))
    #柱
    geometry.placeCuboid(editor,(x-2,y+1,z-2),(x-2,y+4,z-2),Block("cobblestone_wall"))
    geometry.placeCuboid(editor,(x-2,y+1,z+2),(x-2,y+4,z+2),Block("cobblestone_wall"))
    geometry.placeCuboid(editor,(x+2,y+1,z-2),(x+2,y+4,z-2),Block("cobblestone_wall"))
    geometry.placeCuboid(editor,(x+2,y+1,z+2),(x+2,y+4,z+2),Block("cobblestone_wall"))
    #天井
    editor.placeBlock([x-2,y+5,z-2],Block("bamboo_stairs",{"facing":"east","shape":"outer_right"}))
    editor.placeBlock([x-2,y+5,z+2],Block("bamboo_stairs",{"facing":"east","shape":"outer_left"}))
    editor.placeBlock([x+2,y+5,z-2],Block("bamboo_stairs",{"facing":"west","shape":"outer_left"}))
    editor.placeBlock([x+2,y+5,z+2],Block("bamboo_stairs",{"facing":"west","shape":"outer_right"}))
    geometry.placeCuboid(editor,(x-2,y+5,z-1),(x-2,y+5,z+1),Block("bamboo_stairs",{"facing":"east","shape":"straight"}))
    geometry.placeCuboid(editor,(x-1,y+5,z-2),(x+1,y+5,z-2),Block("bamboo_stairs",{"facing":"south","shape":"straight"}))
    geometry.placeCuboid(editor,(x-1,y+5,z+2),(x+1,y+5,z+2),Block("bamboo_stairs",{"facing":"north","shape":"straight"}))
    geometry.placeCuboid(editor,(x+2,y+5,z-1),(x+2,y+5,z+1),Block("bamboo_stairs",{"facing":"west","shape":"straight"}))
    geometry.placeCuboid(editor,(x-1,y+6,z-1),(x+1,y+6,z+1),Block("bamboo_slab",{"type":"bottom"}))
    editor.placeBlock([x,y+6,z],Block("bamboo_planks"))
    #装飾
    editor.placeBlock([x,y+1,z],Block("water_cauldron",{"level":"3"}))
    editor.placeBlock([x+2,y+1,z+1],Block("water_cauldron",{"level":"3"}))
    geometry.placeCuboid(editor,(x,y+2,z),(x,y+5,z),Block("bamboo_fence"))
    editor.placeBlock([x+1,y+5,z-1],Block("lantern",{"hanging":"true"}))
    editor.placeBlock([x-1,y+5,z+1],Block("lantern",{"hanging":"true"}))
    editor.placeBlock([x,y+7,z],Block("lantern",{"hanging":"false"}))
    



def cave_inner_path(cave_inner_path_coor,editor):
    #処理内容:道を元に一定間隔で松明を置く
    for i in range(len(cave_inner_path_coor)):
        if(i%5==0):
            coor=cave_inner_path_coor[i].copy()
            coor[1]+=1
            editor.placeBlock(coor,Block("torch"))

def place_torch(box_build_cave_map,editor):
    #処理内容:松明を全域においての脇つぶし
    for i in range(len(box_build_cave_map[0])):#xの方
        for j in range(len(box_build_cave_map[0][0])):#zの方
            if(i%5==0 and j%5==0 and box_build_cave_map[1][i][j]!=0):
                print(box_build_cave_map[1][i][j])
                coor=box_build_cave_map[1][i][j].copy() 
                coor[1]+=1 #y座標を1つ上げる
                editor.placeBlock(coor,Block("torch"))

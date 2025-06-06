from gdpc import Editor, Block, geometry,Transform
from Block_check import block_check,colored
from under_cave_inner import under_cave_inner
from skimage.morphology import skeletonize
from scipy.ndimage import convolve
import time
import cave_base
import winsound
import math
editor = Editor(buffering=True)
import numpy as np




color_table=["black","dark_blue","dark_green","dark_aqua","dark_red","dark_purple",
            "gold","gray","dark_gray","blue","green","aqua","red","light_purple",
            "yellow","white"]

#buildareaを読み込むことで読み込み処理速度が増加する.

#worldslice内で扱う座標とMinecraft内で扱う座標の変換
#coor_basisは,worldsliceの基準となる座標.
#coor_MCは,minecraft内での座標
#coor_WSは,coor_MCを原点としたWorldSlive内の座標

def slope_calu(min_coor,max_coor):
    print(min_coor)
    print(max_coor)
    xz=math.sqrt((min_coor[0]-max_coor[0])**2+(min_coor[2]-max_coor[2])**2)
    diff_height=max_coor[1]-min_coor[1]
    if(xz!=0):
        slope=diff_height/xz
    else:
        slope=-1
    return slope



def xz_cluster(cluster):
    cluster_map=[[[] for i in range(pillar_map_length[0])] for j in range(pillar_map_length[1])]
    for i in range(len(cluster)):
        x=cluster[i][0]
        y=cluster[i][1]
        z=cluster[i][2]
        cluster_map[x][z].append(y)
    return cluster_map


def wall_check(cluster_map,i):
    coor_wall=[]
    for x in range(pillar_map_length[0]):
        for z in range(pillar_map_length[1]):
            search_coor=cluster_map[x][z]
            if(search_coor):
                floor_count=len(cluster_map[x+1][z])+len(cluster_map[x-1][z])+len(cluster_map[x][z+1])+len(cluster_map[x][z-1])
                if(floor_count <= 3):
                    coor_wall.append([x,search_coor[0],z])
                    cave_list[i].remove([x,search_coor[0],z]) #壁の座標を消す
                    
    
    return coor_wall




def coortrans_WS_to_MC(coor_WS,coor_basis):
    coor_trans=[0,0,0]
    for i in range(len(coor_trans)):
        coor_trans[i]=coor_basis[i]+coor_WS[i]

    return coor_trans

def coortrans_MC_to_WS(coor_MC,coor_basis):
    coor_trans=[0,0,0]
    for i in range(len(coor_trans)):
        coor_trans[i]=coor_MC[i]-coor_basis[i]

    return coor_trans
#pillar_map[x][z].append(coor_scan) 
#coor=[[x,coor_scan[1],z],coor_scan]
def bfs(coor_wait,pillar_map,cluster):
    coor_vis=[]
    while (coor_wait): #探索する配列が空かを調べる.
        coor_current=coor_wait.pop(0).copy()
        coor_vis.append([coor_current[0],coor_current[0]])
        for i in range(4):
            xi=[0,0,1,-1]
            zi=[1,-1,0,0]
            shift_x=coor_current[0]+xi[i]
            shift_z=coor_current[2]+zi[i]
            #pillar_mapの範囲内かを調べる
            if(shift_x >= 0 and shift_x <=pillar_map_length[0]-1): 
                if(shift_z >= 0 and shift_z <=pillar_map_length[1]-1):
                    search_coor=pillar_map[shift_x][shift_z].copy()
                    if(search_coor and [shift_x,shift_z] not in coor_vis):
                        basis_height=coor_current[1]
                        for i in range(len(search_coor)):
                            comp_height=search_coor[i][1]
                            if(abs(basis_height-comp_height) <= perm_height_diff):
                                del pillar_map[shift_x][shift_z][i]
                                coor_wait.append([shift_x,comp_height,shift_z])
                                cluster.append([[shift_x,comp_height,shift_z],search_coor[i]])
                                break
                            else:
                                coor_vis.append([shift_x,shift_z])
                    else:
                        if([shift_x,shift_z] not in coor_vis):
                            coor_vis.append([shift_x,shift_z])
    return pillar_map,cluster


#探したいもの:地下の建築可能スペース.
#条件1
#海抜よりも低い事(y=62以下)
#深層岩よりも高い事(y=8以上)
#天井が8-16(要検証)マス程度の高さがあること.
#平坦であること
#探しているのは,大規模な空洞
#大規模空洞に街を作る.
#使いやすいように,洞窟のあるエリアを,長方体として記録したい.
#探索範囲を,地下許容エリア範囲内にする.

#壁に関する処理
#エリアの中心を求め,中心と逆側を調べる.逆側が空気だったら壁,そうでなければ石材




#buildareaの設定
#XL,YL,ZL=255
#y下限:-64
XS=100
YS=0
ZS=100
XL,YL,ZL=300,256,300
coor_basis=[XS,YS,ZS]

command_build_area= f"setbuildarea {XS} {-64} {ZS} {XS+XL} {YS+YL} {ZS+ZL}"
editor.runCommand(command_build_area)


worldSlice = editor.loadWorldSlice() #worldsliceの座標系を確保
buildArea = editor.getBuildArea() #上に同じだが,処理で使用
#worldSliceのy座標は,必ず0が基準になる.
#WorldSlice(0,0,0)=MC(,0,?)


#呼び出される関数として考える.
#渡されるもの
#editor,worldSlice,基準座標(worldSlice内),worldSlice_size,調査範囲,方向
#基準座標を原点として,範囲のエリアを調べる.
#基準座標は,各階層のメイン地下拠点の中心.
#端に近い場合,それだけずらす
#x,y,z:探査範囲の座標,X,Y,Z:マイクラ内での座標


start = time.time()

direction=1 #一旦eastにする.

x_range=200 #奥行,進行方向への調査範囲
y_range=30 #高さ,基準から上下に探査する
z_range=100 #横,基準から左右に探査する

y_scan_range=y_range*2+1




pillars=[] #ピラーをまとめておくリスト
clusters=[] #クラスターをまとめておくリスト
pillar_map_length=[x_range,z_range*2+1]
pillar_map=[[[] for i in range(pillar_map_length[1])] for j in range(pillar_map_length[0])]
PILLAR_LENGHT=6 #ピラーとなる長さ.
pillar_height=0
pillar_mode=0 #ピラーを作っているかを調べる.
#洞窟内に存在する,洞窟の壁を構成しないブロックのリスト 
#水と溶岩だけ,別の処理
no_stone_block=["minecraft:air","minecraft:short_grass","minecraft:big_dripleaf",
                   "minecraft:small_dripleaf","minecraft:moss_carpet","minecraft:azalea",
                   "minecraft:tall_grass","minecraft:big_dripleaf_stem","minecraft:cave_vines_plant",
                   "minecraft:cave_vines","minecraft:spore_blossom","minecraft:pointed_dripstone"
                   "minecraft:lava","minecraft:water"]

#洞窟内に存在する,洞窟を構成するブロック
stone_block=[]


#実際に探査する座標についての考え方.
#与えられた方角を向いている時の左手側を原点にする

#向きごとにマインクラフトの座標をどう操作するかを変える
#east:x=+X z=+Z dire=0 #"east"
#south:x=+Z z=-X dire=3  #"south"
#west:x=-X z=-Z dire=2 #"west"
#north:x=-Z z=+X dire=1 #"north"


#基準座標の移動
coor_base=[150,20,150]#この座標は,探査位置の中心部なので,初期地点を求める. #WS系


if(direction==0):
    coor_base[2] -= z_range
elif(direction==1):
    coor_base[0] -= z_range
elif(direction==2):
    coor_base[2] += z_range
elif(direction==3):
    coor_base[0] += z_range

#y座標を探査したい高さの下方向にずらす
coor_base[1] += y_range

#探査の初期地点がエリア外なら,それをずらす.
if(direction==0):
    if(coor_base[2]<0):
        coor_base[2] =0
    elif(coor_base[2]+pillar_map_length[1]>ZL):
        coor_base[2] = ZL-pillar_map_length[1]
elif(direction==1):
    if(coor_base[0]<0):
        coor_base[0]=0
    elif(coor_base[0]>XL):
        coor_base[0] =XL-pillar_map_length[1]
elif(direction==2):
    if(coor_base[2]<pillar_map_length[1]):
        coor_base[2]=pillar_map_length[1]
    elif(coor_base[2]>ZL):
        coor_base[2] =ZL
elif(direction==3):
    if(coor_base[0]<pillar_map_length[1]):
        coor_base[0]=pillar_map_length[1]
    elif(coor_base[0]>XL):
        coor_base[0] =XL

transform=Transform(translation=coor_basis, rotation=0) #向きは内部で変化させるため
editor.transform.push(transform)



coor_scan=[0,0,0] #仮定義

for x in range(pillar_map_length[0]):
    for z in range(pillar_map_length[1]):
        pillar_mode=0
        for y in range(y_scan_range):
            coor_scan[1] = coor_base[1]-y
            if(direction==0):
                coor_scan[0] = coor_base[0]+x
                coor_scan[2] = coor_base[2]+z
            elif(direction==1):
                coor_scan[0] = coor_base[0]+z
                coor_scan[2] = coor_base[2]-x
            elif(direction==2):
                coor_scan[0] = coor_base[0]-x
                coor_scan[2] = coor_base[2]-z
            elif(direction==3):
                coor_scan[0] = coor_base[0]-z
                coor_scan[2] = coor_base[2]+x

            block=worldSlice.getBlock(coor_scan)

            if(block.id in no_stone_block):
                if(block.id=="minecraft:lava" or block.id=="minecraft:water"):
                    if(block.states['level']!='0'): #水流,溶岩流なら無視
                        editor.placeBlock(coor_scan,Block("air"))
                    else: #水源埋め立て
                        editor.placeBlock(coor_scan,Block("stone"))
                #block_check(coortrans_WS_to_MC(coor_WS,coor_basis),"purple")
                if(pillar_mode==0):
                    pillar_mode=1
                    #block_check(coortrans_WS_to_MC(coor_WS,coor_basis),1)
                    pillar_height=1 #ピラーの現在の長さ
                else: #pillar_mode==1
                    pillar_height += 1
            else:
                if(pillar_mode==1):
                    pillar_mode=0
                    if(PILLAR_LENGHT <= pillar_height):
                        pillar=[coor_scan.copy(),pillar_height]
                        pillars.append(pillar)
                        pillar_map[x][z].append(coor_scan.copy()) 
                        #coor_scan_temp=[coor_scan[0],coor_scan[1],coor_scan[2]]
                        #block_check(coortrans_WS_to_MC(coor_scan_temp,coor_basis),"blue")


editor.transform.pop(transform)

#pillarに記録されているcoor_scan: WSにおける座標

#pillar_mapにWS座標を入力




end = time.time()
time_diff = end - start
print(time_diff)  
search_block_count=(pillar_map_length[0])*(pillar_map_length[1])*(y_scan_range)
print(f"調査ブロック数:{search_block_count}")
print(f"ピラー数:{len(pillars)}")
#print(pillar_map)
#piller_mapに対して探査を行う.
coor_wait=[] #調査待ち 高さの情報も入れる
coor_vis=[] #調査済み 高さの情報をいれない.
coor_wall=[] #壁を建てる予定の座標

perm_height_diff=3 #permission_height_difference:高さの差の許容値
cluster_count=0


for x in range(pillar_map_length[0]):
    for z in range(pillar_map_length[1]):
        for count in range(len(pillar_map[x][z])):
            cluster=[]
            coor_scan=pillar_map[x][z].pop(0).copy()
            coor=[x,coor_scan[1],z]
            coor_wait.append(coor.copy()) 
            cluster.append([coor.copy(),coor_scan.copy()])
            pillar_map,cluster=bfs(coor_wait.copy(),pillar_map.copy(),cluster.copy())
            clusters.append(cluster.copy())
cave_list=[]


# print(f"クラスター数:{len(clusters)}")
# for i in range(len(clusters)): #クラスター全体の数
#     volume_sum=0
#     for j in range(len(clusters[i])):#各クラスターのピラーの数
#         for k in range(len(pillars)):
#             if(clusters[i][j] in pillars[k]):
#                 volume_sum+=pillars[k][1]
#     if(volume_sum >= 1000): #体積で取っているが,床面積でも良いかも
#         print(f"ピラー数:{len(clusters[i])},体積:{volume_sum}")
#         cave_list.append(clusters[i])

min_space=200 #床面積の最小値

print(f"クラスター数:{len(clusters)}")

build_cave=[] #建築可能洞窟
not_build_cave=[] #建築不能洞窟

box_build_cave=[] #長方形に加工したもの
box_not_build_cave=[]

for i in range(len(clusters)): #クラスター全体の数
    #print(f"クラスターの広さ:{len(clusters[i])}")
    if(len(clusters[i])>=min_space):
        min_height=1000
        max_height=0
        for j in range(len(clusters[i])):#各クラスターのピラーの数
            #print(clusters[i][j][1])
            #block_check(coortrans_WS_to_MC(clusters[i][j][1],coor_basis),color_table[i%len(color_table)])
            height=clusters[i][j][1][1]
            if(height<=min_height):
                min_height=height
                min_coor=clusters[i][j][1].copy()
            if(height>max_height):
                max_height=height
                max_coor=clusters[i][j][1].copy()
        slope=slope_calu(min_coor,max_coor)
        if(slope<1):
            build_cave.append(clusters[i])
        else:
            not_build_cave.append(clusters[i])

        print(f"クラスターの広さ:{len(clusters[i])}")
        print(f"識別色:{color_table[i%len(color_table)]}")
        print(f"傾き:{slope}")
for i in range(len(build_cave)):
    for j in range(len(build_cave[i])):
        #block_check(coortrans_WS_to_MC(build_cave[i][j][1],coor_basis),color_table[i%len(color_table)])
        pass


for i in range(len(build_cave)):
    #box化(xz平面で取り扱える形にする)
    #方策:xとzの最大最小を探す.
    min_x=10000
    min_z=10000
    max_x=-1
    max_z=-1
    for j in range(len(build_cave[i])):
        coor=build_cave[i][j][0]
        if(coor[0]<min_x):
            min_x=coor[0]
        if(coor[0]>max_x):
            max_x=coor[0]
        if(coor[2]<min_z):
            min_z=coor[2]
        if(coor[2]>max_z):
            max_z=coor[2]
    print(f"min_x:{min_x},max_x:{max_x},min_z:{min_z},max_z:{max_z}")
    box_x_range=max_x - min_x
    box_z_range=max_z - min_z
    box_build_cave_map=[[[ 0 for i in range(box_z_range +1)] for j in range(box_x_range +1)] for k in range(2)]
    #+1は引き算によって生じた差の分
    #2つ目のレイヤーにはWS座標を記録
    for j in range(len(build_cave[i])):
        coor=build_cave[i][j][0]
        coor_WS=build_cave[i][j][1]
        #print(coor)
        box_build_cave_map[0][coor[0]-min_x][coor[2]-min_z]=1
        box_build_cave_map[1][coor[0]-min_x][coor[2]-min_z]=coor_WS.copy()
    #マップの端に0を設置
    for l in range(box_z_range +1):
        box_build_cave_map[0][0][l]=0
        box_build_cave_map[0][box_x_range][l]=0
    for m in range(box_x_range +1):
        box_build_cave_map[0][m][0]=0
        box_build_cave_map[0][m][box_z_range]=0    
    #ここまでbox化
    
    #box化した値をunder_cave_innerに送る


    #ここから道を引く処理

    under_cave_inner(box_build_cave_map,coor_basis,editor,worldSlice)

#洞窟の処理
#1:道を引く
#2:松明を設置する(道)
#3:建築ができるかを調べる(処理回数は20~30?)
#4:鉱石を設置する
  
    





#探査系から見たマップ
#この内部に,洞窟の情報や建築物の情報をいれる
#0:何もなし
#1:建築エリア
#2:建築可能洞窟
#2:建築不能洞窟
#3:特殊建造物
scan_area_map=[[[0] for i in range(pillar_map_length[1])] for j in range(pillar_map_length[0])]
for i in range(len(build_cave)):

    for j in range(len(build_cave[i])):
        coor=build_cave[i][j][0]
        scan_area_map[coor[0]][coor[2]]=1
    #print("test1")

for i in range(len(not_build_cave)):
    for j in range(len(not_build_cave[i])):
        coor=not_build_cave[i][j][0]
        scan_area_map[coor[0]][coor[2]]=2
    #print("test2")






#洞窟のタイプ:
#広場タイプ


colored()
editor.flushBuffer()







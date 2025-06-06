from gdpc import Editor, Block, geometry,Transform
from Block_check import block_check,colored
import time
import cave_base
editor = Editor(buffering=True)



#buildareaの設定
#XL,YL,ZL=255
#y下限:-64
XS=100
YS=0
ZS=100
XL,YL,ZL=500,256,500
coor_basis=[XS,YS,ZS]

command_build_area= f"setbuildarea {XS} {-64} {ZS} {XS+XL} {YS+YL} {ZS+ZL}"

editor.runCommand(command_build_area)




#buildareaを読み込むことで読み込み処理速度が増加する.

#worldslice内で扱う座標とMinecraft内で扱う座標の変換
#coor_basisは,worldsliceの基準となる座標.
#coor_MCは,minecraft内での座標
#coor_WSは,coor_MCを原点としたWorldSlive内の座標

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

def bfs(coor_wait,pillar_map,cluster):
    coor_vis=[]
    while (coor_wait): #探索する配列が空かを調べる.
        coor_current=coor_wait.pop(0)
        coor_vis.append([coor_current[0],coor_current[2]])
        for i in range(4):
            xi=[0,0,1,-1]
            zi=[1,-1,0,0]
            shift_x=coor_current[0]+xi[i]
            shift_z=coor_current[2]+zi[i]
            #pillar_mapの範囲内かを調べる
            if(shift_x >= 0 and shift_x <=pillar_map_length[0]-1): 
                if(shift_z >= 0 and shift_z <=pillar_map_length[1]-1):
                    search_coor=pillar_map[shift_x][shift_z]
                    if(search_coor and [shift_x,shift_z] not in coor_vis):
                        basis_height=coor_current[1]
                        for i in range(len(search_coor)):
                            comp_height=search_coor[i] #マップの一番上の高さとのみ比較する.
                            if(abs(basis_height-comp_height) <= perm_height_diff):
                                del pillar_map[shift_x][shift_z][i]
                                coor_wait.append([shift_x,comp_height,shift_z])
                                cluster.append([shift_x,comp_height,shift_z])
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


start = time.time()
worldSlice = editor.loadWorldSlice() #worldsliceの座標系を確保
#worldSliceのy座標は,必ず0が基準になる.
#WorldSlice(0,0,0)=MC(,0,?)


transform=Transform(translation=coor_basis)
editor.transform.push(transform)
#座標系をWS系に合わせる


SEA_LEVEL=62#海抜の高さ
DEEP_LAYER=-20#深層岩の出現する高さ (y=8)

y_scan_range=SEA_LEVEL-DEEP_LAYER #調査する幅
#端っこは見る必要が薄いため,端っこは見ない.(8ブロック程度を無視)
IGNORE_LENGTH=2 #無視する長さ





pillars=[] #ピラーをまとめておくリスト
clusters=[] #クラスターをまとめておくリスト
pillar_map_length=[XL,ZL]
pillar_map=[[[] for i in range(pillar_map_length[0])] for j in range(pillar_map_length[1])]
PILLAR_LENGHT=6 #ピラーとなる長さ.
pillar_height=0
pillar_mode=0 #ピラーを作っているかを調べる.
#洞窟内に存在する,洞窟の壁を構成しないブロックのリスト #水に入っているかも調べる
no_stone_block=["minecraft:air","minecraft:short_grass","minecraft:big_dripleaf",
                   "minecraft:small_dripleaf","minecraft:moss_carpet","minecraft:azalea",
                   "minecraft:tall_grass","minecraft:big_dripleaf_stem","minecraft:cave_vines_plant",
                   "minecraft:cave_vines","minecraft:spore_blossom"]


#調査したい範囲
#

#現在の処理:全域探査
#行いたい処理:探査範囲の制限(メイン坑道近辺のみにしたい.)



for x in range(pillar_map_length[0]):
    for z in range(pillar_map_length[1]):
        if(x>=IGNORE_LENGTH and XL-x>=IGNORE_LENGTH):
            if(z>=IGNORE_LENGTH and ZL-z>=IGNORE_LENGTH):
                pillar_mode=0 #底抜けと見て無視する(修正可能性あり)
                for y in range(y_scan_range):
                    y_scan=SEA_LEVEL-y #下方向へと調査する. 
                    coor_WS=[x,y_scan,z]
                    #print(coor_WS)
                    block=worldSlice.getBlock(coor_WS)
                    #print(block)
                    if(block.id == "minecraft:stone_bricks"): #2回目用の処理なので無視
                        editor.placeBlock(coor_WS,Block("air"))
                        block.id="minecraft:air"


                    if(block.id in no_stone_block):
                        #block_check(coortrans_WS_to_MC(coor_WS,coor_basis),4)
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
                                pillar=[coor_WS,pillar_height]
                                pillars.append(pillar)
                                pillar_map[coor_WS[0]][coor_WS[2]].append(coor_WS[1])
                                #block_check(coortrans_WS_to_MC(coor_WS,coor_basis),2)

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
            basis_height=pillar_map[x][z].pop(0)
            coor=[x,basis_height,z]
            coor_wait.append(coor)
            cluster.append(coor)
            pillar_map,cluster=bfs(coor_wait,pillar_map,cluster)
            clusters.append(cluster)


cave_list=[]

print(f"クラスター数:{len(clusters)}")
for i in range(len(clusters)):
    volume_sum=0
    for j in range(len(clusters[i])):
        for k in range(len(pillars)):
            if(clusters[i][j] in pillars[k]):
                volume_sum+=pillars[k][1]
    if(volume_sum >= 1000): #体積で取っているが,床面積でも良いかも
        print(f"ピラー数:{len(clusters[i])},体積:{volume_sum}")
        cave_list.append(clusters[i])
    

for i in range(len(cave_list)):
    print(f"cave代表座標{cave_list[i][0]}")
    #i+=2
    #壁を建てる処理
    cluster_map=xz_cluster(cave_list[i])
    #coor_wall=wall_check(cluster_map,i)
    
    for j in range(len(coor_wall)):
        block_check(coortrans_WS_to_MC(coor_wall[j],coor_basis),"red")
        #cave_base.build_wall(coortrans_WS_to_MC(coor_wall[j],coor_basis),"stone_bricks",5)
        pass
    for k in range(len(cave_list[i])):
        #床を張り直す処理
        #print(cave_list[i][j])
        block_check(coortrans_WS_to_MC(cave_list[i][k],coor_basis),"blue")
        #cave_base.build_floor(coortrans_WS_to_MC(cave_list[i][k],coor_basis),"stone")
        #天井と空間を確保する処理
        #cave_base.build_ceiling(worldSlice,cave_list[i][k],coortrans_WS_to_MC(cave_list[i][k],coor_basis),"stone",no_stone_block)
        pass  
    break


editor.flushBuffer()

# print(len(clusters))
# for i in range(len(clusters)):
#     print(len(clusters[i]))
    # if(clusters[i]):
    #     for j in range(len(clusters[0])):
    #         cave_base.build_floor(coortrans_WS_to_MC(clusters[i][j],coor_basis),"stone")
    #     cluster_map=xz_cluster(clusters[0])
    #     coor_wall=wall_check(cluster_map)
    #     for j in range(len(coor_wall)):
    #         cave_base.build_wall(coortrans_WS_to_MC(coor_wall[j],coor_basis),"stone_bricks",6)













colored("red")
colored("blue")





#狭ければ渓谷,広ければ空洞.



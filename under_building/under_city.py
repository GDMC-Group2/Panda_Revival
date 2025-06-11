from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_building.under_build import under_build_base,place_door,place_bed,place_pot,base_transform,summon_animal,fix_rotation
from under_building.under_apartment import under_apartment
from under_building.under_house import under_house_1 ,under_house_2
from under_building.under_well import under_well
from under_building.under_park import under_park_1
from under_building.museum import museum1
from under_building.panda_statue import panda_statue

# editor=Editor()

# coor=[150,-61,200]
# rotation=0
# size=[115,7,115]
def under_city(editor,coor,base_coor,base_rota,rotation,size=[115,7,115]):
    with editor.pushTransform(Transform(coor,rotation=base_rota)):

        #13*13が 7*7
        #建築物 
        #集合住宅 under_apartment
        #高級住宅 under_house_1 ,under_house_2
        #井戸 under_well
        #公園 under_park_1

        #ランダム抽選の重さ
        build_list=["under_apartment","under_house_1","under_house_2","under_well","under_park_1"]
        weight=[4,1,1,2,2]
        under_build_base(editor,coor,base_rota,size)


        #道
        for i in range(8):
            geometry.placeCuboid(editor,[0,0,0+i*16],[115,0,2+i*16],Block("smooth_stone")) 
            geometry.placeCuboid(editor,[0+i*16,0,0],[2+i*16,0,115],Block("smooth_stone")) 
    
        for i in range(7):
            for j in range(7):
                build_coor=[3+i*16,0,3+j*16]
                base_coor_tran=base_transform(build_coor,base_coor,rotation)
                b_rota=0
                c_rota=fix_rotation(b_rota,rotation)
                #確率で建築物を設置する
                build_name=random.choices(build_list,weights=weight)
                build_name=' '.join(build_name)
                if(build_name=="under_apartment"):
                    under_apartment(editor,build_coor,base_coor_tran,b_rota,c_rota)
                elif(build_name=="under_house_1"):
                    under_house_1(editor,build_coor,base_coor_tran,b_rota,c_rota)
                elif(build_name=="under_house_2"):
                    under_house_2(editor,build_coor,base_coor_tran,b_rota,c_rota)
                elif(build_name=="under_well"):
                    under_well(editor,build_coor,base_coor_tran,b_rota,c_rota)
                elif(build_name=="under_park_1"):
                    under_park_1(editor,build_coor,base_coor_tran,b_rota,c_rota)

        #出入口 
        geometry.placeCuboid(editor,[-1,1,55],[-1,7,61],Block("air"))

        build_tunnel(editor,[18,1,115],1,8)
        museum1(editor,32,-1,123,base_coor,1)
        geometry.placeCuboid(editor,[16,1,123],[18,3,123],Block("air"))
        panda_statue(editor,166,1,68,base_coor,2)
        build_tunnel_deco(editor,[115,1,55],0,20)





        #追加建造物


#under_city(editor,coor,rotation,size)




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


def build_tunnel_deco(editor,coor,rotation,length):
    #用途:装飾された道の作成
    with editor.pushTransform(Transform(coor,rotation=rotation)):
        #トンネルの左下を基準にする
        
        geometry.placeCuboid(editor,[0,-1,0],[length+1,-1,4],Block("polished_granite"))
        geometry.placeCuboid(editor,[1,0,-1],[length,4,-3],Block("polished_diorite"))
        geometry.placeCuboid(editor,[1,0,5],[length,4,7],Block("polished_diorite"))
        geometry.placeCuboid(editor,[1,5,0],[length,6,4],Block("polished_diorite"))
        geometry.placeCuboid(editor,[0,-1,1],[length+1,-1,3],Block("polished_diorite"))
        geometry.placeCuboid(editor,[0,0,0],[length+1,4,4],Block("air"))
        geometry.placeCuboid(editor,[0,5,-2],[0,5,6],Block("stripped_acacia_log",{"axis":"z"}))          
        geometry.placeCuboid(editor,[0,1,-1],[0,6,-1],Block("stripped_acacia_log"))  
        geometry.placeCuboid(editor,[0,1,5],[0,6,5],Block("stripped_acacia_log"))
        editor.placeBlock([0,0,-1],Block("obsidian")) 
        editor.placeBlock([0,0,5],Block("obsidian")) 
        for i in range(length):
            if(i!=0 and i%3==0):
                geometry.placeCuboid(editor,[i,0,5],[i,4,5],Block("stripped_acacia_log"))
                editor.placeBlock([i,1,5],Block("crimson_trapdoor",{"facing":"south","open":"true"}))
                editor.placeBlock([i,1,6],Block("torch"))
                geometry.placeCuboid(editor,[i,0,-1],[i,4,-1],Block("stripped_acacia_log"))
                editor.placeBlock([i,1,-1],Block("crimson_trapdoor",{"facing":"north","open":"true"}))
                editor.placeBlock([i,1,-2],Block("torch"))


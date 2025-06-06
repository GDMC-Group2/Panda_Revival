from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_build import under_build_base,place_door,place_bed,place_pot
from under_apartment import under_apartment
from under_house import under_house_1 ,under_house_2
from under_well import under_well
from under_park import under_park_1


editor=Editor()

coor=[150,-61,200]
rotation=0
size=[115,7,115]
def under_city(editor,coor,rotation,size):

    

    #ランダム抽選の重さ
    build_list=["under_apartment","under_house_1","under_house_2","under_well","under_park_1"]
    weight=[4,1,1,2,2]
    

    base_coor=coor #分かりやすさの為記述
    transform=Transform(translation=coor, rotation=rotation)
    editor.transform.push(transform)
    under_build_base(editor,coor,rotation,size)



    #道
    for i in range(8):
        geometry.placeCuboid(editor,[0,0,0+i*16],[115,0,2+i*16],Block("smooth_stone")) 
        geometry.placeCuboid(editor,[0+i*16,0,0],[2+i*16,0,115],Block("smooth_stone")) 
  
    for i in range(7):
        for j in range(7):
            build_coor=[3+i*16,0,3+j*16]
            #確率で建築物を設置する
            build_name=random.choices(build_list,weights=weight)
            build_name=' '.join(build_name)
            if(build_name=="under_apartment"):
                under_apartment(editor,build_coor)
            elif(build_name=="under_house_1"):
                under_house_1(editor,build_coor,base_coor,rotation)
            elif(build_name=="under_house_2"):
                under_house_2(editor,build_coor,base_coor,rotation)
            elif(build_name=="under_well"):
                under_well(editor,build_coor)
            elif(build_name=="under_park_1"):
                under_park_1(editor,build_coor)
    #13*13が 7*7
    #建築物 
    #集合住宅 under_apartment
    #高級住宅 under_house_1 ,under_house_2
    #井戸 under_well
    #公園 under_park_1

under_city(editor,coor,rotation,size)





from gdpc import Editor, Block, geometry, Transform
import time
from under_build import under_build_base,summon_animal
import random


def under_bamboo_farm(editor,coor,base_coor,build_rotation,rotation,size=[13,10,13]):
    with editor.pushTransform(Transform(coor,rotation=build_rotation)):
        under_build_base(editor,coor,rotation,size)
        geometry.placeCuboid(editor,[0,0,0],[12,0,12],Block("dirt"))
        for i in range(4):
            for j in range(4):
                place_bamboo(editor,[2+i,1,2+j])
        for i in range(4):
            for j in range(4):
                place_bamboo(editor,[7+i,1,2+j])
        for i in range(4):
            for j in range(4):
                place_bamboo(editor,[2+i,1,7+j])
        for i in range(4):
            for j in range(4):
                place_bamboo(editor,[7+i,1,7+j])

        #床光源
        editor.placeBlock([1,1,1],Block("torch"))
        editor.placeBlock([1,1,6],Block("torch"))
        editor.placeBlock([1,1,11],Block("torch"))
        editor.placeBlock([6,1,1],Block("torch"))
        editor.placeBlock([6,1,6],Block("torch"))
        editor.placeBlock([6,1,11],Block("torch"))
        editor.placeBlock([11,1,1],Block("torch"))
        editor.placeBlock([11,1,6],Block("torch"))
        editor.placeBlock([11,1,11],Block("torch"))

        #収納
        editor.placeBlock([12,1,0],Block("chest",{"facing":"west","type":"right"}))
        editor.placeBlock([12,1,1],Block("chest",{"facing":"west","type":"left"}))
        editor.placeBlock([12,2,0],Block("chest",{"facing":"west","type":"right"}))
        editor.placeBlock([12,2,1],Block("chest",{"facing":"west","type":"left"}))

        #天井光源
        editor.placeBlock([1,10,6],Block("birch_fence"))
        editor.placeBlock([1,9,6],Block("chain",{"axis":"y"}))
        editor.placeBlock([1,8,6],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([6,10,1],Block("birch_fence"))
        editor.placeBlock([6,9,1],Block("chain",{"axis":"y"}))
        editor.placeBlock([6,8,1],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([6,10,6],Block("birch_fence"))
        editor.placeBlock([6,9,6],Block("chain",{"axis":"y"}))
        editor.placeBlock([6,8,6],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([6,10,11],Block("birch_fence"))
        editor.placeBlock([6,9,11],Block("chain",{"axis":"y"}))
        editor.placeBlock([6,8,11],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([11,10,6],Block("birch_fence"))
        editor.placeBlock([11,9,6],Block("chain",{"axis":"y"}))
        editor.placeBlock([11,8,6],Block("lantern",{"hanging":"true"}))

        for i in range(2):
            summon_animal(editor,[11,1,6],base_coor,rotation,"panda","panda")

def place_bamboo(editor,coor,rate=0.1):
    #用途:竹の生成.
    #良い感じにしたいので,ランダムにする.
    #bamboo_sapling_rate=0.1 タケノコになる可能性
    bamboo_sapling_rate=rate

    if(random.random()<bamboo_sapling_rate):
        editor.placeBlock(coor,Block("bamboo_sapling"))
    else:
        bamboo_height=random.randint(2,8)
        if(bamboo_height<=3):
            age="0"
        else:
            age="1"
        for i in range(bamboo_height):
            if(i != 0 and bamboo_height-i<=2):
                leaves="large"
            else:
                leaves="none"
            bamboo=Block("bamboo",{"age":age,"leaves":leaves})
            editor.placeBlock([coor[0],coor[1]+i,coor[2]],bamboo)

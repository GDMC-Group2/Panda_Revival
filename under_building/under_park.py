from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_building.under_build import under_build_base,place_stand,place_frame,place_frame_up,\
place_door,place_bed,place_pot,summon_animal


def under_park_1(editor,coor,base_coor,b_rota,c_rota):
    #原点座標系の算出
    #コケ広場
    with editor.pushTransform(Transform(coor,rotation=b_rota)):
        geometry.placeCuboid(editor,[0,0,0],[12,0,12],Block("moss_block"))

        #花壇
        lists=[Block("azalea"),Block("flowering_azalea")]
        geometry.placeCuboid(editor,[1,1,2],[2,1,10],Block("moss_block"))
        geometry.placeCuboid(editor,[1,2,2],[2,2,10],lists)
        geometry.placeCuboid(editor,[0,1,2],[0,1,10],Block("spruce_trapdoor",{"facing":"west","open":"true"}))
        geometry.placeCuboid(editor,[3,1,2],[3,1,10],Block("spruce_trapdoor",{"facing":"east","open":"true"}))
        geometry.placeCuboid(editor,[1,1,1],[2,1,1],Block("spruce_trapdoor",{"facing":"north","open":"true"}))
        geometry.placeCuboid(editor,[1,1,11],[2,1,11],Block("spruce_trapdoor",{"facing":"south","open":"true"}))

        geometry.placeCuboid(editor,[10,1,2],[11,1,10],Block("moss_block"))
        geometry.placeCuboid(editor,[10,2,2],[11,2,10],lists)
        geometry.placeCuboid(editor,[9,1,2],[9,1,10],Block("spruce_trapdoor",{"facing":"west","open":"true"}))
        geometry.placeCuboid(editor,[12,1,2],[12,1,10],Block("spruce_trapdoor",{"facing":"east","open":"true"}))
        geometry.placeCuboid(editor,[10,1,1],[11,1,1],Block("spruce_trapdoor",{"facing":"north","open":"true"}))
        geometry.placeCuboid(editor,[10,1,11],[11,1,11],Block("spruce_trapdoor",{"facing":"south","open":"true"}))

        #ベンチ
        geometry.placeCuboid(editor,[5,1,2],[7,1,2],Block("birch_stairs",{"facing":"north"}))
        editor.placeBlock([4,1,2],Block("birch_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([8,1,2],Block("birch_trapdoor",{"facing":"east","open":"true"}))
        geometry.placeCuboid(editor,[5,1,10],[7,1,10],Block("birch_stairs",{"facing":"south"}))
        editor.placeBlock([4,1,10],Block("birch_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([8,1,10],Block("birch_trapdoor",{"facing":"east","open":"true"}))

        #木
        geometry.placeCuboid(editor,[4,4,4],[8,4,8],Block("oak_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[5,5,5],[7,5,7],Block("oak_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[4,5,5],[4,5,7],Block("oak_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[5,5,4],[7,5,4],Block("oak_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[5,5,7],[7,5,7],Block("oak_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[7,5,4],[7,5,7],Block("oak_leaves",{"persistent":"true"})) 
        editor.placeBlock([6,6,6],Block("oak_leaves",{"persistent":"true"}))
        editor.placeBlock([5,6,6],Block("oak_leaves",{"persistent":"true"}))
        editor.placeBlock([6,6,5],Block("oak_leaves",{"persistent":"true"}))
        editor.placeBlock([6,6,7],Block("oak_leaves",{"persistent":"true"}))
        editor.placeBlock([7,6,6],Block("oak_leaves",{"persistent":"true"}))

        geometry.placeCuboid(editor,[6,1,6],[6,5,6],Block("oak_log",{"axis":"y"}))


        #照明
        light(editor,[0,1,0])
        light(editor,[6,1,0])
        light(editor,[0,1,12])
        light(editor,[12,1,0])
        light(editor,[6,1,12])
        light(editor,[12,1,12])
        editor.placeBlock([1,3,6],Block("lantern"))
        editor.placeBlock([11,3,6],Block("lantern"))
        editor.placeBlock([5,4,6],Block("oak_log",{"axis":"x"}))
        editor.placeBlock([7,4,6],Block("oak_log",{"axis":"x"}))
        editor.placeBlock([5,3,6],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([7,3,6],Block("lantern",{"hanging":"true"}))

        #パンダ
        if(random.random()<0.5):
            summon_animal(editor,[4,2,6],base_coor,c_rota,"panda","panda")
        if(random.random()<0.5):
            summon_animal(editor,[8,2,6],base_coor,c_rota,"panda","panda")



def light(editor,coor):
    editor.placeBlock(coor,Block("cobblestone_wall"))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]],Block("lantern"))
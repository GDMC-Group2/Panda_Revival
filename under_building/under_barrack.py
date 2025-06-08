from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_build import under_build_base,place_stand,place_frame,place_frame_up,\
place_door,place_bed,place_pot,summon_animal


#under_barrack
#設置位置:1層


def under_barrack(editor,coor,base_coor,build_rotation,rotation,size=[13,14,29]): 
    with editor.pushTransform(Transform(coor,rotation=build_rotation)):
        under_build_base(editor,coor,rotation,size)
        geometry.placeCuboid(editor,[0,0,0],[12,0,28],Block("sand"))

        geometry.placeCuboid(editor,[0,7,0],[12,7,28],Block("stone"))
        geometry.placeCuboid(editor,[0,8,0],[12,8,28],Block("birch_planks"))
        geometry.placeCuboid(editor,[0,1,13],[12,2,13],Block("birch_fence"))
        geometry.placeCuboid(editor,[5,2,13],[7,2,13],Block("air"))
        geometry.placeCuboid(editor,[5,1,13],[7,1,13],Block("birch_fence_gate",{"facing":"north"}))
        meele_target(editor,[2,1,10])
        meele_target(editor,[6,1,8])
        meele_target(editor,[10,1,10])
        range_target(editor,[2,1,25])
        range_target(editor,[6,1,27])
        range_target(editor,[10,1,25])
        range_target(editor,[4,1,21])
        range_target(editor,[8,1,21])
        editor.placeBlock([11,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([12,1,0],Block("chest",{"facing":"south","type":"left"}))

        stairs(editor)

        #2階
        geometry.placeCuboid(editor,[-1,9,0],[-1,14,28],Block("birch_planks"))
        geometry.placeCuboid(editor,[13,9,12],[13,14,28],Block("birch_planks"))
        geometry.placeCuboid(editor,[0,9,-1],[5,14,-1],Block("birch_planks"))
        geometry.placeCuboid(editor,[9,9,11],[12,14,11],Block("birch_planks"))
        geometry.placeCuboid(editor,[8,9,12],[8,14,28],Block("birch_planks"))
        geometry.placeCuboid(editor,[4,9,12],[4,14,28],Block("birch_planks"))
        geometry.placeCuboid(editor,[6,9,0],[6,14,5],Block("birch_planks"))
        geometry.placeCuboid(editor,[4,9,7],[4,14,10],Block("birch_planks"))
        geometry.placeCuboid(editor,[5,9,6],[5,14,6],Block("birch_planks"))
        geometry.placeCuboid(editor,[0,9,11],[3,14,11],Block("birch_planks"))

        geometry.placeCuboid(editor,[0,9,20],[3,14,20],Block("birch_planks"))
        geometry.placeCuboid(editor,[9,9,20],[12,14,20],Block("birch_planks"))


        geometry.placeCuboid(editor,[8,9,11],[8,14,11],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[4,9,11],[4,14,11],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[6,9,6],[6,14,6],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[4,9,6],[4,14,6],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[4,9,20],[4,14,20],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[8,9,20],[8,14,20],Block("spruce_log",{"axis":"y"}))


        place_door(editor,[6,9,2],"west","right","birch")
        place_door(editor,[6,9,3],"west","left","birch")
        place_door(editor,[4,9,15],"west","right","birch")
        place_door(editor,[4,9,16],"west","left","birch")
        place_door(editor,[4,9,24],"west","right","birch")
        place_door(editor,[4,9,25],"west","left","birch")

        place_door(editor,[8,9,15],"east","left","birch")
        place_door(editor,[8,9,16],"east","right","birch")
        place_door(editor,[8,9,24],"east","left","birch")
        place_door(editor,[8,9,25],"east","right","birch")

        room(editor,[0,9,12])
        room(editor,[12,9,12],True)
        room(editor,[0,9,21])
        room(editor,[12,9,21],True)

        #食堂
        geometry.placeCuboid(editor,[0,8,0],[5,8,5],Block("bamboo_mosaic")) 
        geometry.placeCuboid(editor,[1,10,1],[3,10,4],Block("spruce_trapdoor",{"facing":"west","half":"bottom"})) 
        editor.placeBlock([1,9,1],Block("spruce_fence"))
        editor.placeBlock([3,9,1],Block("spruce_fence"))
        editor.placeBlock([1,9,4],Block("spruce_fence"))
        editor.placeBlock([3,9,4],Block("spruce_fence"))
        geometry.placeCuboid(editor,[-1,9,6],[-1,14,6],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[0,9,6],[1,9,6],Block("stripped_birch_log",{"axis":"x"}))
        editor.placeBlock([2,9,6],Block("birch_trapdoor",{"facing":"east","half":"top"}))
        editor.placeBlock([3,9,6],Block("birch_trapdoor",{"facing":"west","half":"top"}))
        geometry.placeCuboid(editor,[3,10,10],[3,14,10],Block("cobblestone_wall"))
        editor.placeBlock([2,10,10],Block("cobblestone_wall"))
        geometry.placeCuboid(editor,[3,9,10],[2,9,10],Block("smoker",{"facing":"north"}))
        editor.placeBlock([0,9,9],Block("chest",{"facing":"east","type":"left"}))
        editor.placeBlock([0,9,10],Block("chest",{"facing":"east","type":"right"}))
        geometry.placeCuboid(editor,[0,11,10],[1,11,10],Block("birch_slab",{"type":"top"})) 
        geometry.placeCuboid(editor,[0,12,10],[1,12,10],Block("barrel",{"facing":"north"}))
        editor.placeBlock([0,12,6],Block("birch_fence"))
        editor.placeBlock([3,12,6],Block("birch_fence"))
        editor.placeBlock([0,13,6],Block("birch_stairs",{"facing":"west","half":"top"}))
        editor.placeBlock([1,14,6],Block("birch_stairs",{"facing":"west","half":"top"}))
        editor.placeBlock([3,13,6],Block("birch_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([2,14,6],Block("birch_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([0,14,6],Block("birch_planks"))
        editor.placeBlock([3,14,6],Block("birch_planks"))
        
        editor.placeBlock([2,14,3],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([2,14,2],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([1,14,3],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([3,14,3],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))
        editor.placeBlock([2,14,4],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([2,13,3],Block("chain",{"axis":"y"}))
        editor.placeBlock([2,12,3],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([3,12,8],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([3,13,8],Block("lantern"))
        editor.placeBlock([0,12,0],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([0,13,0],Block("lantern"))




        #壁装飾
        geometry.placeCuboid(editor,[5,9,29],[7,13,29],Block("air")) 
        geometry.placeCuboid(editor,[5,9,29],[7,9,29],Block("birch_planks"))
        geometry.placeCuboid(editor,[5,10,29],[7,10,29],Block("birch_leaves"))
        geometry.placeCuboid(editor,[4,9,29],[4,13,29],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[8,9,29],[8,13,29],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([5,14,29],Block("birch_stairs",{"facing":"west","half":"top"}))
        editor.placeBlock([7,14,29],Block("birch_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([6,14,29],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[5,9,30],[7,14,30],Block("polished_granite"))
        geometry.placeCuboid(editor,[6,9,30],[6,10,30],Block("polished_diorite"))
        geometry.placeCuboid(editor,[5,11,30],[5,12,30],Block("polished_diorite"))
        geometry.placeCuboid(editor,[7,11,30],[7,12,30],Block("polished_diorite"))
        geometry.placeCuboid(editor,[6,13,30],[6,14,30],Block("polished_diorite"))
        editor.placeBlock([6,13,30],Block("polished_diorite"))

        #照明
        editor.placeBlock([10,1,0],Block("lantern"))

        editor.placeBlock([5,12,20],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([5,13,20],Block("lantern"))
        editor.placeBlock([7,12,20],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([7,13,20],Block("lantern"))
        editor.placeBlock([5,12,11],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([5,13,11],Block("lantern"))
        editor.placeBlock([7,12,11],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([7,13,11],Block("lantern"))
        editor.placeBlock([5,12,7],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([5,13,7],Block("lantern"))
        editor.placeBlock([5,12,0],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([5,13,0],Block("lantern"))

        editor.placeBlock([5,9,28],Block("cobblestone_wall"))
        editor.placeBlock([5,10,28],Block("lantern"))
        editor.placeBlock([7,9,28],Block("cobblestone_wall"))
        editor.placeBlock([7,10,28],Block("lantern"))

        editor.placeBlock([6,14,16],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([6,14,15],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([5,14,16],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([7,14,16],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))
        editor.placeBlock([6,14,17],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([6,13,16],Block("chain",{"axis":"y"}))
        editor.placeBlock([6,12,16],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([6,14,24],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([6,14,23],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([5,14,24],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([7,14,24],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))
        editor.placeBlock([6,14,25],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([6,13,24],Block("chain",{"axis":"y"}))
        editor.placeBlock([6,12,24],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([3,6,4],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([3,6,3],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([2,6,4],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([4,6,4],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))
        editor.placeBlock([3,6,5],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([3,5,4],Block("chain",{"axis":"y"}))
        editor.placeBlock([3,4,4],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([10,10,0],Block("lantern"))
        editor.placeBlock([10,10,6],Block("lantern"))
        editor.placeBlock([2,3,13],Block("lantern"))
        editor.placeBlock([10,3,13],Block("lantern"))
        editor.placeBlock([7,3,2],Block("lantern"))

        editor.placeBlock([12,6,1],Block("wall_torch",{"facing":"west"}))
        editor.placeBlock([6,1,16],Block("torch"))
        editor.placeBlock([0,1,18],Block("torch"))
        editor.placeBlock([12,1,18],Block("torch"))
        for i in range(2):
            summon_animal(editor,[3,2,6],base_coor,rotation,"panda","panda")
        summon_animal(editor,[2,10,8],base_coor,rotation,"panda","panda")
        for i in range(3):
            summon_animal(editor,[6,9,15],base_coor,rotation,"panda","panda")            


def stairs(editor):
    geometry.placeCuboid(editor,[11,7,0],[12,8,4],Block("air")) 
    geometry.placeCuboid(editor,[11,8,5],[12,8,5],Block("air")) 
    geometry.placeCuboid(editor,[8,1,0],[8,1,1],Block("birch_stairs",{"facing":"east"}))
    geometry.placeCuboid(editor,[9,1,0],[9,1,1],Block("birch_stairs",{"facing":"west","half":"top"}))
    geometry.placeCuboid(editor,[9,2,0],[9,2,1],Block("birch_stairs",{"facing":"east"}))
    geometry.placeCuboid(editor,[10,2,0],[10,2,1],Block("birch_stairs",{"facing":"west","half":"top"}))
    geometry.placeCuboid(editor,[10,3,0],[10,3,1],Block("birch_stairs",{"facing":"east"}))
    geometry.placeCuboid(editor,[11,3,0],[12,3,1],Block("birch_planks"))
    geometry.placeCuboid(editor,[11,4,2],[12,4,2],Block("birch_stairs",{"facing":"south"}))
    geometry.placeCuboid(editor,[11,3,2],[12,3,2],Block("birch_stairs",{"facing":"north","half":"top"}))
    geometry.placeCuboid(editor,[11,5,3],[12,5,3],Block("birch_stairs",{"facing":"south"}))
    geometry.placeCuboid(editor,[11,4,3],[12,4,3],Block("birch_stairs",{"facing":"north","half":"top"}))
    geometry.placeCuboid(editor,[11,6,4],[12,6,4],Block("birch_stairs",{"facing":"south"}))
    geometry.placeCuboid(editor,[11,5,4],[12,5,4],Block("birch_stairs",{"facing":"north","half":"top"}))
    geometry.placeCuboid(editor,[11,7,5],[12,7,5],Block("birch_stairs",{"facing":"south"}))
    geometry.placeCuboid(editor,[11,6,5],[12,6,5],Block("birch_stairs",{"facing":"north","half":"top"}))
    geometry.placeCuboid(editor,[11,8,6],[12,8,6],Block("birch_stairs",{"facing":"south"}))
    geometry.placeCuboid(editor,[8,1,2],[10,6,2],Block("birch_fence")) 
    geometry.placeCuboid(editor,[7,1,2],[7,2,2],Block("birch_fence")) 
    geometry.placeCuboid(editor,[10,4,3],[10,6,4],Block("birch_fence")) 
    geometry.placeCuboid(editor,[10,5,5],[10,6,5],Block("birch_fence")) 
    geometry.placeCuboid(editor,[10,9,0],[10,9,6],Block("birch_fence")) 


def meele_target(editor,coor):
    editor.placeBlock(coor,Block("birch_fence"))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]],Block("hay_block"))
    editor.placeBlock([coor[0]-1,coor[1]+1,coor[2]],Block("birch_fence"))
    editor.placeBlock([coor[0]+1,coor[1]+1,coor[2]],Block("birch_fence"))
    editor.placeBlock([coor[0],coor[1]+2,coor[2]],Block("carved_pumpkin",{"facing":"north"}))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]+1],Block("wall_torch",{"facing":"south"}))

def range_target(editor,coor):
    editor.placeBlock(coor,Block("birch_fence"))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]],Block("redstone_lamp"))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]-1],Block("birch_button",{"face":"wall","facing":"north"}))
    editor.placeBlock([coor[0]-1,coor[1]+1,coor[2]],Block("birch_fence"))
    editor.placeBlock([coor[0]+1,coor[1]+1,coor[2]],Block("birch_fence"))
    editor.placeBlock([coor[0],coor[1]+2,coor[2]],Block("carved_pumpkin",{"facing":"north"}))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]+1],Block("wall_torch",{"facing":"south"}))

def room(editor,coor,mirror=False):
    with editor.pushTransform(Transform(coor,flip=(mirror,False,False))):
        #各部屋の設計
        #座標は左下(x,z最小)を基準
        place_bed(editor,[0,0,2],"north")
        place_bed(editor,[1,0,2],"north")
        place_bed(editor,[0,3,2],"north")
        place_bed(editor,[1,3,2],"north")
        place_bed(editor,[0,0,5],"south")
        place_bed(editor,[1,0,5],"south")
        place_bed(editor,[0,3,5],"south")
        place_bed(editor,[1,3,5],"south")
        geometry.placeCuboid(editor,[2,0,3],[2,0,4],Block("birch_stairs",{"facing":"west"}))
        geometry.placeCuboid(editor,[1,1,3],[1,1,4],Block("birch_stairs",{"facing":"west"}))
        geometry.placeCuboid(editor,[0,2,3],[0,2,4],Block("birch_stairs",{"facing":"west"}))
        geometry.placeCuboid(editor,[0,0,0],[1,0,0],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[0,3,0],[1,3,0],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[0,0,7],[1,0,7],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[0,3,7],[1,3,7],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[0,2,0],[1,2,2],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[0,2,5],[1,2,7],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[2,3,0],[2,3,2],Block("birch_fence"))
        geometry.placeCuboid(editor,[2,3,5],[2,3,7],Block("birch_fence"))
        geometry.placeCuboid(editor,[0,0,3],[1,0,3],Block("barrel",{"facing":"north"}))
        geometry.placeCuboid(editor,[0,0,4],[1,0,4],Block("barrel",{"facing":"south"}))
        editor.placeBlock([0,1,3],Block("barrel",{"facing":"north"}))
        editor.placeBlock([0,1,4],Block("barrel",{"facing":"south"}))
        place_pot(editor,[0,1,0],"bamboo")
        place_pot(editor,[0,4,0],"bamboo")
        place_pot(editor,[0,1,7],"bamboo")
        place_pot(editor,[0,4,7],"bamboo")
        editor.placeBlock([3,2,1],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([3,3,1],Block("lantern"))
        editor.placeBlock([3,2,6],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([3,3,6],Block("lantern"))





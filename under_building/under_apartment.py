from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_build import under_build_base,place_door,place_bed,place_pot


def under_apartment(editor,coor):
    #建材を変更できる
    #wood
    #piller
    #wall
    color_list=["black","gray","light_gray","blue","green","cyan","red","purple",
            "brown","orange","lime","yellow","light_blue","magenta","pink","white"]
    wood_list=["bamboo","birch"]
    piller_list=["spruce_log","stone_bricks","polished_andesite","stripped_birch_log"]
    wall_list=["polished_diorite","polished_granite"]
    choice_wood=random.choice(wood_list)
    floor_wood=choice_wood+"_planks"
    fence_wood=choice_wood+"_fence"
    stair_wood=choice_wood+"_stairs"
    sigh_wood=choice_wood+"_wall_hanging_sign"
    piller=random.choice(piller_list)
    wall=random.choice(wall_list)

    with editor.pushTransform(Transform(coor)):
        geometry.placeCuboid(editor,[0,0,0],[12,0,12],Block(floor_wood))

        geometry.placeCuboid(editor,[0,1,1],[0,5,11],Block(wall)) 
        geometry.placeCuboid(editor,[1,1,0],[11,5,0],Block(wall)) 
        geometry.placeCuboid(editor,[12,1,1],[12,5,11],Block(wall)) 
        geometry.placeCuboid(editor,[1,1,12],[11,5,12],Block(wall)) 
        geometry.placeCuboid(editor,[1,6,1],[11,6,11],Block(wall)) 
        geometry.placeCuboid(editor,[6,1,1],[6,5,11],Block(wall)) 
        geometry.placeCuboid(editor,[1,1,6],[11,5,6],Block(wall)) 
        #縦柱
        geometry.placeCuboid(editor,[0,1,0],[0,6,0],Block(piller)) 
        geometry.placeCuboid(editor,[0,1,12],[0,6,12],Block(piller)) 
        geometry.placeCuboid(editor,[12,1,0],[12,6,0],Block(piller)) 
        geometry.placeCuboid(editor,[12,1,12],[12,6,12],Block(piller)) 
        geometry.placeCuboid(editor,[6,1,0],[6,6,0],Block(piller)) 
        geometry.placeCuboid(editor,[6,1,12],[6,6,12],Block(piller)) 
        geometry.placeCuboid(editor,[0,1,6],[0,6,6],Block(piller)) 
        geometry.placeCuboid(editor,[12,1,6],[12,6,6],Block(piller)) 
        #横柱
        geometry.placeCuboid(editor,[0,6,0],[0,6,12],Block(piller)) 
        geometry.placeCuboid(editor,[0,6,0],[12,6,0],Block(piller)) 
        geometry.placeCuboid(editor,[12,6,0],[12,6,12],Block(piller)) 
        geometry.placeCuboid(editor,[0,6,12],[12,6,12],Block(piller)) 

        place_door(editor,[0,1,2],"east","left",choice_wood)
        place_door(editor,[0,1,3],"east","right",choice_wood)
        place_door(editor,[0,1,9],"east","left",choice_wood)
        place_door(editor,[0,1,10],"east","right",choice_wood)
        place_door(editor,[12,1,2],"west","right",choice_wood)
        place_door(editor,[12,1,3],"west","left",choice_wood)
        place_door(editor,[12,1,9],"west","right",choice_wood)
        place_door(editor,[12,1,10],"west","left",choice_wood)
        #窓
        geometry.placeCuboid(editor,[3,2,0],[4,3,0],Block(fence_wood)) 
        geometry.placeCuboid(editor,[3,2,12],[4,3,12],Block(fence_wood)) 
        geometry.placeCuboid(editor,[8,2,0],[9,3,0],Block(fence_wood)) 
        geometry.placeCuboid(editor,[8,2,12],[9,3,12],Block(fence_wood)) 


        #表札:名前を書きたい

        editor.placeBlock([-1,3,4],Block(sigh_wood,{"facing":"north"}))
        editor.placeBlock([-1,3,11],Block(sigh_wood,{"facing":"north"}))
        editor.placeBlock([13,3,1],Block(sigh_wood,{"facing":"south"}))
        editor.placeBlock([13,3,8],Block(sigh_wood,{"facing":"south"}))




        #照明(外)
        outer_light(editor,[-1,4,0],choice_wood)
        outer_light(editor,[-1,4,6],choice_wood)
        outer_light(editor,[0,4,13],choice_wood)
        outer_light(editor,[6,4,13],choice_wood)
        outer_light(editor,[13,4,12],choice_wood)
        outer_light(editor,[13,4,6],choice_wood)
        outer_light(editor,[6,4,-1],choice_wood)
        outer_light(editor,[12,4,-1],choice_wood)
        editor.placeBlock([6,7,6],Block("lantern"))
        #内装
        color=random.choice(color_list)
        place_bed(editor,[4,1,4],"east",color)
        place_bed(editor,[4,1,5],"east",color)
        geometry.placeCuboid(editor,[3,1,1],[4,1,1],Block(stair_wood,{"facing":"north","half":"top"})) 
        editor.placeBlock([1,1,1],Block("crafting_table"))
        editor.placeBlock([2,1,1],Block("furnace",{"facing":"south"}))
        geometry.placeCuboid(editor,[1,1,4],[1,2,4],Block("chest",{"facing":"east","type":"left"})) 
        geometry.placeCuboid(editor,[1,1,5],[1,2,5],Block("chest",{"facing":"east","type":"right"})) 
        on_table(editor,[3,2,1])
        interior(editor,[5,1,1])
        inner_light(editor,[1,3,1],choice_wood)
        inner_light(editor,[5,3,5],choice_wood)

        color=random.choice(color_list)
        place_bed(editor,[4,1,7],"east",color)
        place_bed(editor,[4,1,8],"east",color)
        geometry.placeCuboid(editor,[3,1,11],[4,1,11],Block(stair_wood,{"facing":"south","half":"top"})) 
        editor.placeBlock([1,1,11],Block("crafting_table"))
        editor.placeBlock([2,1,11],Block("furnace",{"facing":"north"}))
        geometry.placeCuboid(editor,[1,1,7],[1,2,7],Block("chest",{"facing":"east","type":"left"})) 
        geometry.placeCuboid(editor,[1,1,8],[1,2,8],Block("chest",{"facing":"east","type":"right"})) 
        on_table(editor,[3,2,11])
        interior(editor,[5,1,11])
        inner_light(editor,[1,3,11],choice_wood)
        inner_light(editor,[5,3,7],choice_wood)

        color=random.choice(color_list)
        place_bed(editor,[8,1,4],"west",color)
        place_bed(editor,[8,1,5],"west",color)
        geometry.placeCuboid(editor,[8,1,1],[9,1,1],Block(stair_wood,{"facing":"north","half":"top"})) 
        editor.placeBlock([11,1,1],Block("crafting_table"))
        editor.placeBlock([10,1,1],Block("furnace",{"facing":"south"}))
        geometry.placeCuboid(editor,[11,1,5],[11,2,5],Block("chest",{"facing":"west","type":"left"})) 
        geometry.placeCuboid(editor,[11,1,4],[11,2,4],Block("chest",{"facing":"west","type":"right"})) 
        on_table(editor,[9,2,1])
        interior(editor,[7,1,1])
        inner_light(editor,[11,3,1],choice_wood)
        inner_light(editor,[7,3,5],choice_wood)
    
        color=random.choice(color_list)
        place_bed(editor,[8,1,7],"west",color)
        place_bed(editor,[8,1,8],"west",color)
        geometry.placeCuboid(editor,[8,1,11],[9,1,11],Block(stair_wood,{"facing":"south","half":"top"})) 
        editor.placeBlock([11,1,11],Block("crafting_table"))
        editor.placeBlock([10,1,11],Block("furnace",{"facing":"north"}))
        geometry.placeCuboid(editor,[11,1,8],[11,2,8],Block("chest",{"facing":"west","type":"left"})) 
        geometry.placeCuboid(editor,[11,1,7],[11,2,7],Block("chest",{"facing":"west","type":"right"})) 
        on_table(editor,[9,2,11])
        interior(editor,[7,1,11])
        inner_light(editor,[7,3,7],choice_wood)
        inner_light(editor,[11,3,11],choice_wood)

def on_table(editor,coor):
    #机の上に置くもの
    #置かない,ポット,ろうそく,
    table_list=["none","pot","candle"]
    flower_list=["bamboo","red_mushroom","brown_mushroom","dandelion","poppy","birch_sapling",
            "red_tulip","orange_tulip","white_tulip","pink_tulip","oxeye_daisy","cornflower","lily_of_the_valley"]
    table=random.choice(table_list)
    if(table=="pot"):
        flower=random.choice(flower_list)
        place_pot(editor,coor,flower)
    elif(table=="candle"):
        editor.placeBlock(coor,Block("candle",{"candles":"3","lit":"true"}))


def interior(editor,coor):
    #インテリア
    #観葉植物,レコード,服
    interior_list=["plant","jukebox"]
    inte=random.choice(interior_list)
    if(inte=="plant"):
        editor.placeBlock(coor,Block("composter",{"level":"6"}))
        geometry.placeCuboid(editor,[coor[0],coor[1]+1,coor[2]],[coor[0],coor[1]+2,coor[2]],Block("birch_leaves",{"persistent":"true"})) 
    elif(inte=="jukebox"):
        editor.placeBlock(coor,Block("jukebox"))

def outer_light(editor,coor,choice_wood):
    #外側の明かり
    x=coor[0]
    y=coor[1]
    z=coor[2]
    half=choice_wood+"_slab"
    editor.placeBlock([x,y,z],Block(half,{"type":"bottom"}))
    editor.placeBlock([x,y-1,z],Block("lantern",{"hanging":"true"}))


def inner_light(editor,coor,choice_wood):
    #内側の明かり
    x=coor[0]
    y=coor[1]
    z=coor[2]
    half=choice_wood+"_slab"
    editor.placeBlock([x,y,z],Block(half,{"type":"top"}))
    editor.placeBlock([x,y+1,z],Block("lantern"))


from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_building.under_build import under_build_base,place_stand,place_frame,place_frame_up,summon_animal



def under_blacksmith(editor,coor,base_coor,build_rotation,rotation,size=[13,7,13]):
    with editor.pushTransform(Transform(coor,rotation=build_rotation)):
        under_build_base(editor,coor,rotation,size)
        geometry.placeCuboid(editor,[0,0,0],[12,0,12],Block("polished_andesite"))
        for i in range(2):
            for j in range(2):
                geometry.placeCuboid(editor,[0+i*8,0,0+j*8],[4+i*8,0,4+j*8],Block("polished_granite"))
                geometry.placeCuboid(editor,[0+i*9,0,0+j*9],[3+i*9,0,3+j*9],Block("polished_diorite"))
        big_furnace(editor)
        forge(editor)
        ore(editor)
        display(editor,base_coor,rotation)
        editor.placeBlock([4,1,4],Block("cobblestone_wall"))
        editor.placeBlock([4,2,4],Block("lantern"))
        editor.placeBlock([8,1,4],Block("cobblestone_wall"))
        editor.placeBlock([8,2,4],Block("lantern"))
        editor.placeBlock([8,1,8],Block("cobblestone_wall"))
        editor.placeBlock([8,2,8],Block("lantern"))
        for i in range(3):
            summon_animal(editor,[6,2,6],base_coor,rotation,"panda","panda")

def ore(editor,ore_type="raw_iron_block"):
    geometry.placeCuboid(editor,[9,1,8],[12,1,8],Block("spruce_trapdoor",{"facing":"north","half":"bottom","open":"true"}))
    geometry.placeCuboid(editor,[8,1,9],[8,1,12],Block("spruce_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
    geometry.placeCuboid(editor,[9,1,9],[12,1,10],Block(ore_type))
    geometry.placeCuboid(editor,[10,2,9],[12,2,10],Block(ore_type))
    geometry.placeCuboid(editor,[12,3,9],[12,3,10],Block(ore_type))
    editor.placeBlock([11,3,9],Block(ore_type))

    geometry.placeCuboid(editor,[9,1,11],[12,1,12],Block("coal_block"))
    geometry.placeCuboid(editor,[11,2,11],[12,2,12],Block("coal_block"))
    editor.placeBlock([10,2,11],Block("coal_block"))
    geometry.placeCuboid(editor,[12,3,11],[12,3,12],Block("coal_block"))
    editor.placeBlock([11,3,12],Block("coal_block"))
    editor.placeBlock([12,4,12],Block("birch_slab",{"type":"top"}))
    editor.placeBlock([12,5,12],Block("lantern"))


def forge(editor,stone="deepslate_tile"):
    brick=Block(stone+"s")    
    wall=Block(stone+"_wall")
    half=stone+"_slab"
    geometry.placeCuboid(editor,[-1,1,1],[-1,4,4],brick)
    geometry.placeCuboid(editor,[1,1,-1],[4,4,-1],brick)
    geometry.placeCuboid(editor,[0,1,0],[0,4,0],Block("lava"))
    geometry.placeCuboid(editor,[1,2,0],[1,3,0],wall)
    geometry.placeCuboid(editor,[4,2,0],[4,3,0],wall)
    geometry.placeCuboid(editor,[0,2,1],[0,3,1],wall)
    geometry.placeCuboid(editor,[0,2,4],[0,3,4],wall)
    geometry.placeCuboid(editor,[1,5,0],[4,5,0],Block(half))
    geometry.placeCuboid(editor,[0,5,1],[0,5,4],Block(half))
    editor.placeBlock([0,5,0],brick)
    editor.placeBlock([0,6,0],Block("lantern"))
    editor.placeBlock([1,1,0],Block("blast_furnace",{"facing":"south"}))
    editor.placeBlock([4,1,0],Block("blast_furnace",{"facing":"south"}))
    editor.placeBlock([1,4,0],Block("blast_furnace",{"facing":"south"}))
    editor.placeBlock([4,4,0],Block("blast_furnace",{"facing":"south"}))
    editor.placeBlock([0,1,1],Block("blast_furnace",{"facing":"east"}))
    editor.placeBlock([0,1,4],Block("blast_furnace",{"facing":"east"}))
    editor.placeBlock([0,4,1],Block("blast_furnace",{"facing":"east"}))
    editor.placeBlock([0,4,4],Block("blast_furnace",{"facing":"east"}))
    geometry.placeCuboid(editor,[2,3,0],[3,3,0],Block("polished_diorite_slab",{"type":"top"}))
    editor.placeBlock([2,4,0],Block("chest",{"facing":"south","type":"right"}))
    editor.placeBlock([3,4,0],Block("chest",{"facing":"south","type":"left"}))
    geometry.placeCuboid(editor,[0,3,2],[0,3,3],Block("polished_diorite_slab",{"type":"top"}))
    editor.placeBlock([0,4,2],Block("chest",{"facing":"east","type":"left"}))
    editor.placeBlock([0,4,3],Block("chest",{"facing":"east","type":"right"}))
    editor.placeBlock([2,1,0],Block("anvil",{"facing":"east"}))
    editor.placeBlock([3,1,0],Block("anvil",{"facing":"east"}))
    editor.placeBlock([0,1,2],Block("grindstone",{"facing":"east"}))
    editor.placeBlock([0,1,3],Block("stonecutter",{"facing":"east"}))
    
    editor.placeBlock([2,0,2],Block("crafting_table"))
    editor.placeBlock([3,1,3],Block("water_cauldron",{"level":"3"}))

def big_furnace(editor,stone="deepslate_tile"):
    brick=Block(stone+"s")
    wall=Block(stone+"_wall")
    stairs=stone+"_stairs"
    half=stone+"_slab"
    geometry.placeCuboid(editor,[-1,2,10],[-1,5,12],brick)
    geometry.placeCuboid(editor,[0,2,13],[2,5,13],brick)
    geometry.placeCuboid(editor,[0,1,9],[0,4,9],brick)
    geometry.placeCuboid(editor,[3,1,12],[3,4,12],brick)
    geometry.placeCuboid(editor,[0,1,8],[0,4,8],wall)
    geometry.placeCuboid(editor,[4,1,12],[4,4,12],wall)
    geometry.placeCuboid(editor,[1,1,9],[2,1,9],Block(stairs,{"facing":"south"}))
    geometry.placeCuboid(editor,[1,4,9],[2,4,9],Block(stairs,{"facing":"south","half":"top"}))
    geometry.placeCuboid(editor,[0,5,9],[2,5,9],Block(stairs,{"facing":"south"}))
    geometry.placeCuboid(editor,[3,1,10],[3,1,11],Block(stairs,{"facing":"west"}))
    geometry.placeCuboid(editor,[3,4,10],[3,4,11],Block(stairs,{"facing":"west","half":"top"}))
    geometry.placeCuboid(editor,[3,5,10],[3,5,12],Block(stairs,{"facing":"west"}))
    editor.placeBlock([3,1,9],Block(stairs,{"facing":"south","shape":"outer_right"}))
    editor.placeBlock([3,4,9],Block(stairs,{"facing":"south","half":"top","shape":"outer_right"}))
    editor.placeBlock([3,5,9],Block(stairs,{"facing":"south","shape":"outer_right"}))
    geometry.placeCuboid(editor,[0,6,10],[2,6,12],Block(half))
    editor.placeBlock([1,6,11],brick)
    editor.placeBlock([1,7,11],Block("lantern"))

    #fire
    geometry.placeCuboid(editor,[1,2,9],[2,3,9],Block("iron_bars"))
    geometry.placeCuboid(editor,[3,2,10],[3,3,11],Block("iron_bars"))
    editor.placeBlock([3,3,9],Block("iron_bars"))
    geometry.placeCuboid(editor,[0,1,10],[2,1,12],Block("netherrack"))
    geometry.placeCuboid(editor,[0,2,10],[2,2,12],Block("fire"))

def display(editor,coor,rotation):
    geometry.placeCuboid(editor,[8,1,-1],[8,5,-1],Block("polished_deepslate"))
    geometry.placeCuboid(editor,[13,1,4],[13,5,4],Block("polished_deepslate"))
    geometry.placeCuboid(editor,[9,5,-1],[13,5,-1],Block("polished_deepslate"))
    geometry.placeCuboid(editor,[13,5,-0],[13,5,4],Block("polished_deepslate"))

    geometry.placeCuboid(editor,[9,1,-1],[12,4,-1],Block("polished_tuff"))
    geometry.placeCuboid(editor,[13,1,0],[13,4,3],Block("polished_tuff"))
    place_stand(editor,[12,1,0],coor,rotation,"west","diamond_boots","diamond_leggings","diamond_chestplate","diamond_helmet")
    place_stand(editor,[12,1,1],coor,rotation,"west","chainmail_boots","chainmail_leggings","chainmail_chestplate","chainmail_helmet")
    place_stand(editor,[12,1,2],coor,rotation,"west","iron_boots","iron_leggings","iron_chestplate","iron_helmet")
    place_stand(editor,[12,1,3],coor,rotation,"west","chainmail_boots","chainmail_leggings","chainmail_chestplate","chainmail_helmet")
    place_frame(editor,[9,2,0],coor,rotation,"south","iron_sword")
    place_frame(editor,[10,2,0],coor,rotation,"south","iron_pickaxe")
    place_frame(editor,[11,2,0],coor,rotation,"south","bucket")
    place_frame(editor,[9,3,0],coor,rotation,"south","iron_hoe")
    place_frame(editor,[10,3,0],coor,rotation,"south","iron_shovel")
    place_frame(editor,[11,3,0],coor,rotation,"south","iron_axe")
    geometry.placeCuboid(editor,[10,1,1],[10,1,2],Block("polished_tuff"))
    place_frame_up(editor,[10,2,1],coor,rotation,"diamond_sword",True)
    place_frame_up(editor,[10,2,2],coor,rotation,"diamond_pickaxe",True)
    editor.placeBlock([12,4,0],Block("birch_slab",{"type":"top"}))
    editor.placeBlock([12,5,0],Block("lantern"))


from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_build import under_build_base,place_door,place_bed,place_pot,place_paint
from under_apartment import under_apartment


def under_well(editor,coor):
    #床
    with editor.pushTransform(Transform(coor)):
        geometry.placeCuboid(editor,[0,0,5],[3,0,7],Block("smooth_stone"))
        geometry.placeCuboid(editor,[5,0,0],[7,0,3],Block("smooth_stone"))
        geometry.placeCuboid(editor,[5,0,9],[7,0,12],Block("smooth_stone"))
        geometry.placeCuboid(editor,[9,0,5],[12,0,7],Block("smooth_stone"))
    #照明
        light(editor,[0,1,4])
        light(editor,[0,1,8])
        light(editor,[4,1,0])
        light(editor,[8,1,0])
        light(editor,[4,1,12])
        light(editor,[8,1,12])
        light(editor,[12,1,4])
        light(editor,[12,1,8])


    #井戸
        geometry.placeCuboid(editor,[4,1,5],[4,1,7],Block("polished_andesite_stairs",{"facing":"east"}))
        geometry.placeCuboid(editor,[5,1,4],[7,1,4],Block("polished_andesite_stairs",{"facing":"south"}))
        geometry.placeCuboid(editor,[5,1,8],[7,1,8],Block("polished_andesite_stairs",{"facing":"north"}))
        geometry.placeCuboid(editor,[8,1,5],[8,1,7],Block("polished_andesite_stairs",{"facing":"west"}))
        editor.placeBlock([4,1,4],Block("chiseled_stone_bricks"))
        editor.placeBlock([4,1,8],Block("chiseled_stone_bricks"))
        editor.placeBlock([8,1,4],Block("chiseled_stone_bricks"))
        editor.placeBlock([8,1,8],Block("chiseled_stone_bricks"))
        editor.placeBlock([4,2,4],Block("andesite_wall"))
        editor.placeBlock([4,2,8],Block("andesite_wall"))
        editor.placeBlock([8,2,4],Block("andesite_wall"))
        editor.placeBlock([8,2,8],Block("andesite_wall"))
        editor.placeBlock([3,1,4],Block("bamboo_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([3,1,8],Block("bamboo_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([4,1,3],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
        editor.placeBlock([8,1,3],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
        editor.placeBlock([4,1,9],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
        editor.placeBlock([8,1,9],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
        editor.placeBlock([9,1,4],Block("bamboo_trapdoor",{"facing":"east","open":"true"}))
        editor.placeBlock([9,1,8],Block("bamboo_trapdoor",{"facing":"east","open":"true"}))

        geometry.placeCuboid(editor,[4,3,4],[4,4,4],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[4,3,8],[4,4,8],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[8,3,4],[8,4,4],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[8,3,8],[8,4,8],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[4,4,5],[4,4,7],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[5,4,4],[7,4,4],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[5,4,8],[7,4,8],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[8,4,5],[8,4,7],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[4,5,4],[8,5,8],Block("bamboo_slab",{"type":"bottom"}))

        geometry.placeCuboid(editor,[3,5,5],[3,5,7],Block("bamboo_trapdoor",{"facing":"west","half":"bottom"}))
        geometry.placeCuboid(editor,[5,5,3],[7,5,3],Block("bamboo_trapdoor",{"facing":"north","half":"bottom"}))
        geometry.placeCuboid(editor,[5,5,9],[7,5,9],Block("bamboo_trapdoor",{"facing":"south","half":"bottom"}))
        geometry.placeCuboid(editor,[9,5,5],[9,5,7],Block("bamboo_trapdoor",{"facing":"east","half":"bottom"}))

        editor.placeBlock([4,5,6],Block("bamboo_planks"))
        editor.placeBlock([4,6,6],Block("lantern"))
        editor.placeBlock([6,5,4],Block("bamboo_planks"))
        editor.placeBlock([6,5,8],Block("bamboo_planks"))
        editor.placeBlock([8,5,6],Block("bamboo_planks"))
        editor.placeBlock([8,6,6],Block("lantern"))
        geometry.placeCuboid(editor,[5,5,5],[7,5,7],Block("bamboo_planks"))
        editor.placeBlock([6,6,6],Block("bamboo_planks"))
        editor.placeBlock([6,7,6],Block("lantern"))
        editor.placeBlock([5,6,6],Block("bamboo_slab"))
        editor.placeBlock([7,6,6],Block("bamboo_slab"))
        editor.placeBlock([6,6,5],Block("bamboo_slab"))
        editor.placeBlock([6,6,7],Block("bamboo_slab"))


        editor.placeBlock([6,4,5],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([6,4,7],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([6,5,6],Block("grindstone",{"face":"ceiling","facing":"west"}))
        geometry.placeCuboid(editor,[6,2,6],[6,4,6],Block("chain"))
        editor.placeBlock([6,1,6],Block("cauldron"))
        geometry.placeCuboid(editor,[0,1,0],[0,1,3],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[0,1,9],[0,1,12],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[12,1,0],[12,1,3],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[12,1,9],[12,1,12],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[0,1,0],[3,1,0],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[9,1,0],[12,1,0],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[0,1,12],[3,1,12],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[9,1,12],[12,1,12],Block("birch_leaves",{"persistent":"true"}))




    #地下水
        stone_list=[Block("stone"),Block("cobblestone")]
        geometry.placeCuboid(editor,[4,0,5],[4,-2,7],stone_list)
        geometry.placeCuboid(editor,[5,0,4],[7,-2,4],stone_list)
        geometry.placeCuboid(editor,[5,0,8],[7,-2,8],stone_list)
        geometry.placeCuboid(editor,[8,0,5],[8,-2,7],stone_list)
        geometry.placeCuboid(editor,[5,-3,5],[7,-3,7],stone_list)
        geometry.placeCuboid(editor,[5,-2,5],[7,-2,7],Block("water"))




def light(editor,coor):
    editor.placeBlock(coor,Block("cobblestone_wall"))
    editor.placeBlock([coor[0],coor[1]+1,coor[2]],Block("lantern"))
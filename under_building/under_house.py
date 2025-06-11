from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_building.under_build import under_build_base,place_door,place_bed,place_pot,place_paint,summon_animal





color_list=["black","gray","light_gray","blue","green","cyan","red","purple",
        "brown","orange","lime","yellow","light_blue","magenta","pink","white"]

def under_house_1(editor,coor,base_coor,b_rota,c_rota):

    with editor.pushTransform(Transform(coor,rotation=b_rota)):
        #外の装飾
        geometry.placeCuboid(editor,[0,1,0],[0,1,6],Block("bricks"))
        geometry.placeCuboid(editor,[0,2,0],[0,2,6],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[-1,1,0],[-1,1,6],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([0,1,-1],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([0,1,7],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))        
        geometry.placeCuboid(editor,[0,1,12],[4,1,12],Block("bricks"))
        geometry.placeCuboid(editor,[0,2,12],[4,2,12],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[0,1,13],[4,1,13],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([-1,1,12],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([5,1,12],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))        
        geometry.placeCuboid(editor,[8,1,12],[12,1,12],Block("bricks"))
        geometry.placeCuboid(editor,[8,2,12],[12,2,12],Block("birch_leaves",{"persistent":"true"}))
        geometry.placeCuboid(editor,[8,1,13],[12,1,13],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))       
        editor.placeBlock([7,1,12],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([13,1,12],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))   

        #屋根
        geometry.placeCuboid(editor,[2,6,1],[11,6,10],Block("polished_andesite"))
        geometry.placeCuboid(editor,[0,6,0],[0,6,11],Block("polished_andesite_stairs",{"facing":"east","half":"top"}))
        geometry.placeCuboid(editor,[1,6,12],[12,6,12],Block("polished_andesite_stairs",{"facing":"north","half":"top"}))
        geometry.placeCuboid(editor,[13,6,0],[13,6,11],Block("polished_andesite_stairs",{"facing":"west","half":"top"}))
        geometry.placeCuboid(editor,[1,6,-1],[12,6,-1],Block("polished_andesite_stairs",{"facing":"south","half":"top"}))
        editor.placeBlock([0,6,-1],Block("polished_andesite_stairs",{"facing":"east","half":"top","shape":"outer_right"}))
        editor.placeBlock([0,6,12],Block("polished_andesite_stairs",{"facing":"east","half":"top","shape":"outer_left"}))
        editor.placeBlock([13,6,12],Block("polished_andesite_stairs",{"facing":"west","half":"top","shape":"outer_right"}))
        editor.placeBlock([13,6,-1],Block("polished_andesite_stairs",{"facing":"west","half":"top","shape":"outer_left"}))

        #壁
        geometry.placeCuboid(editor,[1,1,0],[12,6,0],Block("polished_diorite"))
        geometry.placeCuboid(editor,[1,1,0],[1,6,11],Block("polished_diorite"))
        geometry.placeCuboid(editor,[1,1,11],[12,6,11],Block("polished_diorite"))
        geometry.placeCuboid(editor,[12,1,0],[12,6,11],Block("polished_diorite"))
        geometry.placeCuboid(editor,[7,1,1],[7,5,5],Block("polished_diorite"))
        geometry.placeCuboid(editor,[7,1,5],[11,5,5],Block("polished_diorite"))

        #柱
        geometry.placeCuboid(editor,[1,1,0],[1,6,0],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[7,1,0],[7,6,0],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[12,1,0],[12,6,0],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[1,1,7],[1,6,7],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[1,1,11],[1,6,11],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[4,1,11],[4,6,11],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[8,1,11],[8,6,11],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[12,1,11],[12,6,11],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[12,1,6],[12,6,6],Block("stripped_birch_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[7,1,5],[7,6,5],Block("stripped_birch_log",{"axis":"y"}))

        #ドア
        place_door(editor,[1,1,8],"east","left")
        place_door(editor,[1,1,9],"east","right")
        place_door(editor,[7,1,2],"east","left")
        place_door(editor,[7,1,3],"east","right")

        #床
        geometry.placeCuboid(editor,[1,0,1],[11,0,10],Block("birch_planks"))


        #窓
        geometry.placeCuboid(editor,[3,2,0],[5,3,0],Block("birch_fence"))
        geometry.placeCuboid(editor,[5,2,11],[7,3,11],Block("birch_fence"))
        geometry.placeCuboid(editor,[12,2,8],[12,3,9],Block("birch_fence"))

        #照明(外)
        outer_light(editor,[1,4,-1],"birch")
        outer_light(editor,[7,4,-1],"birch")
        outer_light(editor,[12,4,-1],"birch")
        outer_light(editor,[0,4,7],"birch")
        outer_light(editor,[4,4,12],"birch")
        outer_light(editor,[8,4,12],"birch")
        outer_light(editor,[13,4,6],"birch")
        outer_light(editor,[13,4,11],"birch")
        editor.placeBlock([7,7,5],Block("lantern"))

        #看板
        editor.placeBlock([0,3,10],Block("birch_wall_hanging_sign",{"facing":"north"}))
        
        #寝室
        color=random.choice(color_list)
        place_bed(editor,[9,1,2],"east",color)
        place_bed(editor,[9,1,3],"east",color)
        geometry.placeCuboid(editor,[9,1,1],[10,1,1],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
        geometry.placeCuboid(editor,[9,1,4],[10,1,4],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
        geometry.placeCuboid(editor,[11,1,1],[11,1,4],Block("stripped_birch_log",{"axis":"z"}))
        geometry.placeCuboid(editor,[11,2,2],[11,2,3],Block("bookshelf"))
        editor.placeBlock([11,2,1],Block("lantern"))
        on_table(editor,[11,2,4])
        inner_light(editor,[8,4,4],"birch")

        #ダイニング
        geometry.placeCuboid(editor,[11,1,9],[11,1,10],Block("birch_stairs",{"facing":"east"}))
        editor.placeBlock([11,1,8],Block("birch_wall_sign",{"facing":"north"}))
        geometry.placeCuboid(editor,[5,1,9],[5,1,10],Block("birch_stairs",{"facing":"west"}))
        editor.placeBlock([5,1,8],Block("birch_wall_sign",{"facing":"north"}))
        geometry.placeCuboid(editor,[9,1,9],[9,1,10],Block("bamboo_stairs",{"facing":"east","half":"top"}))
        geometry.placeCuboid(editor,[8,1,9],[8,1,10],Block("bamboo_slab",{"type":"top"}))       
        geometry.placeCuboid(editor,[7,1,9],[7,1,10],Block("bamboo_stairs",{"facing":"west","half":"top"}))
        on_table(editor,[7,2,10])
        editor.placeBlock([9,2,9],Block("lantern"))

        editor.placeBlock([4,5,6],Block("stripped_birch_log",{"axis":"y"}))
        editor.placeBlock([4,5,5],Block("spruce_trapdoor",{"facing":"north","half":"top","open":"true"}))
        editor.placeBlock([3,5,6],Block("spruce_trapdoor",{"facing":"west","half":"top","open":"true"}))
        editor.placeBlock([5,5,6],Block("spruce_trapdoor",{"facing":"east","half":"top","open":"true"}))
        editor.placeBlock([4,5,7],Block("spruce_trapdoor",{"facing":"south","half":"top","open":"true"}))
        editor.placeBlock([4,4,6],Block("lantern",{"hanging":"true"}))
        place_paint(editor,[2,3,4],base_coor,c_rota,"east","fern")

        #キッチン
        geometry.placeCuboid(editor,[2,1,2],[6,1,5],Block("lime_carpet"))
        outer_light(editor,[6,4,1],"birch")
        geometry.placeCuboid(editor,[2,4,1],[5,4,1],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([2,1,1],Block("crafting_table"))  
        editor.placeBlock([3,1,1],Block("furnace",{"facing":"south"}))  
        editor.placeBlock([4,1,1],Block("smoker",{"facing":"south"}))       
        editor.placeBlock([5,1,1],Block("water_cauldron",{"level":"3"}))
        editor.placeBlock([6,1,1],Block("chest",{"facing":"south"}))
        editor.placeBlock([2,5,1],Block("pumpkin"))  
        editor.placeBlock([3,5,1],Block("honeycomb_block"))  
        editor.placeBlock([4,5,1],Block("barrel",{"facing":"south"}))       
        editor.placeBlock([5,5,1],Block("birch_fence"))


        #棚
        geometry.placeCuboid(editor,[8,1,6],[10,1,6],Block("birch_stairs",{"facing":"north","half":"top"}))
        geometry.placeCuboid(editor,[7,1,6],[7,5,6],Block("spruce_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[11,1,6],[11,5,6],Block("spruce_trapdoor",{"facing":"east","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[8,3,6],[10,3,6],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[8,5,6],[10,5,6],Block("birch_slab",{"type":"bottom"}))
        editor.placeBlock([8,2,6],Block("lantern"))
        geometry.placeCuboid(editor,[9,2,6],[10,2,6],Block("barrel",{"facing":"south"}))
        geometry.placeCuboid(editor,[8,4,6],[9,4,6],Block("bookshelf"))
        editor.placeBlock([10,4,6],Block("large_amethyst_bud",{"facing":"up"}))

        #パンダ

        if(random.random()<0.7):
            summon_animal(editor,[4,2,4],base_coor,c_rota,"panda","panda")



def under_house_2(editor,coor,base_coor,b_rota,c_rota):

    with editor.pushTransform(Transform(coor,rotation=b_rota)):
        #外の装飾   
        geometry.placeCuboid(editor,[0,0,0],[0,0,12],Block("grass_block"))
        geometry.placeCuboid(editor,[0,0,6],[0,0,7],Block("gravel"))
        geometry.placeCuboid(editor,[0,1,0],[0,1,5],Block("bamboo_sapling"))
        geometry.placeCuboid(editor,[0,1,8],[0,1,12],Block("bamboo_sapling"))

        #壁
        geometry.placeCuboid(editor,[1,1,0],[1,1,12],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[12,1,0],[12,1,12],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[1,1,0],[12,1,0],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[1,1,12],[12,1,12],Block("waxed_copper_block"))

        geometry.placeCuboid(editor,[1,2,1],[1,4,11],Block("calcite"))
        geometry.placeCuboid(editor,[2,2,0],[11,4,0],Block("calcite"))
        geometry.placeCuboid(editor,[12,2,1],[12,4,11],Block("calcite"))
        geometry.placeCuboid(editor,[2,2,12],[11,4,12],Block("calcite"))
        geometry.placeCuboid(editor,[5,5,0],[8,5,0],Block("calcite"))
        geometry.placeCuboid(editor,[5,5,12],[8,5,12],Block("calcite"))

        #窓

        geometry.placeCuboid(editor,[1,2,2],[1,2,4],Block("bamboo_trapdoor",{"facing":"east","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[1,3,2],[1,3,4],Block("bamboo_trapdoor",{"facing":"east","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[1,2,9],[1,2,10],Block("bamboo_trapdoor",{"facing":"east","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[1,3,9],[1,3,10],Block("bamboo_trapdoor",{"facing":"east","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[3,2,12],[5,2,12],Block("bamboo_trapdoor",{"facing":"north","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[3,3,12],[5,3,12],Block("bamboo_trapdoor",{"facing":"north","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[8,2,12],[10,2,12],Block("bamboo_trapdoor",{"facing":"north","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[8,3,12],[10,3,12],Block("bamboo_trapdoor",{"facing":"north","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[3,2,0],[5,2,0],Block("bamboo_trapdoor",{"facing":"south","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[3,3,0],[5,3,0],Block("bamboo_trapdoor",{"facing":"south","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[8,2,0],[10,2,0],Block("bamboo_trapdoor",{"facing":"south","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[8,3,0],[10,3,0],Block("bamboo_trapdoor",{"facing":"south","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[12,2,2],[12,2,4],Block("bamboo_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[12,3,2],[12,3,4],Block("bamboo_trapdoor",{"facing":"west","half":"top","open":"true"}))
        geometry.placeCuboid(editor,[12,2,8],[12,2,10],Block("bamboo_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
        geometry.placeCuboid(editor,[12,3,8],[12,3,10],Block("bamboo_trapdoor",{"facing":"west","half":"top","open":"true"}))



        #柱
        geometry.placeCuboid(editor,[1,2,0],[1,4,0],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[12,2,0],[12,4,0],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[1,2,12],[1,4,12],Block("waxed_copper_block"))
        geometry.placeCuboid(editor,[12,2,12],[12,4,12],Block("waxed_copper_block"))



        #屋根
        roof_b="waxed_oxidized_cut_copper_slab"
        roof_an_b="waxed_weathered_cut_copper_slab"
        editor.placeBlock([0,6,-1],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([1,5,-1],Block(roof_b,{"type":"top"}))
        geometry.placeCuboid(editor,[2,5,-1],[11,5,-1],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([12,5,-1],Block(roof_b,{"type":"top"}))
        editor.placeBlock([13,6,-1],Block(roof_b,{"type":"bottom"}))

        editor.placeBlock([0,6,13],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([1,5,13],Block(roof_b,{"type":"top"}))
        geometry.placeCuboid(editor,[2,5,13],[11,5,13],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([12,5,13],Block(roof_b,{"type":"top"}))
        editor.placeBlock([13,6,13],Block(roof_b,{"type":"bottom"}))

        editor.placeBlock([0,5,12],Block(roof_b,{"type":"top"}))
        editor.placeBlock([13,5,12],Block(roof_b,{"type":"top"}))
        editor.placeBlock([0,5,0],Block(roof_b,{"type":"top"}))
        editor.placeBlock([13,5,0],Block(roof_b,{"type":"top"}))


        editor.placeBlock([1,5,0],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([1,5,12],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([12,5,0],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([12,5,12],Block(roof_b,{"type":"bottom"}))


        for z in range(11):
            if(z%2==0):
                editor.placeBlock([0,5,1+z],Block(roof_b,{"type":"bottom"}))
            else:
                editor.placeBlock([0,4,1+z],Block(roof_b,{"type":"top"}))

        for z in range(11):
            if(z%2==0):
                editor.placeBlock([13,5,1+z],Block(roof_b,{"type":"bottom"}))
            else:
                editor.placeBlock([13,4,1+z],Block(roof_b,{"type":"top"}))

        for z in range(13):
            if(z%2==1):
                geometry.placeCuboid(editor,[1,5,z],[2,5,z],Block(roof_an_b,{"type":"top"}))
            else:
                geometry.placeCuboid(editor,[1,5,z],[2,5,z],Block(roof_an_b,{"type":"bottom"}))
        
        for z in range(13):
            if(z%2==1):
                geometry.placeCuboid(editor,[11,5,0+z],[12,5,0+z],Block(roof_an_b,{"type":"top"}))
            else:
                geometry.placeCuboid(editor,[11,5,0+z],[12,5,0+z],Block(roof_an_b,{"type":"bottom"}))

        for z in range(13):
            if(z%2==1):
                geometry.placeCuboid(editor,[3,6,z],[4,6,z],Block(roof_b,{"type":"bottom"}))
            else:
                geometry.placeCuboid(editor,[3,5,z],[4,5,z],Block(roof_b,{"type":"top"}))

        for z in range(13):
            if(z%2==1):
                geometry.placeCuboid(editor,[9,6,z],[10,6,z],Block(roof_b,{"type":"bottom"}))
            else:
                geometry.placeCuboid(editor,[9,5,z],[10,5,z],Block(roof_b,{"type":"top"}))

        for z in range(13):
            if(z%2==1):
                editor.placeBlock([5,6,z],Block(roof_an_b,{"type":"top"}))
            else:
                editor.placeBlock([5,6,z],Block(roof_an_b,{"type":"bottom"}))

        for z in range(13):
            if(z%2==1):
                editor.placeBlock([8,6,z],Block(roof_an_b,{"type":"top"}))
            else:
                editor.placeBlock([8,6,z],Block(roof_an_b,{"type":"bottom"}))

        for z in range(13):
            if(z%2==1):
                geometry.placeCuboid(editor,[6,7,z],[7,7,z],Block(roof_b,{"type":"bottom"}))
            else:
                geometry.placeCuboid(editor,[6,6,z],[7,6,z],Block(roof_b,{"type":"top"}))

        editor.placeBlock([2,5,-1],Block("waxed_oxidized_cut_copper_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([2,5,13],Block("waxed_oxidized_cut_copper_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([11,5,-1],Block("waxed_oxidized_cut_copper_stairs",{"facing":"west","half":"top"}))
        editor.placeBlock([11,5,13],Block("waxed_oxidized_cut_copper_stairs",{"facing":"west","half":"top"}))

        geometry.placeCuboid(editor,[3,6,-1],[4,6,-1],Block(roof_b,{"type":"bottom"}))
        geometry.placeCuboid(editor,[3,6,13],[4,6,13],Block(roof_b,{"type":"bottom"}))
        geometry.placeCuboid(editor,[9,6,-1],[10,6,-1],Block(roof_b,{"type":"bottom"}))
        geometry.placeCuboid(editor,[9,6,13],[10,6,13],Block(roof_b,{"type":"bottom"}))
        editor.placeBlock([5,6,-1],Block(roof_b,{"type":"top"}))
        editor.placeBlock([8,6,-1],Block(roof_b,{"type":"top"}))
        editor.placeBlock([5,6,13],Block(roof_b,{"type":"top"}))
        editor.placeBlock([8,6,13],Block(roof_b,{"type":"top"}))
        geometry.placeCuboid(editor,[6,7,-1],[7,7,-1],Block(roof_b,{"type":"bottom"}))
        geometry.placeCuboid(editor,[6,7,13],[7,7,13],Block(roof_b,{"type":"bottom"}))
        geometry.placeCuboid(editor,[6,6,0],[7,6,0],Block("waxed_oxidized_cut_copper"))
        geometry.placeCuboid(editor,[6,6,12],[7,6,12],Block("waxed_oxidized_cut_copper"))


        #床
        geometry.placeCuboid(editor,[1,0,0],[12,0,12],Block("bamboo_planks"))

        #ドア
        place_door(editor,[1,1,6],"east","left","bamboo")
        place_door(editor,[1,1,7],"east","right","bamboo")

        #外照明
        editor.placeBlock([0,5,-1],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([0,5,13],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([13,5,-1],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([13,5,13],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([0,5,6],Block("lantern"))
        editor.placeBlock([13,5,6],Block("lantern"))
        editor.placeBlock([3,6,2],Block("lantern"))
        editor.placeBlock([10,6,2],Block("lantern"))
        editor.placeBlock([3,6,10],Block("lantern"))
        editor.placeBlock([10,6,10],Block("lantern"))
        editor.placeBlock([6,7,6],Block("lantern"))
        editor.placeBlock([7,6,-1],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([7,6,13],Block("lantern",{"hanging":"true"}))


        #ベッド(蚊帳)
        geometry.placeCuboid(editor,[8,1,8],[11,1,11],Block("bamboo_slab",{"type":"bottom"}))
        geometry.placeCuboid(editor,[8,4,8],[11,4,11],Block("bamboo_slab",{"type":"top"}))
        editor.placeBlock([8,1,8],Block("bamboo_mosaic"))
        geometry.placeCuboid(editor,[8,2,8],[8,3,8],Block("bamboo_fence"))
        editor.placeBlock([8,4,8],Block("bamboo_slab"))
        editor.placeBlock([11,1,8],Block("bamboo_mosaic"))       
        geometry.placeCuboid(editor,[11,2,8],[11,3,8],Block("bamboo_fence"))
        editor.placeBlock([11,4,8],Block("bamboo_slab"))    
        editor.placeBlock([8,1,11],Block("bamboo_mosaic"))
        geometry.placeCuboid(editor,[8,2,11],[8,3,11],Block("bamboo_fence"))
        editor.placeBlock([8,4,11],Block("bamboo_slab"))  
        editor.placeBlock([11,1,11],Block("bamboo_mosaic"))
        geometry.placeCuboid(editor,[11,2,11],[11,3,11],Block("bamboo_fence"))
        editor.placeBlock([11,4,11],Block("bamboo_slab"))  
        place_bed(editor,[9,1,9],"east")
        place_bed(editor,[9,1,10],"east")
        geometry.placeCuboid(editor,[7,4,8],[7,4,11],Block("white_wall_banner",{"facing":"west"}))    
        geometry.placeCuboid(editor,[8,4,7],[11,4,7],Block("white_wall_banner",{"facing":"north"}))    
        editor.placeBlock([7,1,8],Block("jungle_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([7,1,11],Block("jungle_trapdoor",{"facing":"west","open":"true"}))
        editor.placeBlock([8,1,7],Block("jungle_trapdoor",{"facing":"north","open":"true"}))
        editor.placeBlock([11,1,7],Block("jungle_trapdoor",{"facing":"north","open":"true"}))

        #机
        geometry.placeCuboid(editor,[11,1,2],[11,1,4],Block("bamboo_mosaic_stairs",{"facing":"east"}))
        editor.placeBlock([11,1,1],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
        editor.placeBlock([11,1,5],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
        geometry.placeCuboid(editor,[8,1,2],[8,1,4],Block("bamboo_mosaic_stairs",{"facing":"west"}))
        editor.placeBlock([8,1,1],Block("bamboo_trapdoor",{"facing":"north","open":"true"}))
        editor.placeBlock([8,1,5],Block("bamboo_trapdoor",{"facing":"south","open":"true"}))
        geometry.placeCuboid(editor,[9,1,2],[10,1,4],Block("bamboo_fence"))
        geometry.placeCuboid(editor,[9,2,2],[10,2,4],Block("bamboo_pressure_plate"))

        geometry.placeCuboid(editor,[6,1,4],[6,4,4],Block("spruce_trapdoor",{"facing":"south","open":"true"}))
        geometry.placeCuboid(editor,[6,3,1],[6,3,3],Block("spruce_trapdoor",{"facing":"west","half":"top"}))
        geometry.placeCuboid(editor,[6,5,1],[6,5,3],Block("spruce_trapdoor",{"facing":"west","half":"bottom"}))
        geometry.placeCuboid(editor,[6,1,1],[6,2,3],Block("barrel",{"facing":"west"}))
        geometry.placeCuboid(editor,[6,4,1],[6,4,2],Block("bookshelf"))
        editor.placeBlock([6,4,3],Block("lantern"))
        place_paint(editor,[7,2,2],base_coor,c_rota,"east","pond")

        #植物机
        geometry.placeCuboid(editor,[2,1,10],[2,1,11],Block("polished_andesite_stairs",{"facing":"west","half":"top"}))
        geometry.placeCuboid(editor,[3,1,10],[4,1,11],Block("polished_andesite_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[5,1,10],[5,1,11],Block("polished_andesite_stairs",{"facing":"east","half":"top"}))
        editor.placeBlock([2,2,11],Block("lantern"))
        place_pot(editor,[3,2,10],"red_tulip")
        place_pot(editor,[4,2,10],"cornflower")
        place_pot(editor,[5,2,10],"lily_of_the_valley")
        place_pot(editor,[3,2,11],"torchflower")
        place_pot(editor,[4,2,11],"bamboo")
        place_pot(editor,[5,2,11],"oxeye_daisy")


        #照明
        inner_light(editor,[11,2,6],"bamboo")
        inner_light(editor,[6,2,11],"bamboo")
        editor.placeBlock([2,4,2],Block("lantern",{"hanging":"true"}))

        if(random.random()<0.7):
            summon_animal(editor,[4,2,4],base_coor,c_rota,"panda","panda")




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
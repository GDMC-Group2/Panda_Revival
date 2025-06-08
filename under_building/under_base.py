#建築物:ベース
#憩いの場,兼輸送場所になる

#設置位置:1,2,3層
#大きさ2*1(29*10*13)

from gdpc import Editor, Block, geometry, Transform
import time
from under_build import under_build_base, place_frame



# editor=Editor()



def under_basement(editor,coor,base_coor,build_rotation,rotation,size):
    #layer:何層目のベースか
    with editor.pushTransform(Transform(coor,rotation=build_rotation)):
        under_build_base(editor,coor,rotation,size,Block("birch_planks"))
        #階段(1-2階層)

        stairs(editor,[23,0,6],20)
        geometry.placeCuboid(editor,[23,6,2],[23,7,2],Block("air"))
        geometry.placeCuboid(editor,[23,6,10],[23,7,10],Block("air"))

        #2階
        editor.placeBlock([0,1,10],Block("birch_stairs",{"facing":"south"}))
        editor.placeBlock([1,1,10],Block("birch_stairs",{"facing":"south"}))
        geometry.placeCuboid(editor,[0,2,11],[1,2,12],Block("birch_slab",{"type":"bottom"}))
        geometry.placeCuboid(editor,[2,2,11],[2,2,12],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[3,3,11],[3,3,12],Block("birch_stairs",{"facing":"east"}))
        geometry.placeCuboid(editor,[4,4,11],[4,4,12],Block("birch_stairs",{"facing":"east"}))
        geometry.placeCuboid(editor,[5,5,11],[5,5,12],Block("birch_stairs",{"facing":"east"}))
        geometry.placeCuboid(editor,[6,5,4],[9,5,12],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[0,5,0],[9,5,3],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[10,5,10],[20,5,12],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[21,5,0],[28,5,12],Block("birch_slab",{"type":"top"}))
        geometry.placeCuboid(editor,[2,1,10],[2,3,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[3,3,10],[3,4,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[4,4,10],[4,5,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[5,5,10],[5,6,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[0,6,3],[6,6,3],Block("birch_fence"))
        geometry.placeCuboid(editor,[6,6,4],[6,6,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[9,6,0],[9,6,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[10,6,10],[20,6,10],Block("birch_fence"))
        geometry.placeCuboid(editor,[21,6,0],[21,6,10],Block("birch_fence"))

        #2階装飾
        aquarium(editor)

        #階段部分追記
        editor.placeBlock([23,5,2],Block("birch_planks"))
        editor.placeBlock([23,5,10],Block("birch_planks"))
        geometry.placeCuboid(editor,[24,1,2],[28,1,2],Block("birch_fence"))
        geometry.placeCuboid(editor,[24,1,10],[28,1,10],Block("birch_fence"))


        #時計
        editor.placeBlock([14,1,12],Block("dark_oak_slab",{"type":"bottom"}))
        editor.placeBlock([13,1,12],Block("spruce_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
        editor.placeBlock([13,2,12],Block("spruce_trapdoor",{"facing":"west","half":"bottom","open":"true"}))
        editor.placeBlock([15,1,12],Block("spruce_trapdoor",{"facing":"east","half":"bottom","open":"true"}))
        editor.placeBlock([15,2,12],Block("spruce_trapdoor",{"facing":"east","half":"bottom","open":"true"}))
        editor.placeBlock([14,2,12],Block("bell",{"attachment":"ceiling","facing":"south"}))
        editor.placeBlock([14,3,12],Block("dark_oak_planks"))
        place_frame(editor,[14,3,11],base_coor,rotation,"north","clock")

        #机
        geometry.placeCuboid(editor,[11,1,5],[11,1,7],Block("bamboo_stairs",{"facing":"west"}))
        geometry.placeCuboid(editor,[13,1,3],[15,1,3],Block("bamboo_stairs",{"facing":"north"}))
        geometry.placeCuboid(editor,[17,1,5],[17,1,7],Block("bamboo_stairs",{"facing":"east"}))
        geometry.placeCuboid(editor,[13,1,9],[15,1,9],Block("bamboo_stairs",{"facing":"south"}))
        geometry.placeCuboid(editor,[12,0,4],[16,0,8],Block("bamboo_mosaic"))
        geometry.placeCuboid(editor,[13,1,5],[15,1,7],Block("birch_slab",{"type":"top"}))
        #収納
        editor.placeBlock([0,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([1,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([0,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([1,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([0,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([1,3,0],Block("chest",{"facing":"south","type":"left"}))

        editor.placeBlock([2,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([3,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([2,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([3,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([2,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([3,3,0],Block("chest",{"facing":"south","type":"left"}))

        editor.placeBlock([9,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([10,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([9,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([10,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([9,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([10,3,0],Block("chest",{"facing":"south","type":"left"}))

        editor.placeBlock([11,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([12,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([11,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([12,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([11,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([12,3,0],Block("chest",{"facing":"south","type":"left"}))

        editor.placeBlock([16,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([17,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([16,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([17,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([16,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([17,3,0],Block("chest",{"facing":"south","type":"left"}))

        editor.placeBlock([18,1,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([19,1,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([18,2,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([19,2,0],Block("chest",{"facing":"south","type":"left"}))
        editor.placeBlock([18,3,0],Block("chest",{"facing":"south","type":"right"}))
        editor.placeBlock([19,3,0],Block("chest",{"facing":"south","type":"left"}))

        geometry.placeCuboid(editor,[13,1,0],[15,3,0],Block("barrel",{"facing":"south"}))
        geometry.placeCuboid(editor,[0,6,0],[7,8,0],Block("barrel",{"facing":"south"}))

        geometry.placeCuboid(editor,[17,1,12],[19,2,12],Block("furnace",{"facing":"north"}))


        #柱
        geometry.placeCuboid(editor,[-1,1,2],[-1,10,2],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[-1,1,10],[-1,10,10],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[29,1,2],[29,10,2],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[29,1,10],[29,10,10],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[3,1,-1],[3,10,-1],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[3,1,13],[3,10,13],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[9,1,-1],[9,10,-1],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[9,1,13],[9,10,13],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[14,1,-1],[14,10,-1],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[14,1,13],[14,10,13],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[19,1,-1],[19,10,-1],Block("spruce_log",{"axis":"y"}))
        geometry.placeCuboid(editor,[19,1,13],[19,10,13],Block("spruce_log",{"axis":"y"}))

        geometry.placeCuboid(editor,[3,9,0],[3,9,12],Block("spruce_log",{"axis":"z"}))
        geometry.placeCuboid(editor,[14,9,0],[14,9,12],Block("spruce_log",{"axis":"z"}))
        geometry.placeCuboid(editor,[4,9,6],[13,9,6],Block("spruce_log",{"axis":"x"}))

        geometry.placeCuboid(editor,[-1,6,0],[-1,6,12],Block("spruce_log",{"axis":"z"}))
        geometry.placeCuboid(editor,[29,6,0],[29,6,12],Block("spruce_log",{"axis":"z"}))
        geometry.placeCuboid(editor,[0,6,-1],[28,6,-1],Block("spruce_log",{"axis":"x"}))
        geometry.placeCuboid(editor,[0,6,13],[28,6,13],Block("spruce_log",{"axis":"x"}))
        #照明
        #
        editor.placeBlock([2,4,10],Block("lantern"))
        editor.placeBlock([0,7,3],Block("lantern"))
        editor.placeBlock([6,7,3],Block("lantern"))
        editor.placeBlock([6,7,10],Block("lantern"))
        editor.placeBlock([9,7,0],Block("lantern"))
        editor.placeBlock([9,7,10],Block("lantern"))
        editor.placeBlock([14,7,10],Block("lantern"))
        editor.placeBlock([21,7,10],Block("lantern"))
        editor.placeBlock([21,7,5],Block("lantern"))
        editor.placeBlock([21,7,0],Block("lantern"))
        editor.placeBlock([28,6,0],Block("lantern"))
        editor.placeBlock([28,6,12],Block("lantern"))
        editor.placeBlock([3,10,6],Block("lantern"))
        editor.placeBlock([14,10,6],Block("lantern"))    


        editor.placeBlock([3,8,6],Block("grindstone",{"face":"ceiling","facing":"east"}))
        editor.placeBlock([3,7,6],Block("chain",{"axis":"y"}))
        editor.placeBlock([3,6,6],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([14,8,6],Block("grindstone",{"face":"ceiling","facing":"east"}))
        editor.placeBlock([14,7,6],Block("chain",{"axis":"y"}))
        editor.placeBlock([14,6,6],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([0,5,0],Block("birch_slab",{"type":"double"}))
        editor.placeBlock([0,4,0],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([6,5,3],Block("birch_slab",{"type":"double"}))
        editor.placeBlock([6,4,3],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([7,5,6],Block("birch_slab",{"type":"double"}))
        editor.placeBlock([7,4,6],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([21,5,0],Block("birch_slab",{"type":"double"}))
        editor.placeBlock([21,4,0],Block("lantern",{"hanging":"true"}))
        editor.placeBlock([21,5,0],Block("birch_slab",{"type":"double"}))
        editor.placeBlock([21,4,0],Block("lantern",{"hanging":"true"}))

        editor.placeBlock([11,3,12],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([11,4,12],Block("lantern"))
        editor.placeBlock([11,8,12],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([11,9,12],Block("lantern"))
        editor.placeBlock([17,8,12],Block("birch_slab",{"type":"top"}))
        editor.placeBlock([17,9,12],Block("lantern"))

        editor.placeBlock([11,1,3],Block("cobblestone_wall"))
        editor.placeBlock([11,2,3],Block("lantern"))
        editor.placeBlock([11,1,9],Block("cobblestone_wall"))
        editor.placeBlock([11,2,9],Block("lantern"))
        editor.placeBlock([17,1,3],Block("cobblestone_wall"))
        editor.placeBlock([17,2,3],Block("lantern"))
        editor.placeBlock([17,1,9],Block("cobblestone_wall"))
        editor.placeBlock([17,2,9],Block("lantern"))


        #出入口の確保
        geometry.placeCuboid(editor,[-1,1,3],[-1,5,9],Block("air"))
        geometry.placeCuboid(editor,[-1,1,3],[0,1,3],Block("rail",{"shape":"east_west"}))
        geometry.placeCuboid(editor,[1,1,3],[2,1,3],Block("powered_rail",{"shape":"east_west"}))
        editor.placeBlock([3,1,3],Block("birch_planks"))
        editor.placeBlock([3,2,3],Block("birch_button",{"face":"floor","facing":"west"}))







def aquarium(editor):
    block_list=[Block("seagrass"),Block("brain_coral_fan",{"waterlogged":"true"}),Block("water")]
    geometry.placeCuboid(editor,[25,6,2],[28,6,10],Block("sand"))
    geometry.placeCuboid(editor,[24,6,1],[28,10,1],Block("glass"))
    geometry.placeCuboid(editor,[24,6,11],[28,10,11],Block("glass"))
    geometry.placeCuboid(editor,[24,6,2],[24,10,10],Block("glass"))
    geometry.placeCuboid(editor,[25,7,2],[28,10,10],Block("water"))
    geometry.placeCuboid(editor,[25,7,2],[28,7,10],block_list)
    editor.placeBlock([26,7,4],Block("cobblestone_wall"))
    editor.placeBlock([26,8,4],Block("lantern"))
    editor.placeBlock([26,7,8],Block("cobblestone_wall"))
    editor.placeBlock([26,8,8],Block("lantern"))




def stairs(editor,coor,lenght):
    for i in range(lenght):
        geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]-3],[coor[0]+i,coor[1]-i,coor[2]+3],Block("cobblestone_stairs",{"facing":"west"}))
        geometry.placeCuboid(editor,[coor[0]+i+1,coor[1]-i,coor[2]-3],[coor[0]+i+6,coor[1]-i,coor[2]+3],Block("air"))
        geometry.placeCuboid(editor,[coor[0]+i+7,coor[1]-i,coor[2]-3],[coor[0]+i+7,coor[1]-i,coor[2]+3],Block("stone"))
        if (i != 0):
            geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]-4],[coor[0]+i+6,coor[1]-i,coor[2]-4],Block("stone"))
            geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]+4],[coor[0]+i+6,coor[1]-i,coor[2]+4],Block("stone"))
        if(i%4 == 0):
            if(i==4):
                geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]-4],[coor[0]+i,coor[1]-i+3,coor[2]-4],Block("spruce_log",{"axis":"y"}))
                geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]+4],[coor[0]+i,coor[1]-i+3,coor[2]+4],Block("spruce_log",{"axis":"y"}))
            else:
                geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]-4],[coor[0]+i,coor[1]-i+7,coor[2]-4],Block("spruce_log",{"axis":"y"}))
                geometry.placeCuboid(editor,[coor[0]+i,coor[1]-i,coor[2]+4],[coor[0]+i,coor[1]-i+7,coor[2]+4],Block("spruce_log",{"axis":"y"}))
            editor.placeBlock([coor[0]+i,coor[1]-i+3,coor[2]-3],Block("wall_torch",{"facing":"south"}))    
            editor.placeBlock([coor[0]+i,coor[1]-i+3,coor[2]+3],Block("wall_torch",{"facing":"north"}))    

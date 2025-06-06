from gdpc import Editor, Block, geometry, Transform
import time
from under_build import under_build_base


#under_farm_big
#設置位置:1層(生産層)
#大きさ2*2(29*6*29)
#農作物:小麦,キノコ,ジャガイモ
#竹は別の場所に作る
editor=Editor()

coor=[100,-61,100]
rotation=0
size=[29,6,29]
def under_farm_big(editor,coor,rotation,size):
    transform=Transform(translation=coor, rotation=rotation)
    editor.transform.push(transform)
    under_build_base(editor,coor,rotation,size)
    geometry.placeCuboid(editor,[1,0,1],[21,0,21],Block("polished_granite"))

    field_coor=[2,0,2]
    crop="wheat"
    make_field(editor,field_coor,crop)
    
    field_coor=[2,0,12]
    crop="carrots"
    make_field(editor,field_coor,crop)

    field_coor=[12,0,2]
    crop="wheat"
    make_field(editor,field_coor,crop)

    field_coor=[12,0,12]
    crop="potatoes"
    make_field(editor,field_coor,crop)

    geometry.placeCuboid(editor,[0,0,22],[28,0,28],Block("dirt"))

    mushroom_coor=[3,0,25]
    place_mushroom(editor,mushroom_coor,"red")

    mushroom_coor=[9,0,25]
    place_mushroom(editor,mushroom_coor,"brown")

    mushroom_coor=[19,0,25]
    place_mushroom(editor,mushroom_coor,"brown")

    mushroom_coor=[25,0,25]
    place_mushroom(editor,mushroom_coor,"red")

    #スイカ,かぼちゃ畑
    geometry.placeCuboid(editor,[22,0,16],[28,0,20],Block("polished_granite"))
    geometry.placeCuboid(editor,[22,0,17],[28,0,19],Block("farmland",{"moisture":"7"}))
    geometry.placeCuboid(editor,[22,0,18],[28,0,18],Block("water"))
    editor.placeBlock([21,1,17],Block("torch"))
    editor.placeBlock([21,1,19],Block("torch"))
    geometry.placeCuboid(editor,[22,1,17],[28,1,17],Block("pumpkin_stem",{"age":"7"}))
    geometry.placeCuboid(editor,[22,1,19],[28,1,19],Block("melon_stem",{"age":"7"}))
    

    #水場
    geometry.placeCuboid(editor,[26,-1,0],[28,-1,4],Block("stone"))
    geometry.placeCuboid(editor,[26,0,0],[28,0,4],Block("water"))

    #収納
    editor.placeBlock([28,1,6],Block("crafting_table"))
    editor.placeBlock([28,1,7],Block("chest",{"facing":"west","type":"right"}))
    editor.placeBlock([28,1,8],Block("chest",{"facing":"west","type":"left"}))
    editor.placeBlock([28,2,7],Block("chest",{"facing":"west","type":"right"}))
    editor.placeBlock([28,2,8],Block("chest",{"facing":"west","type":"left"}))
    geometry.placeCuboid(editor,[28,1,9],[28,3,11],Block("barrel",{"facing":"west"}))

    #光源
    editor.placeBlock([0,1,28],Block("torch"))
    editor.placeBlock([6,1,28],Block("torch"))
    editor.placeBlock([22,1,28],Block("torch"))
    editor.placeBlock([28,1,28],Block("torch"))
    editor.placeBlock([14,1,28],Block("torch"))
    editor.placeBlock([28,3,2],Block("wall_torch",{"facing":"west"}))
    editor.placeBlock([28,3,12],Block("wall_torch",{"facing":"west"}))
    editor.placeBlock([28,3,18],Block("wall_torch",{"facing":"west"}))
    editor.placeBlock([3,6,25],Block("lantern",{"hanging":"true"}))
    editor.placeBlock([9,6,25],Block("lantern",{"hanging":"true"}))
    editor.placeBlock([19,6,25],Block("lantern",{"hanging":"true"}))
    editor.placeBlock([25,6,25],Block("lantern",{"hanging":"true"}))


    editor.flushBuffer()


def make_field(editor,coor,crop):
    #用途:9*9の畑を作る
    #coor:畑のx,zが最小の点
    #crop:作物:ちゃんと名前をいれる事,
    with editor.pushTransform():
        editor.transform @= Transform((coor[0],coor[1],coor[2]))
        Block_crop_list=[]
        for i in range(8):
            num=f"{i}"
            Block_crop=Block(crop,{"age":num})
            Block_crop_list.append(Block_crop)
        #松明の設置
        editor.placeBlock([4,1,-1],Block("torch"))
        editor.placeBlock([4,1,9],Block("torch"))
        editor.placeBlock([-1,1,4],Block("torch"))
        editor.placeBlock([9,1,4],Block("torch"))

        editor.placeBlock([-1,1,-1],Block("torch"))
        editor.placeBlock([9,1,-1],Block("torch"))
        editor.placeBlock([-1,1,9],Block("torch"))
        editor.placeBlock([9,1,9],Block("torch"))

        #畑の設置
        geometry.placeCuboid(editor,[0,0,0],[8,0,8],Block("farmland",{"moisture":"7"}))
        geometry.placeCuboid(editor,[0,1,0],[8,1,8],Block_crop_list)
        editor.placeBlock([4,-1,4],Block("stone"))
        editor.placeBlock([4,0,4],Block("water"))
        editor.placeBlock([4,1,4],Block("stone"))
        editor.placeBlock([4,2,4],Block("torch"))


def place_mushroom(editor,coor,mushroom_type):
    #内容:巨大キノコを設置する
    with editor.pushTransform():
        editor.transform @= Transform((coor[0],coor[1],coor[2]))
        if(mushroom_type=="red"):
            mushroom_block=Block("red_mushroom_block")
            geometry.placeCuboid(editor,[0,1,0],[0,4,0],Block("mushroom_stem"))

            geometry.placeCuboid(editor,[-2,3,-1],[-2,4,1],mushroom_block)
            geometry.placeCuboid(editor,[2,3,-1],[2,4,1],mushroom_block)
            geometry.placeCuboid(editor,[-1,3,-2],[1,4,-2],mushroom_block)
            geometry.placeCuboid(editor,[-1,3,2],[1,4,2],mushroom_block)
            geometry.placeCuboid(editor,[-1,5,-1],[1,5,1],mushroom_block)

        elif(mushroom_type=="brown"):
            mushroom_block=Block("brown_mushroom_block")
            geometry.placeCuboid(editor,[0,1,0],[0,4,0],Block("mushroom_stem"))
            editor.placeBlock([-2,4,0],mushroom_block)
            editor.placeBlock([-1,4,-1],mushroom_block)
            editor.placeBlock([-1,4,1],mushroom_block)
            editor.placeBlock([0,4,-2],mushroom_block)
            editor.placeBlock([0,4,2],mushroom_block)
            editor.placeBlock([1,4,-1],mushroom_block)
            editor.placeBlock([1,4,1],mushroom_block)
            editor.placeBlock([2,4,0],mushroom_block)

            editor.placeBlock([0,5,0],mushroom_block)
            editor.placeBlock([-1,5,0],mushroom_block)
            editor.placeBlock([1,5,0],mushroom_block)
            editor.placeBlock([0,5,-1],mushroom_block)
        editor.placeBlock([0,5,1],mushroom_block)       

under_farm_big(editor,coor,rotation,size)


from gdpc import Editor, Block, geometry, Transform
import time
import random
from under_building.under_build import under_build_base,summon_animal


#under_farm_big
#設置位置:1層(生産層)
#size:3*1(45*9*13)

def under_plantation(editor,coor,base_coor,build_rotation,rotation,size=[45,9,13]):
    with editor.pushTransform(Transform(coor,rotation=build_rotation)):
        under_build_base(editor,coor,rotation,size)
        for i in range(7):
            for j in range(2):
                editor.placeBlock([4+i*6,0,3+j*6],Block("dirt"))
                place_tree(editor,[4+i*6,1,3+j*6])
                editor.placeBlock([4+i*6,9,3+j*6],Block("chain",{"axis":"y"}))
                editor.placeBlock([4+i*6,8,3+j*6],Block("lantern",{"hanging":"true"}))
        for i in range(8):
            for j in range(3):
                editor.placeBlock([1+i*6,1,0+j*6],Block("torch"))

        editor.placeBlock([0,1,0],Block("chest",{"facing":"east","type":"left"}))
        editor.placeBlock([0,1,1],Block("chest",{"facing":"east","type":"right"}))
        editor.placeBlock([0,2,0],Block("chest",{"facing":"east","type":"left"}))
        editor.placeBlock([0,2,1],Block("chest",{"facing":"east","type":"right"}))
        geometry.placeCuboid(editor,[0,1,2],[0,2,3],Block("barrel",{"facing":"east"}))
        for i in range(3):
            summon_animal(editor,[21,1,6],base_coor,rotation,"panda","panda")


def place_tree(editor,coor,log_type = "birch"):
    log= log_type+"_log"
    leaves= Block(log_type+"_leaves",{"persistent":"false"})
    sapling=Block(log_type+"_sapling")
    if (random.random()<0.8):
        geometry.placeCuboid(editor,[coor[0]-2,coor[1]+2,coor[2]-2],[coor[0]+2,coor[1]+3,coor[2]+2],leaves)
        editor.placeBlock([coor[0]-1,coor[1]+4,coor[2]],leaves)
        editor.placeBlock([coor[0]-1,coor[1]+5,coor[2]],leaves)
        editor.placeBlock([coor[0],coor[1]+4,coor[2]-1],leaves)
        editor.placeBlock([coor[0],coor[1]+5,coor[2]-1],leaves)
        editor.placeBlock([coor[0],coor[1]+4,coor[2]+1],leaves)
        editor.placeBlock([coor[0],coor[1]+5,coor[2]+1],leaves)
        editor.placeBlock([coor[0]+1,coor[1]+4,coor[2]],leaves)
        editor.placeBlock([coor[0]+1,coor[1]+5,coor[2]],leaves)
        editor.placeBlock([coor[0],coor[1]+5,coor[2]],leaves)
        for i in range(5):
            editor.placeBlock([coor[0],coor[1]+i,coor[2]],Block(log,{"axis":"y"}))
    else:
        editor.placeBlock([coor[0],coor[1],coor[2]],sapling)



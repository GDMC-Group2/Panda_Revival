from gdpc import Editor, Block, geometry, Transform
import time
from under_build import under_build_base
import random



def place_frame(editor,coor,base_coor,rotation,direction,item):
    #用途:フレームの設置
    #direction:向き(NASWで入力)
    #rotation:設置系の向き

    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"
    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"): #右向き
            place_dire=3 
        elif(direction=="west"): #後ろ向き
            place_dire=4 
        elif(direction=="north"): #左向き
            place_dire=2 
        elif(direction=="east"): #正面
            place_dire=5 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):#右向き
            place_dire=4 
        elif(direction=="west"):#後ろ向き
            place_dire=2 
        elif(direction=="north"):#左向き
            place_dire=5 
        elif(direction=="east"):#正面
            place_dire=3 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):
            place_dire=2 
        elif(direction=="west"):
            place_dire=5 
        elif(direction=="north"):
            place_dire=3 
        elif(direction=="east"):
            place_dire=4 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=5
        elif(direction=="west"):
            place_dire=3
        elif(direction=="north"):
            place_dire=4
        elif(direction=="east"):
            place_dire=2
    if item:
        NBT=f"{{Facing:{place_dire},Item:{{id:{item}}}}}"
    else:
        NBT=f"{{Facing:{place_dire}}}"

    editor.runCommand(f"summon item_frame {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")



def place_stand(editor,coor,base_coor,rotation,direction,boots="",leggings="",chestplate="",helmet=""):
    #用途:アーマースタンドの設置
    #east:x=+X z=+Z dire=0 #"east"
    #south:x=+Z z=-X dire=3  #"south"
    #west:x=-X z=-Z dire=2 #"west"
    #north:x=-Z z=+X dire=1 #"north"

    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"): #右向き
            place_dire=0 
        elif(direction=="west"): #後ろ向き
            place_dire=90  
        elif(direction=="north"): #左向き
            place_dire=180 
        elif(direction=="east"): #正面
            place_dire=-90 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):
            place_dire=90 
        elif(direction=="west"):
            place_dire=180 
        elif(direction=="north"):
            place_dire=-90 
        elif(direction=="east"):
            place_dire=0 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):#右向き
            place_dire=180 
        elif(direction=="west"):#後ろ向き
            place_dire=-90 
        elif(direction=="north"):#左向き
            place_dire=0 
        elif(direction=="east"):#正面
            place_dire=90 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=-90 #west
        elif(direction=="west"):
            place_dire=0 #north
        elif(direction=="north"):
            place_dire=90 #east
        elif(direction=="east"):
            place_dire=180 #south

    if boots:
        boots=f"id:\"{boots}\",Count:1b"
    if leggings:
        leggings=f"id:\"{leggings}\",Count:1b"
    if chestplate:
        chestplate=f"id:\"{chestplate}\",Count:1b"
    if helmet:
        helmet=f"id:\"{helmet}\",Count:1b"
    NBT=f"{{Rotation:[{place_dire}f,0f],ArmorItems:[{{{boots}}},{{{leggings}}},{{{chestplate}}},{{{helmet}}}]}}"
    #print(NBT)
    editor.runCommand(f"summon armor_stand {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {NBT}")





def place_bed(editor,coor,facing,color="red"):
    #用途:ベッドの設置
    #coorは足側を入力する
    #facing=ベット自体の向き

    bed_color=color+"_bed"
    x=0
    z=0
    if(facing=="south"): #右向き
        z=1
    elif(facing=="west"): #後ろ向き
        x=-1
    elif(facing=="north"): #左向き
        z=-1
    elif(facing=="east"): #正面
        x=1
    editor.placeBlock(coor,Block(bed_color,{"facing":facing,"part":"foot"}))
    editor.placeBlock([coor[0]+x,coor[1],coor[2]+z],Block(bed_color,{"facing":facing,"part":"head"}))






# editor=Editor()


# coor=[4,1,0]
# place_bed(editor,coor,facing)


def place_paint(editor,coor,base_coor,rotation,direction,name):
    place_dire=0
    if(rotation==0): #east
        x=coor[0]
        y=coor[1]
        z=coor[2]
        if(direction=="south"):
            place_dire=0 
        elif(direction=="west"):
            place_dire=1 
        elif(direction=="north"):
            place_dire=2 
        elif(direction=="east"):
            place_dire=3 
    elif(rotation==1):#"north"
        x=-coor[2]
        y=coor[1]
        z=coor[0]
        if(direction=="south"):
            place_dire=1 
        elif(direction=="west"):
            place_dire=2 
        elif(direction=="north"):
            place_dire=3 
        elif(direction=="east"):
            place_dire=0 
    elif(rotation==2):#"west"
        x=-coor[0]
        y=coor[1]
        z=-coor[2]
        if(direction=="south"):
            place_dire=2 
        elif(direction=="west"):
            place_dire=3 
        elif(direction=="north"):
            place_dire=0 
        elif(direction=="east"):
            place_dire=1 
    elif(rotation==3):#"south"
        x=coor[2]
        y=coor[1]
        z=-coor[0]
        if(direction=="south"):
            place_dire=3
        elif(direction=="west"):
            place_dire=0
        elif(direction=="north"):
            place_dire=1
        elif(direction=="east"):
            place_dire=2

    editor.runCommand(f"summon painting {base_coor[0]+x} {base_coor[1]+y} {base_coor[2]+z} {{facing:{place_dire},variant:{name}}}")

# editor=Editor()

# base_coor=[70,-61,250]
# rotation=3
# facing="west"
# transform=Transform(translation=base_coor, rotation=rotation)
# editor.transform.push(transform)
# geometry.placeCuboid(editor,[3,1,-1],[3,4,1],Block("polished_diorite"))
# place_paint(editor,[2,3,0],[70,-61,250],rotation,facing,"fern")
#パンダ柄のはた
# minecraft:white_wall_banner[facing=west]{patterns:[{color:"black",pattern:"minecraft:flower"},
# {color:"white",pattern:"minecraft:half_horizontal_bottom"},
# {color:"black",pattern:"minecraft:triangles_top"},
# {color:"white",pattern:"minecraft:stripe_center"},
# {color:"black",pattern:"minecraft:creeper"},
# {color:"white",pattern:"minecraft:stripe_bottom"}]}
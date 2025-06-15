from copy import deepcopy
from gdpc import Editor, Block, WorldSlice,Box,geometry
from glm import  ivec3
from time import *


def FindRiver(heightmap, env):
    print("Finding rivers")
    tempHM = deepcopy(heightmap)
    RiverMap = [[0 for k in range(len(heightmap[0]))] for j in range(len(heightmap))]
    for x in range(len(tempHM)):
        for y in range(len(tempHM[0])):
            if tempHM[x][y] != 999 and env[x][y] == 0:
                area = []
                area.append([x,y])
                stonks = []
                stonks.append([x,y])
                length = len(stonks)
                tempHM[x][y] = 999
                while length >= 1:
                    x = stonks[0][0]
                    y = stonks[0][1]
                    stonks.pop(0)
                    if (y - 1) >= 0: # go to west
                        if tempHM[x][y - 1] != 999 and env[x][y - 1] == 0:
                            stonks.append([x, y - 1])
                            area.append([x, y - 1])
                            tempHM[x][y - 1] = 999
                    if (y + 1) < len(tempHM[x]): # go to east
                        if tempHM[x][y + 1] != 999 and env[x][y + 1] == 0:
                            stonks.append([x, y + 1])
                            area.append([x, y + 1])
                            tempHM[x][y + 1] = 999
                    if (x + 1) < len(tempHM): # go to south
                        if tempHM[x + 1][y] != 999 and env[x + 1][y] == 0:
                            stonks.append([x + 1, y])
                            area.append([x + 1, y])
                            tempHM[x + 1][y] = 999
                    if (x - 1) >= 0: # go to north
                        if tempHM[x - 1][y] != 999 and env[x - 1][y] == 0:
                            stonks.append([x - 1, y])
                            area.append([x - 1, y])
                            tempHM[x - 1][y] = 999
                    length = len(stonks)
                if len(area) > 150:
                    for cell in area:
                        RiverMap[cell[0]][cell[1]] = 1
    return RiverMap

def RemoveTrees(editor,worldSlice,area,heightmap,heightmapWithTrees):
    print("Removing trees") 
    begin_time=time()
    #-60がy座標下限,255が最大
    #area[0]area[1]が原点,area[2],area[3]が距離

    heightDiff =  heightmapWithTrees - heightmap
    for x in range(area[2]):
        for z in range(area[3]):
            if heightDiff[x][z] != 0:
                count=0
                while True: #木の幹を消す
                    name=worldSlice.getBlockGlobal((area[0]+x,heightmap[x][z]-count-1,area[1]+z))
                    if'_log' in name.id: 
                        heightDiff[x][z] += 1
                        count+=1
                    else:
                        break
                #for i in range(heightDiff[x][z]):
                    # print(area[0]+x, heightmap[x][y]+i, area[1]+y)
                geometry.placeCuboid(editor,[area[0]+x, heightmap[x][z]-count, area[1]+z],[area[0]+x, heightmap[x][z]-count+heightDiff[x][z]-1, area[1]+z], Block('air'))
                    #editor.placeBlock((area[0]+x, heightmap[x][z]-count+i, area[1]+z), Block('air'))
    end_time=time()
    print('RemoveTrees done time:',end_time - begin_time)



def CoverFluid(editor,heightmap, area, env, CoverRiver = 0):
    RiverMap = [[0 for k in range(len(heightmap[0]))] for j in range(len(heightmap))]
    if CoverRiver == 0:
        RiverMap = FindRiver(heightmap, env)
    print("Covering water and lava")
    def FindAdjacentType(x, y):
        tempHM = deepcopy(heightmap)
        stonks = []
        stonks.append([x,y])
        length = len(stonks)
        tempHM[x][y] = 999
        while length >= 1:
            x = stonks[0][0]
            y = stonks[0][1]
            stonks.pop(0)
            if ((y - 1) >= 0):  # go to west
                if tempHM[x][y - 1] != 999:
                    if env[x][y - 1] in [1,2,3]:
                        return env[x][y - 1]
                    else:
                        stonks.append([x, y - 1])
                        tempHM[x][y - 1] = 999
            if ((y + 1) < area[2]): # go to east
                if tempHM[x][y + 1] != 999:
                    if env[x][y + 1] in [1,2,3]:
                        return env[x][y + 1]
                    else:
                        stonks.append([x, y + 1])
                        tempHM[x][y + 1] = 999
            if ((x + 1) < area[3]): # go to south
                if tempHM[x + 1][y] != 999:
                    if env[x + 1][y] in [1,2,3]:
                        return env[x + 1][y]
                    else:
                        stonks.append([x + 1, y])
                        tempHM[x + 1][y] = 999
            if ((x - 1) >= 0): # go to north
                if tempHM[x - 1][y] != 999:
                    if env[x - 1][y] in [1,2,3]:
                        return env[x - 1][y]
                    else:
                        stonks.append([x - 1, y])
                        tempHM[x - 1][y] = 999
            length = len(stonks)
        return -1
    for x in range(area[2]):
        for y in range(area[3]):
            blockType = env[x][y]
            if (blockType == 0 and RiverMap[x][y] == 0) or (blockType == 4 and 'lava' in editor.getBlock(area[0]+1,heightmap[1][1]-1,area[1]+1)):
                blockID = FindAdjacentType(x, y)
                if blockID == 1:
                    editor.placeBlock((area[0]+x, heightmap[x][y]-1, area[1]+y), Block('grass_block'))
                elif blockID == 2:
                    editor.placeBlock((area[0]+x, heightmap[x][y]-1, area[1]+y), Block('sand'))
                elif blockID == 3:
                    editor.placeBlock((area[0]+x, heightmap[x][y]-1, area[1]+y), Block('stone'))
                else:
                    editor.placeBlock((area[0]+x, heightmap[x][y]-1, area[1]+y), Block('grass_block'))
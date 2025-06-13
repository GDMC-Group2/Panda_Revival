"""
Get the name of the block with the most occurrences in the specified area.

input:worldSlice
output:most common block name


Note: The number of types of block names is unknown.

getSubslice function: Get only the specified area of ​​the two-dimensional array.

"""

#biomeを情報元に追加したい
#改変
#何もなければ草ブロック
#寒冷地なら草+雪
#砂漠なら砂岩
#荒野なら赤砂岩



class SearchBlocks:
    def __init__(self, worldSlice, Area):
        self.worldSlice = worldSlice
        self.Area = Area
        self.blockDict = {}
        self.blockList = []
        self.mostCommonBlock = ""
        self.mostCommonBlockNum = 0
        self.biomeDict = {}
        self.biomeList = []
        self.mostCommonBiome = ""
        # self.mostCommonBlockList = []
        # self.mostCommonBlockNumList = []
        # self.blockNum = 0
        self.blockName = ""
        self.biomeName = ""
        # self.blockNumList = []
        # self.blockNameList = []
        self.heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # def getSubslice(self):
    #     return self.worldSlice[self.Area[0]:self.Area[0] + self.Area[2], self.Area[1]:self.Area[1] + self.Area[3]]

    def run(self):
        x1 = self.Area[0]
        z1 = self.Area[1]
        for x in range(self.Area[2]):
            for z in range(self.Area[3]):
                y = self.heightmap[x1+x, z1+z]
                self.blockName = self.worldSlice.getBlock((x1+x, y-1, z1+z))
                if self.blockName.id in self.blockDict:
                    self.blockDict[self.blockName.id] += 1
                else:
                    self.blockDict[self.blockName.id] = 1
                self.biomeName = self.worldSlice.getBiome((x1+x, y-1, z1+z))
                if self.biomeName in self.biomeDict:
                    self.biomeDict[self.biomeName] += 1
                else:
                    self.biomeDict[self.biomeName] = 1
        self.blockList = list(self.blockDict.items())
        self.blockList.sort(key=lambda x: x[1], reverse=True)
        self.mostCommonBlock = self.blockList[0][0]
        self.mostCommonBlockNum = self.blockList[0][1]

        self.biomeList = list(self.biomeDict.items())
        self.biomeList.sort(key=lambda x: x[1], reverse=True)
        self.mostCommonBiome = self.biomeList[0][0]
        # for i in range(len(self.blockList)):
        #     if self.blockList[i][1] == self.mostCommonBlockNum:
        #         self.mostCommonBlockList.append(self.blockList[i][0])
        #         self.mostCommonBlockNumList.append(self.blockList[i][1])
        #     else:
        #         break
        # self.blockNum = len(self.blockList)
        # for i in range(self.blockNum):
        #     self.blockNameList.append(self.blockList[i][0])
        #     self.blockNumList.append(self.blockList[i][1])
        # return self.mostCommonBlockList, self.mostCommonBlockNumList, self.blockNameList, self.blockNumList
        #変化
        if(self.mostCommonBlock=="minecraft:sand"):
            self.mostCommonBlock="sandstone"
        elif(self.mostCommonBlock=="minecraft:red_sand"):
            self.mostCommonBlock="red_sandstone"
        
        return self.mostCommonBlock , self.mostCommonBiome
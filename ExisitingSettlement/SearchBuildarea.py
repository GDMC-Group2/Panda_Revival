from gdpc import Editor, Block
from . import china_roof, Gmeans, SortCenters
from . import AStarRoutePlanner as AS
import numpy as np
from time import *
from box import Box
from terrian_adaptation import ICE_JIT_HeightMap as ice_jit_HMap
from terrian_adaptation import ICE_JIT_FlatFinder as ice_jit_F
from terrian_adaptation import ICE_JIT_BorderAreaFinder as ice_jit_S
from terrian_adaptation import ICE_JIT_GravityFinder as G
from terrian_adaptation import ICE_JIT_Pioneer as P
import road_generator as RG

# print("Editor")
# Here we construct an Editor object
#ED = Editor(buffering=True)

# print("Build area")
# Here we read start and end coordinates of our build area
#BUILD_AREA = ED.getBuildArea()  # BUILDAREA

# print("world slice")
#WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while
# print("heights")
#heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
# print("Loading")

class SearchBuildArea():
    def __init__(self,editor, area, heightmap, env, worldSlice):
        self.area = area
        self.heightmap = heightmap
        self.env = env
        self.worldSlice = worldSlice

    def output(self,editor):
        h = ice_jit_HMap.HeightMap(self.env, self.heightmap, self.area[0], self.area[1], self.area[0] + self.area[2],
                                   self.area[1] + self.area[3])
        f = ice_jit_F.FlatFinder(self.worldSlice, h)  # Flat area finding
        # candidate_points = f.getCandidatePoints()  # Flat area's lowest norm points
        f_area = f.getMergeArea()  # Merge flat area
        new_array = np.zeros((f_area.shape))
        centers, centers_ncd= self.findSettlement(editor,f_area, new_array)  # avoid clusters
        centers_int = [[int(num) for num in idx] for idx in centers]  # convert type to int from float
        border_map = ice_jit_S.BorderAreaFinder(f_area)  # Create border map
        area_with_border = border_map.getAreaMap()
        area_borders_in_order = border_map.getAllAreaBordersInOrder()  # Get borders in measure's order

        DecideArea = []
        mid_pos = []
        size = 0
        begin_time = time()
        for c_i in range(len(area_borders_in_order)):
            g = G.GravityFinder(area_borders_in_order[c_i])
            gravity_x, gravity_z = g.get_gravity_point2()
            p = P.Pioneer(h, area_with_border, f.mergeArea_meanHeight, self.area[0], self.area[1],
                          (gravity_x, gravity_z))
            u = p.getUtilization()
            if p.width >= 44 and p.height >= 44 and u > 0.5 and (p.x1, p.z1, p.width, p.height) not in DecideArea:
                for darea in DecideArea:
                    x1, y1, x2, y2 = p.x1, p.z1, p.x1 + p.width, p.z1 + p.height
                    x3, y3, x4, y4 = darea[0], darea[1], darea[0] + darea[2], darea[1] + darea[3]
                    if (max(x1, x3) < min(x2, x4)) and (max(y1, y3) < min(y2, y4)):
                        if x1 < x3:
                            x2 = x3
                        elif x1 > x3:
                            x1 = x4
                        p.x1, p.z1, p.width, p.height = (x1, y1, x2 - x1, y2 - y1)
                if p.width >= 44 and p.height >= 44:
                    DecideArea.append((p.x1, p.z1, p.width, p.height))
                    mid_pos.append((p.x1 + p.width // 2, p.z1 + p.height // 2))
                    size += p.width * p.height
                    if size > 90000:
                        print('size over')
                        break
            area_with_border = p.give_to_next()
        if type(DecideArea) == tuple:
            DecideArea = [DecideArea]
        end_time = time()
        DecideArea_sorted = sorted(DecideArea, key=lambda x: x[2] * x[3], reverse=True)
        print("Decide Areas:", end_time - begin_time)
        if mid_pos != []:
            begin_time = time()
            RoadGene = RG.RoadGenerator(editor,self.area, self.heightmap, new_array, area_with_border)
            maze = AS.make_maze(self.heightmap, area_with_border)
            m = mid_pos.copy()
            for one in centers_ncd:
                m.append((one[0], one[1]))
            centers_sorted = SortCenters.sort(m)
            for i in range(len(centers_sorted) - 1):
                print('-' * 30)
                start = (int(centers_sorted[i][0]), int(centers_sorted[i][1]))
                end0 = (int(centers_sorted[i + 1][0]), int(centers_sorted[i + 1][1]))
                r_start, r_end = RoadGene.find_real_start_end(start, end0)
                print("r_start:", r_start[0] + self.area[0], r_start[1] + self.area[1])
                print("r_end:", r_end[0] + self.area[0], r_end[1] + self.area[1])
                AS.set_star_end(maze, r_start, r_end)
                path_list = AS.run(maze)
                # print("path_list:", path_list)
                RoadGene.generate(editor,path_list)
            end_time = time()
            print("Generate Roads:", end_time - begin_time)
        return DecideArea_sorted
    
    def findSettlement(self,editor, f_area, new_array):
        natural_blocks = []
        f = open('natural_blocks_list.txt', 'r')
        for line in f.readlines():
            natural_blocks.append(line.split(' ')[0])
        f.close()
        # natural_blocks.remove('minecraft:sandstone')
        X = []
        ID_name_table = []
        s = np.zeros((self.area[2], self.area[3]), dtype=int)
        for x in range(self.area[2]):
            for z in range(self.area[3]):
                real_pos = (x + self.area[0], self.heightmap[x][z] - 1, z + self.area[1])
                block_info = self.worldSlice.getBlock(real_pos)
                if block_info.id not in natural_blocks:
                    # print(block_info.id)
                    if block_info.id in ID_name_table:
                        block_id = ID_name_table.index(block_info.id)
                    else:
                        # print(real_pos)
                        # print(block_info) # 既存集落とみなしたブロックを表示
                        block_id = len(ID_name_table)
                        ID_name_table.append(block_info.id)
                    s[x][z] = block_id
                    X.append([x, z])
        clusters, centers, clusters_ncd, centers_ncd = Gmeans.fit(np.array(X),
                                                                    pltshow=0)  # 重要　clusters：centersの周りの点　centers：クラスターの重心

        a = []
        for i in range(len(clusters_ncd)):
            x_min = 100000
            z_min = 100000
            x_max = -100000
            z_max = -100000
            for one_cluster in clusters_ncd[i]:
                if one_cluster[0] < x_min:
                    x_min = one_cluster[0]
                if one_cluster[0] > x_max:
                    x_max = one_cluster[0]
                if one_cluster[1] < z_min:
                    z_min = one_cluster[1]
                if one_cluster[1] > z_max:
                    z_max = one_cluster[1]
            a.append([x_min, x_max, z_min, z_max])
            f_area, new_array = self.ChangeArray(clusters, f_area, new_array)

        from random import randrange
        # Panda invade Settlement
        buildarea = {
            'begin' :{
                'x' : self.area[0],
                'y' : -60,
                'z' : self.area[1]
            },
            'end' : {
                'x' : self.area[0] + self.area[2],
                'y' : 200,
                'z' : self.area[1] + self.area[3]
            }
        }
        buildarea_box = Box(buildarea)
        editor.setBuildArea(buildarea_box)

        invaded_blocks = []
        roof_blocks_set = []
        for one_c in clusters:
            roof_height = -100
            roof_blocks = []
            for one_block_pos in one_c:
                x = one_block_pos[0]
                z = one_block_pos[1]
                y = self.heightmap[x][z]
                if y > roof_height:
                    roof_height = y

            for one_block_pos in one_c:
                x = one_block_pos[0]
                z = one_block_pos[1]
                y = self.heightmap[x][z]

                block_id = s[x][z]
                block_name = ID_name_table[block_id]
                if y == roof_height and ('stairs' in block_name):
                    # tester.placeBlock(x+area[0], y, z+area[1], 'minecraft:gold_block')
                    roof_blocks.append((x, y - 1, z))
                    invaded_blocks.append([x, y - 1, z, 'dark_prismarine_stairs', 0])
                elif y == roof_height and ('stone' in block_name or 'planks' in block_name):
                    # tester.placeBlock(x+area[0], y, z+area[1], 'minecraft:gold_block')
                    roof_blocks.append((x, y - 1, z))
                    invaded_blocks.append([x, y - 1, z, 'dark_prismarine', 1])

                if 'stairs' in block_name:
                    # print(block_name)
                    invaded_blocks.append([x, y - 1, z, 'dark_prismarine_stairs', 0])
                elif 'stone' in block_name or 'planks' in block_name:
                    invaded_blocks.append([x, y - 1, z, 'dark_prismarine', 1])
            if len(roof_blocks) > 0:
                roof_blocks_set.append(roof_blocks)
        roof_blocks_set_confirm = []
        for i in range(len(roof_blocks_set)):
            roof_height = roof_blocks_set[i][0][1]
            x_min = 100000
            z_min = 100000
            x_max = -100000
            z_max = -100000
            for j in range(len(roof_blocks_set[i])):
                x = roof_blocks_set[i][j][0]
                z = roof_blocks_set[i][j][2]
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if z > z_max:
                    z_max = z
                if z < z_min:
                    z_min = z
            check_flag = True
            for x in range(x_min, x_max + 1):
                real_pos = (x + self.area[0], roof_height - 1, z_min - 1 + self.area[1])
                # tester.placeBlock(x + area[0], heightmap[x][z_min] - 2, z_min - 1 + area[1], 'minecraft:gold_block')
                block_info = self.worldSlice.getBlock(real_pos)
                if 'stairs' not in block_info.id:
                    check_flag = False
                    break
                # print(block_info)
            if check_flag:
                y1 = roof_height + 1
                x1 = x_min + self.area[0]
                x2 = x_max + self.area[0]
                z1 = (z_max - z_min) // 2 + z_min + + self.area[1]
                roof_blocks_set_confirm.append([(x1, y1, z1), (x2, y1, z1), 'x'])
            # print(roof_height)

            else:
                check_flag_z = True
                for z in range(z_min, z_max + 1):
                    real_pos = (x_min - 1 + self.area[0], roof_height - 1, z + self.area[1])
                    block_info = self.worldSlice.getBlockGlobal(real_pos)
                    if 'stairs' not in block_info.id:
                        check_flag_z = False
                        break
                if check_flag_z:
                    y1 = roof_height + 1
                    z1 = z_min + self.area[1]
                    z2 = z_max + self.area[1]
                    x1 = (x_max - x_min) // 2 + x_min + + self.area[0]
                    roof_blocks_set_confirm.append([(x1, y1, z1), (x1, y1, z2), 'z'])

        for one_roof in roof_blocks_set_confirm:
            # print(one_roof)
            china_roof.make_roof(editor, one_roof[0], one_roof[1], orientation=one_roof[2])

        for one_block in invaded_blocks:
            x = one_block[0] + self.area[0]
            y = one_block[1]
            z = one_block[2] + self.area[1]
            block_info = ''
            if one_block[4] == 0:
                state_tag = self.worldSlice.getBlockGlobal((x, y, z)).states
                block_info = one_block[3]
                editor.placeBlock((x, y, z), Block(block_info, state_tag))
            elif one_block[4] == 1:
                block_info = one_block[3]
                editor.placeBlock((x, y, z), Block(block_info))
        for one_center in centers:
            x = int(one_center[0])
            z = int(one_center[1])
            y = self.heightmap[x][z]
            x += self.area[0]
            z += self.area[1]
            for i in range(5):
                rnd_x = x + randrange(-10, 10)
                rnd_y = y + randrange(5)
                rnd_z = z + randrange(-10, 10)
                editor.runCommand(
                    'summon minecraft:panda %d %d %d {MainGene:normal,HiddenGene:normal}' % (rnd_x, rnd_y, rnd_z))
        
        return centers, centers_ncd
    
    # Local Outlier Factor and detect the size of built Settlement
    def ChangeArray(self, clusters, f_area, new_array):
        # 既存集落を保存
        for cluster in clusters:
            for pos in cluster:
                f_area[pos[0], pos[1]] = -7 # same as -7
                new_array[pos[0], pos[1]] = 1
        return f_area, new_array


# def main():
#     try:
#     #     # setbuildarea -30 ~-10 150 500 100 500
#     #     # setbuildarea -4800 70 2630 100 100 100
#         # area = (-4800, 2630, 100, 100)
#         area = (-40, 200, 200, 200)
#         centers, centers_ncd = findSettlement(area, WORLDSLICE, heights)

#         print("Done!")

#     except KeyboardInterrupt: # useful for aborting a run-away program
#         print("Pressed Ctrl-C to kill program.")


# === STRUCTURE #4
# The code in here will only run if we run the file directly (not imported).
# This prevents people from accidentally running your generator.
# It is recommended to directly call a function here, because any variables
# you declare outside a function will be global.
# if __name__ == '__main__':
#     main()

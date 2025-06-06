from gdpc import Editor, Block, geometry,Transform
from Block_check import block_check,colored
import time
import cave_base
import winsound
import re
import requests
from requests.exceptions import ConnectionError
session = requests.Session()


def runCommand(command):
    url = 'http://localhost:9000/commands'
    try:
        response = session.post(url,command)
    except ConnectionError:
        return "connection error"
    return response.text

command="locate structure minecraft:stronghold"







#内容:build_areaの基準座標へテレポ
#そこから各建築物に対してlocate_commandを実行
#locateコマンドの結果テキストから各位置の座標を取得
#build_area内にあればを位置を記録し,特殊な処理を実行

#変数:WS_base_coor,WSの基準座標 WS_size:WSの大きさ
def scan_under_locate(WS_base_coor,WS_size):
    structure_list=["minecraft:ancient_city","minecraft:stronghold","minecraft:trial_chambers"]

    command=f"gamemode spectator"
    runCommand(command)
    x=WS_base_coor[0]
    y=WS_base_coor[1]
    z=WS_base_coor[2]
    command=f"tp @a {x} {y} {z}"
    runCommand(command)

    for i in range(len(structure_list)):
        command=f"locate structure {structure_list[i]}"
        text=runCommand(command)
        if(text[11]=="1"): #最初のstatus:の後ろの数字を見る
            locate_coor=re.search(r'は\[.*\]（',text) #一番右側の括弧は,全角括弧
            locate_coor_x=re.findall(r'\[(-*[0-9]+),',locate_coor.group())
            locate_coor_x=int(locate_coor_x[0])
            locate_coor_z=re.findall(r', ([-*0-9]+)\]',locate_coor.group())
            locate_coor_z=int(locate_coor_z[0])

            if(WS_base_coor[0]< locate_coor_x and WS_base_coor[0]+WS_size[0] > locate_coor_x):
                if(WS_base_coor[2] < locate_coor_z and WS_base_coor[1]+WS_size[2] > locate_coor_z):
                    print(f"{structure_list[i]} in area!!")
                    print(f"x:{locate_coor_x},z:{locate_coor_z}")
                    #この座標を基準に調査する.中心として,101*101(XZ)を調査.
                    #各エリアに関係のあるブロックが含まれていなければ箱を縮小
                    #このエリアは上下の取得を行わない.







        else:
            print(f"Do not find {structure_list[i]}")



WS_base_coor=[100,100,100]
WS_size=[500,256,500]
scan_under_locate(WS_base_coor,WS_size)






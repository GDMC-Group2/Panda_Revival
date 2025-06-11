from gdpc import Editor
import os

color_table=["black","dark_blue","dark_green","dark_aqua","dark_red","dark_purple",
            "gold","gray","dark_gray","blue","green","aqua","red","light_purple",
            "yellow","white"]

#関数定義 Block_check
#ある座標にテストエンティティを設置する
#必ずMinecraftの難易度をeasy以上にする事
#変数:座標(リスト型で複数を確保),色
#設置したエンティティは別関数で削除


def block_check(coor,col):
    y=coor[1]+0.42
    if(col in color_table):
        command=f"summon shulker_bullet {coor[0]} {y} {coor[2]} {{NoGravity:true,Glowing:true,Invulnerable:true,Tags:[dis,{col}]}}"
    else:
        command=f"summon shulker_bullet {coor[0]} {y} {coor[2]} {{NoGravity:true,Glowing:true,Invulnerable:true,Tags:[dis]}}"
    editor.runCommandGlobal(command)


def kill_marker():
    command=f"kill @e[tag=dis]"
    editor.runCommand(command)

def colored(color="None"):
#使っている色だけを呼び出す式にしたい
#変数定義の有無で変化
    #渡された変数が存在しない場合,全て呼び出す
    if(color=="None" or color not in color_table):
        for i in range(len(color_table)):
            command=f"team join {color_table[i]} @e[tag={color_table[i]}]"
            editor.runCommand(command)
    else:
        command=f"team join {color} @e[tag={color}]"
        editor.runCommand(command)


def team_setting():
    #シュルカーの玉(壁越しに発光する小さい玉)に色をつけるための部分
    #スコアボードとチームを利用して定義したい

    for i in range(len(color_table)):
        command_1=f"team add {color_table[i]}"
        editor.runCommand(command_1)
        command_2=f"team modify {color_table[i]} color {color_table[i]}"
        editor.runCommand(command_2)

    #こまごまとしたセット
    command=f"gamerule doDaylightCycle false"
    editor.runCommand(command)
    command=f"gamerule doMobSpawning false"
    editor.runCommand(command)

#初回実行時のみteam_settingを呼び出す
file_path=os.path.dirname(__file__)+"/"
file_name="Executed.txt"
if(os.path.isfile(file_path + file_name) == False):
    team_setting()
    open(file_name,mode='w')
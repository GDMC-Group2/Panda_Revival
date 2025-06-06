#洞窟拠点の設計
#考え方.
#1:床の張り替え cluster内の座標でできる
#2:天井の張り替え cluster内の座標から,上方向に空気ブロック化
#ただし,この処理は一回のバッファ処理で行う(事前にflushBufferでバッファを空にし,バッファサイズも上げる)
#3:壁の作成:エリアの端に壁を立てる
#5:脇つぶし:松明を等間隔に並べる
#4:建築物の作成:下に詳細を書く
#6:道の作成:建築物の間を結ぶ線を書く
#壁について
#壁が発生する場所
#マップ端
#高さが低い場所
#高さが低い場所を記録して置きたい


from gdpc import Editor, Block, geometry
from Block_check import block_check,colored


editor = Editor(buffering=False)

# #座標と壁の材質,高さを渡す


def build_wall(coor_wall_MC,wall_con,wall_height):
    for i in range(wall_height):
        editor.placeBlock([coor_wall_MC[0],coor_wall_MC[1]+i+1,coor_wall_MC[2]],Block(wall_con))


def clear_wall(coor_wall_MC,wall_height):
    for i in range(wall_height):
        editor.placeBlock([coor_wall_MC[0],coor_wall_MC[1]+i+1,coor_wall_MC[2]],Block("air"))

def build_floor(coor_MC,floor_con):
    editor.placeBlock([coor_MC[0],coor_MC[1],coor_MC[2]],Block(floor_con))


def build_ceiling(worldSlice,coor_WC,coor_MC,floor_con,no_stone_block):
    #天井+空間自体を整える.
    while(1):
        coor_WC[1]+=1 #一つ上のブロックを見る
        coor_MC[1]+=1
        block=worldSlice.getBlock(coor_WC)
        if(block.id in no_stone_block):
            editor.placeBlock(coor_MC,Block("air"))
        elif(block.id != "minecraft:air"):
            #液体や砂利の事を考えると,一括で処理したい...
            #editor.runCommand("tick freeze")　を利用するとブロックを止めれる
            editor.placeBlock(coor_MC,Block(floor_con))
            break




# coor_wall=[90,13,-133]
# wall_con="stone_bricks"
# wall_height=3
# build_wall(coor_wall,wall_con,wall_height)
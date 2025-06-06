from gdpc import Editor, Block, geometry
from Block_check import block_check,colored
import time
import cave_base
editor = Editor(buffering=False)



#buildareaの設定
#XL,YL,ZL=255
#y下限:-64
XS=64
YS=0
ZS=-143
XL,YL,ZL=128,256,128
coor_basis=[XS,YS,ZS]

command_build_area= f"setbuildarea {XS} {-64} {ZS} {XS+XL} {YS+YL} {ZS+ZL}"

editor.runCommand(command_build_area)



#条件2
#海抜よりも低い事.
#空洞が存在しない事(水,溶岩,空気ブロックの無いエリア.)
#このエリアに生産施設を建てる.

#方策:指定した高さのxz平面に建築できるエリアがあるかを調べる.
#この時,多少(エリア面積に対して10%未満?洞窟とかぶっていても無視する.)
#エリアの作成数は,利用可能エリアから計算する.
#今回のレギュレーションでは1000*1000マス
#全域探査はあまりしたくない(地下の場合,y座標) 


#条件1と2のエリアをつなぐ.


#
start = time.time()
worldSlice = editor.loadWorldSlice()

SEA_LEVEL=62#海抜の高さ
DEEP_LAYER=-20#深層岩の出現する高さ (y=8)

y_scan_range=SEA_LEVEL-DEEP_LAYER #調査する幅
#端っこは見る必要が薄いため,端っこは見ない.(8ブロック程度を無視)
IGNORE_LENGTH=2 #無視する長さ


#洞窟内に存在する,洞窟の壁を構成しないブロックのリスト #水に入っているかも調べる
no_stone_block=["minecraft:air","minecraft:short_grass","minecraft:big_dripleaf",
                   "minecraft:small_dripleaf","minecraft:moss_carpet","minecraft:azalea",
                   "minecraft:tall_grass","minecraft:big_dripleaf_stem","minecraft:cave_vines_plant",
                   "minecraft:cave_vines","minecraft:spore_blossom"]





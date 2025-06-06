#他のところで使えそうな関数の塊

def under_center_base_air(editor,coor,size):
    z_size=size[2]//2

    geometry.placeCuboid(editor,(0+coor[0]+1 ,0+coor[1]-1,-z_size),(0+coor[0]+size[0]+1,coor[1]+size[1],z_size),Block("air"))


def under_center_base_frame(editor,coor,size):
    z_size=size[2]//2
    geometry.placeCuboid(editor,(0+coor[0] ,0+coor[1]-2,-z_size-1),(0+coor[0]+size[0]+2,coor[1]+size[1]+2,z_size+1),Block("stone"))


#frame,baseの順で実行



def runCommand(command):
    """**Executes one or multiple minecraft commands (separated by newlines).**"""
    # print("running cmd " + command)
    url = 'http://localhost:9000/chunks'
    url+= command
    print(url)
    try:
        response = session.get(url,headers={'Accept':'text/plain'})
    except ConnectionError:
        return "connection error"
    return response.text




command='?x=8&z=15&dx=1&dz=1'

chunk=runCommand(command)
print(type(chunk))

f = open('chunk.txt', 'w')
f.write(chunk)
f.close()


#チャンクから地下建築物の情報を取得できる.
#x,z:x,z座標方向に幾つめのチャンクか
#dx,dz:幾つチャンクを調べるか
#チャンクの情報をまとめて確保できる.
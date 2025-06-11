from gdpc import Editor, Block, Transform, geometry

def air(editor,x,y,z,q_id):
    for xx in range(34):
        for yy in range(10):
            for zz in range(36):
                editor.placeBlock((x-17+xx,y-1+yy,z-16+zz),Block(q_id))
def Air(editor,x,y,z):
    air(editor,x,y-20,z,"air")

import os
import sys

blank = [chr(32)]  ##此处为空格格式;Windows控制台下可改为chr(12288) ;linux系统中可改为chr(32)【chr(32)==' ' ;chr(183)=='·' ;chr(12288)=='　'】
tabs = ['']
def DepthTraversal(nowDir, p):
    # 根据目录建立列表
    baseName = os.path.basename(nowDir)
    p.append(baseName)
    c = []    
    #c = [baseName]
    p.append(c)

    ls = os.listdir(nowDir)
    for each in ls:
        nextPath = os.path.join(nowDir, each)
        nextPath_basename = os.path.basename(nextPath)
        if os.path.isdir(nextPath):
            DepthTraversal(nextPath, c)
        else:
            nextPath_basename = os.path.basename(nextPath)
            c.append(nextPath_basename)
def tree(lst,level = 0):
    for name in lst:
        if isinstance(name,list):
            tree(name,level + 1)
        else:
            if level>0:
                print( (blank[0]*3) * level,name)
            else:
                print( name)

def tree1(lst):
    # 树状图输出列表
    l = len(lst)
    if l == 0:
        print('─' * 3)
    else:
        for i, j in enumerate(lst):
            if i != 0:
                #f.write(tabs[0])
                print(tabs[0], end='')
            if l == 1:
                s = '─' * 3
            elif i == 0:
                s = '┬' + '─' * 2
            elif i + 1 == l:
                s = '└' + '─' * 2
            else:
                s = '├' + '─' * 2
            #f.write(s)
            print(s, end='')
            if isinstance(j, list) or isinstance(j, tuple):
                if i + 1 == l:
                    tabs[0] += blank[0] * 3
                else:
                    tabs[0] += '│' + blank[0] * 2
                tree(j)
            else:
                print(j)
                #f.write(j + "\n")
    tabs[0] = tabs[0][:-3]

def travelTree(currentPath, count=0):
    if not os.path.exists(currentPath):
        print("no current Path")
        return 
    if os.path.isfile(currentPath):
        fileName = os.path.basename(currentPath)
        print( "  "*count + "|_ "+fileName )
    elif os.path.isdir(currentPath):
    	#print currentPath 
        print("  "*count + "|_ "+currentPath) 
        pathList = os.listdir(currentPath)
        for eachPath in pathList:
            travelTree(currentPath + '/' + eachPath, count + 1)
    else:
        print("\n")
    	#return
def main(args = None):
    if len(sys.argv) <=1:
        paths ='.'
    else:
        paths = sys.argv[1]
    try:
        path = os.path.abspath(paths)
    except IndexError:
        print("please input absolute path. bye bye.")
        exit()
    #f = open("out", 'w')
    TreeList = []
    DepthTraversal(path, TreeList)
    tree(TreeList)
    #travelTree(path)


if __name__ == '__main__':
    main()
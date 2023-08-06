import os
import sys
import shutil

curPath = '.'

def listFile(dirName):
    tmpPath = os.path.join(curPath,dirName)
    allPath = os.listdir(tmpPath)
    for p in allPath:
        curFile = os.path.join(tmpPath,p)
        print(curFile,end='-')
        if os.path.isfile(curFile):
            print('file')
        else:
            print('directory')
def walkFile(exts,fromDir,toDir):
    tmpPath = os.path.join(curPath,fromDir)
    for curDir,dirs,files in os.walk(tmpPath):
        for name in files:
            curFile = os.path.join(curDir,name)
            filePath, fileFullName = os.path.split(curFile)
            extension = fileFullName.split('.')[-1]
            if extension == exts:
                print('moving: {} '.format(fileFullName))
                shutil.move(curFile,toDir)
    print('Finished!')

def main(args = None):
    if len(sys.argv) <4 :
        print('usage: selectmv ext fromDir toDir.')
    else:
        fromPath = os.path.abspath(sys.argv[2])
        toPath = os.path.abspath(sys.argv[3])
        if not os.path.exists(fromPath):

            print('the directory [{}] dose not exist!'.format(fromPath))
            exit()
        if not os.path.exists(toPath):
            sel1 = input('the directory[{}] dose not exist!\n are you sure to create it?(y/n)'.format(toPath))
            if sel1 == 'y' or sel1 == 'Y':
                os.mkdir(toPath)
                print("the directory [{}] was created!".format(toPath))
            else:
                exit()

        print('will move all files with {} exts from[{}] to [{}]'.format(sys.argv[1],fromPath,toPath))
        sel = input('are you sure to move?(y/n)')
        if sel == 'y' or sel == 'Y':
            walkFile(sys.argv[1],fromPath,toPath)    
        #curPath = '.'
        #parentFile = os.path.join('..','tmpDir')
        #if not os.path.exists(parentFile):
        #    os.mkdir(parentFile)
        #else:
        #    print('notice the parent directory is already exist!')
        #walkFile('.',parentFile)
    

if __name__ == '__main__':
    main()
    

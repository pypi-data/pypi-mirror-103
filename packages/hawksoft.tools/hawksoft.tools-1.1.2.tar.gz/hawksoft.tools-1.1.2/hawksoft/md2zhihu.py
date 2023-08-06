import sys
import os
import re

def replace(file_name, output_file_name):
    try:
        pattern1 = r"\$\$\n*([\s\S]*?)\n*\$\$"
        new_pattern1 = r'\n<img src="https://www.zhihu.com/equation?tex=\1" alt="\1" class="ee_img tr_noresize" eeimg="1">\n'
        pattern2 = r"\$\n*(.*?)\n*\$"
        #new_pattern2 =r'\n<img src="https://www.zhihu.com/equation?tex=\1" alt="\1" class="ee_img tr_noresize" eeimg="1">\n'
        new_pattern2 =r'<img src="https://www.zhihu.com/equation?tex=\1" alt="\1" class="ee_img tr_noresize" eeimg="1">'
        f = open(file_name, 'r')
        f_output = open(output_file_name, 'w')
        all_lines = f.read()
        new_lines1 = re.sub(pattern1, new_pattern1, all_lines)
        new_lines2 = re.sub(pattern2, new_pattern2, new_lines1)
        f_output.write(new_lines2)
        f.close()
        f_output.close()
        print('{}->{}'.format(file_name,output_file_name))
    except ( e):
        print(e)

def dealFile(inputFile,outputFile='../'):
    input_dir = os.path.dirname(inputFile)
    input_name = os.path.basename(inputFile)
    input_name_noext = input_name.split('.')[0]
    if os.path.isdir(outputFile):
        output_dir = outputFile
        output_name = os.path.join(output_dir,input_name_noext+'_zhihu.md')
    else:
        output_dir= os.path.dirname(outputFile)
        output_name = outputFile
    return (inputFile,output_name)
def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if len(sys.argv) < 2:
        print("usage: md2zhihu sourceFileName destineFileName.")
        sys.exit(1)
    if len(sys.argv) < 3:
        tempDistine = "./"
    else:
        tempDistine = sys.argv[2]
    paras = dealFile(sys.argv[1],tempDistine)
    #print(paras)
    replace(*paras)

if __name__ == "__main__":
    main()
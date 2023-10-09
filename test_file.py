import os
import sys

MAGIC_CODE=b'cb'

def merge(file1,file2,output):
    with open(file1,'rb') as f1, open(file2,'rb') as f2, open(output, 'wb') as out:
        out.write(f1.read())
        out.write(f2.read())
        length = os.path.getsize(file1)
        out.write(length.to_bytes(4,byteorder='little'))
        out.write(MAGIC_CODE)

def unmerge(file,out1,out2):
    total = os.path.getsize(file)
    with open(file,'rb') as f, open(out1, 'wb') as out1, open(out2, 'wb') as out2:
        if(f.seek(-len(MAGIC_CODE),2) < 0):
            return False
        if(f.read() != MAGIC_CODE):
            return False
        f.seek(-len(MAGIC_CODE)-4,2)
        byteInt = f.read(4)
        offset = int.from_bytes(byteInt,byteorder='little')
        f.seek(0)
        out1.write(f.read(offset))
        out2.write(f.read(total-offset-len(MAGIC_CODE)-4))
        return True
        
def test_merge():
    merge("test_zip.py","test_gui.py",".tmp/test.bin")
    if not unmerge(".tmp/test.bin",".tmp/test_zip2.py",".tmp/test_gui2.py"):
        print("unmerge failed")

if __name__ == '__main__':
    args = sys.argv[1:]
    match args:
        case ['merge',file1,file2]:
            merge(file1,file2,file1+".mg")
        case ['merge',file1,file2,output]:
            merge(file1,file2,output)
        case ['unmerge',file]:
            unmerge(file,file+".1",file+".2")
        case ['unmerge',file,out1,out2]:
            unmerge(file,out1,out2)
        case _:
            print("Usage: python file.py merge|unmerge",args)
    #test_merge()
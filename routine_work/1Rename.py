import os,re
_1path="."
from nt import chdir
chdir(_1path)
for item in os.listdir(_1path):
    _1Re=re.match("^.*?([0-9a-z\-\_]+).*?(\.mp4|\.mts)",item,re.I)
    if _1Re:
        newname=_1Re.group(1)+_1Re.group(2)
        os.rename(item,newname)
        print(item+"-->"+newname)
input()

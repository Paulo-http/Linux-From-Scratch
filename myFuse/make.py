#
#  make.py
#  ADO_SO
#
#  Created by Paulo Henrique Leite on 12/10/16.
#

#!/usr/bin/python
import sys
import os
from src.file import File, Directory, Stat
from src.structure import Inode, Direction
import src.crypt as crypt

# help for user
def usage():
  print "make.py <image directory>\n"

if len(sys.argv) != 2:
  print "ERROR: wrong number of arguments\n"
  usage()
  quit()

# get param
dir = sys.argv[-1]
if dir.find("/") == -1:
    dir += "/"

# generate secret key for root
key = crypt.GenerateKey()
print "Secret key for root: ",key[1], "\n"

# get png files
print "Scanning for PNG files for implement steganography in", dir, "\n"
files = []
dirl = os.listdir(dir)
for name in dirl:
  if name.split(".")[-1] == "png":
    files.append(name)

# check if has 4 images
if len(files) < 4:
  print "ERROR: Not enough images. It is required 4 PNG files.\n"
  quit()

print "Files used:", files
print
print "1 for the inode of the root"
print "1 for the inode of the .freefile"
print "2 for the blocks of the root and .freefile\n"

print "Using", files[0], "as the root inode"
fopen = open("usage.txt", "r+")
fopen.write("root_key: " + key[1])
fopen.write("\nprefix: " + dir)
fopen.write("\nroot_inode: " + files[0])
fopen.close()

# load image for root dir
inode_img = files[0]
del files[0]

# create inode for root dir
inode = Inode(inode_img, key[1], new=True, prefix=dir)
inode.set_name("/")
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.add_direction_str(Direction("0|||$"))
inode.file_size = 0
inode.type = "1"
inode.save_data()

print "Creating .freefile\n"

f = Directory(inode, files, prefix=dir)
f.mkfile(".freefile")

freefile = File(f.dirs[".freefile"], files, prefix=dir)
freefile.write("$".join(files), 0)
freefile.save_data()
f.save_data()
freefile.truncate(len("$".join(files))-1)
freefile.write("$".join(files), 0)
freefile.save_data()

print "Finsh! To start use:"
print "python myFuse.py <mountdir>"

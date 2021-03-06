#
#  file.py
#  ADO_SO
#
#  Created by Paulo Henrique Leite on 12/10/16.
#

#!/usr/bin/python
import stat
from structure import Inode, Block, Direction
import crypt
from fuse import Stat

class Stat(Stat):
  def __init__(self):
    self.st_mode = stat.S_IFDIR | 0755
    self.st_ino = 0
    self.st_dev = 0
    self.st_nlink = 0
    self.st_uid = 1000
    self.st_gid = 1002
    self.st_size = 4096
    self.st_atime = 0
    self.st_mtime = 0
    self.st_ctime = 0

class File(object):
  def __init__(self, inode, free=[], prefix=""):
    self.inode = inode
    self.free = free
    self.prefix = prefix
    self.count = 0

  def __del__(self):
    self.save_data()

  def release(self):
    self.save_data()

  def save_data(self):
    self.inode.save_data()
    
  def read(self, size, offset):    
    found = False
    block = None
    if self.count > offset:
      if not (self.inode.current_block() is None):
        block = self.inode.current_block()
        found = self.count <= offset
      while self.inode.exists_prev_block() and not found:
        block = self.inode.prev_block()
        found = (self.count-block.size) <= offset
        if not found:
          self.count -= block.size
    else:
      if not (self.inode.current_block() is None):
        block = self.inode.current_block()
        found = self.count+block.size > offset
      while self.inode.exists_next_block() and not found:
        block = self.inode.next_block()
        found = self.count+block.size > offset
        if not found:
          self.count += block.size

    if block is None:
      return str()

    newfrom = offset
    newsize = size
    data = ""

    while newsize > 0 and (newfrom - self.count) < block.size and newfrom < self.inode.file_size:
      data += str(block[newfrom - self.count])
      newfrom += 1
      newsize -= 1

    if newfrom >= self.inode.file_size:
      return str(data)

    if newsize > 0:
      data += self.read(newsize, newfrom)
    
    return str(data)

  def write(self, buf, offset):    
    self.inode.rewind()
    found = False
    count = 0
    block = None
    while self.inode.exists_next_block() and not found:
      block = self.inode.next_block()
      found = count+block.size > offset
      if not found:
        count += block.size

    if not found and (self.inode.file_size - offset) <= 0:
      if len(self.free) == 0:
        return

      byte,key = crypt.GenerateKey()
      type = 1

      newblock = Block(self.free[0], key, new=True, prefix=self.prefix)
      self.inode.add_direction(type, newblock.src, newblock.size, newblock.key)

      del self.free[0]
      block = self.inode.next_block()
    
    if block is None:
      return

    newfrom = offset
    newsize = len(buf)
    written = 0

    while newsize > 0 and (newfrom - count) < block.size:
      block[newfrom - count] = buf[newfrom - offset]
      newfrom += 1
      newsize -= 1
      written += 1
      if newfrom > self.inode.file_size:
        self.inode.set_size(self.inode.file_size + 1)

    if newsize > 0:
      written += self.write(buf[newfrom - offset:], newfrom)

    return written

  def getattr(self):
    st = Stat()
    st.st_size = self.inode.file_size
    st.st_mode = stat.S_IFREG | 0666
    return st

  def truncate(self, length):
    self.modified = True
    old = self.inode.file_size
    diff = length - old
    if diff > 0:
      self.write("\0"*diff, old)
    else:
      self.inode.file_size = length

class Directory(File):
  def __init__(self, inode, free=[], prefix=""):
    super(Directory, self).__init__(inode, free, prefix)
    self.dirs = dict()
    self.readdir(0)

  def __del__(self):
    self.save_data()

  def readdir(self, offset):
    self.dirs["."] = None
    self.dirs[".."] = None
    
    data = self.read(self.inode.file_size, 0).split("$")
    for dir in data:
      if len(dir) != 0:
        d = Direction(dir)
        inode = Inode(d.path, d.key, prefix=self.prefix)
        self.dirs[inode.name] = inode

  def mkdir(self, name, offset=0):
    self.mkobj(name, offset, "1")

  def mkfile(self, name):
    self.mkobj(name, 0, "0")

  def mkobj(self, name, offset=0, type="0"):
    if len(self.free) == 0:
      return

    if name in self.dirs.keys():
      return

    print "Generating random key"
    key = crypt.GenerateKey()

    inode_img = self.free[0]
    print "Creating inode with %s" % inode_img
    inode = Inode(inode_img, key[1], new = True, prefix=self.prefix)
    print "Setting new data"
    del self.free[0]

    inode.type = type
    inode.set_name(name)
    for x in xrange(0,12):
      inode.add_direction_str(Direction("0|||$"))    
    inode.file_size = 0

    print "Saving new inode data"
    inode.save_data()

    self.dirs[name] = inode
    self.inode.modified = True

  def is_empty(self):
    return len(self.dirs)

  def delete(self, name):
    obj = self.dirs[name]
    if obj.is_dir() and not Directory(obj, obj.key, self.prefix).is_empty():
      return

    self.free.append(obj.src)
    obj.rewind()
    while obj.exists_next_block():
      self.free.append(obj.next_block().src)

    self.inode.modified = True
    del self.dirs[name]
    self.save_data()
    self.readdir(0)

  def getattr(self):
    st = Stat()
    return st

  def save_data(self):
    if not self.inode.modified:
      return
    data = ""
    for k in self.dirs:
      if self.dirs[k] is None:
        continue      
      data += "1|" + self.dirs[k].src + "|" + str(self.dirs[k].size) + "|" + self.dirs[k].key + "$"

    if len(data) < self.inode.file_size:
      self.truncate(len(data))
    self.write(data,0)
    self.inode.save_data()

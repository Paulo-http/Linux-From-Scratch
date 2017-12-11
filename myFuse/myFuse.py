import stat
import errno
import fuse
from time import time
from subprocess import *
from src.file import File, Directory, Stat
from src.structure import Inode

fuse.fuse_python_api = (0, 2)

class myFuse(fuse.Fuse):

  # get all params for init fuse 
  def __init__(self, *args, **kw):
    fuse.Fuse.__init__(self, *args, **kw)
    self.root = raw_input("Root inode: ")
    self.key = raw_input("Encryption key: ")
    self.prefix = raw_input("Prefix: ")
    inode = Inode(self.root, self.key, prefix=self.prefix)
    self.root_dir = Directory(inode, prefix=self.prefix)
    self.freefile = File(self.root_dir.dirs[".freefile"])
    self.free = self.freefile.read(self.freefile.inode.file_size, 0).split("$")
    self.root_dir.free = self.free
    self.last_objs = dict()
    print """
    \n# use read to read a file
    \n# use write to write a file
    \n# use mkdir to make a directory
    \n# use rmdir to remove a directory
    \n"""

  # used to return the file or directory of the last element
  def get_obj(self, path):
    if path in self.last_objs.keys():
      return self.last_objs[path]
    pe = path.split('/')[1:]
    step = 0
    current = self.root_dir
    whole_path = ""
    for part in pe:
      in_cache = False
      whole_path += "/"+part
      if whole_path in self.last_objs.keys():
        in_cache = True
        current = self.last_objs[whole_path]
      else:
        if current.dirs[part].is_dir():
          current = Directory(current.dirs[part], self.free, prefix=self.prefix)
        elif part != pe[-1]:
          return -errno.ENOENT
        else:
          current = File(current.dirs[part], self.free, prefix=self.prefix)
      if not in_cache:
        self.last_objs[whole_path] = current
    return current

  def release(self, path, flags):
    self.freefile.truncate(len("$".join(self.free))-1)
    self.freefile.write("$".join(self.free), 0)
    self.freefile.save_data()
    return 0

  def getattr(self, path):
    st = Stat()
    if path == '/':
      pass
    else:
      try:
        obj = self.get_obj(path)
        st = obj.getattr()
      except:
        return -errno.ENOENT
    return st

  # used to read file
  def read(self, path, size, offset):
    f = self.get_obj(path)
    return f.read(size, offset)

  # used to write file
  def write(self, path, buf, offset):
    f = self.get_obj(path)
    written = f.write(buf, offset)
    f.save_data()
    return written
  
  # used to make directory
  def mkdir(self, path, mode):
    elems = path.split('/')
    npath = "/".join(elems[:-1])
    if npath == "":
      self.root_dir.mkdir(elems[-1])
      self.root_dir.save_data()
    else:
      d = self.get_obj(npath)
      d.mkdir(elems[-1])
      d.save_data()
    self.release("",0)
    return 0

  # used to remove directory
  def rmdir(self, path):
    elems = path.split('/')
    npath = "/".join(elems[:-1])
    if npath == "":
      self.root_dir.delete(elems[-1])
      self.root_dir.save_data()
    else:
      d = self.get_obj(npath)
      d.delete(elems[-1])
      d.save_data()
    self.release("",0)
    return 0

# dash_s_do: use whine, undef, or setsingle. [default is whine]
def main():  
  usage  = fuse.Fuse.fusage
  server = myFuse(version=fuse.__version__, usage=usage, dash_s_do='setsingle')
  server.parse(errex=1)
  server.main()  

if __name__ == '__main__':
  main()
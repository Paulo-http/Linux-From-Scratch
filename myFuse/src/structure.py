#
#  structure.py
#  ADO_SO
#
#  Created by Paulo Henrique Leite on 12/10/16.
#

#!/usr/bin/python
import os
import crypt
from PIL import Image
import stepic

class Block(object):
  def __init__(self, src, key, new=False, prefix=""):
    self.size = 0
    self.src = src
    self.key = key
    self.modified = False
    self.data = []
    self.prefix = prefix
    if new:
      self.format_image()
      print "Done!\n"

    self.process_data()

  def __del__(self):
    self.save_data()

  def __getitem__(self, i):
    return self.data[i]

  def __setitem__(self, i, value):
    self.modified = True
    self.data[i] = value

  def __len__(self):
    return len(self.data)

  def process_data(self):
    enc_im = Image.open(self.prefix+self.src)
    self.size = enc_im.size[0] * enc_im.size[1] / 3
    enc_comp_data = stepic.decode(enc_im)
    self.data = list(crypt.decode(self.key, enc_comp_data))

    self.size = len(self.data)

  def save_data(self):
    if not self.modified:
      return

    im = Image.open(self.prefix+self.src)
    encoded = crypt.encode(self.key, ''.join(self.data))
    enc_im = stepic.encode(im, encoded)
    enc_im.save(self.prefix+self.src)
    self.modified = False
    return

  def dump(self):    
    print ''.join(self.data)

  def format_image(self):
    print "Formatting ", self.src
    im = Image.open(self.prefix+self.src)
    data_size = im.size[0] * im.size[1] / 3
    if data_size % 16 != 0:
      data_size += data_size % crypt.block_size
      data_size -= 32
    print "Image size: (", im.size[0], ",", im.size[1], ")"
    print "Possible data inside this block:", (data_size/1024), "Kb"
    data_size -= 32
    data = "$"*data_size
    enc_data = crypt.encode(self.key, data)
    im = stepic.encode(im, enc_data)
    im.save(self.prefix+self.src)
    return data_size


class Direction(object):
  def __init__(self, src):
    self.src = src
    self.type = "0"
    self.path = ""
    self.size = 0
    self.key = ""
    
    self.parse_string("|")

  def parse_string(self, sep):
    tmp = ''.join(self.src).split(sep)
    self.type = tmp[0][-1]
    if self.type == "0":
      return
    self.path = tmp[1]
    self.size = int(tmp[2])
    self.key = tmp[3]

  def __str__(self):
    tmp = self.type
    tmp += "|"
    tmp += self.path[0:255]
    tmp += "|"
    tmp += str(self.size)
    tmp += "|"
    tmp += self.key
    tmp += "$"

    return tmp

class Inode(Block):
  def __init__(self, src, key, new=False, prefix=""):
    self.new = new
    self.current = -1
    self.name = ""
    self.type = "0"
    self.directions = []
    self.file_size = 0
    super(Inode, self).__init__(src, key, new, prefix)

  def is_dir(self):
    return self.type == "1"

  def process_data(self):
    super(Inode, self).process_data()

    if self.new:
      return

    self.name = ""
    i = 0

    while True:
      if self.data[i] == "$":
        break
      self.name += self.data[i]
      i += 1

    i += 1
    tmpsize = "0"
    while True:
      if self.data[i] == "$":
        break
      tmpsize += self.data[i]
      i += 1

    self.file_size = int(tmpsize)

    i += 1
    self.type = self.data[i]
    i += 1

    for dir in xrange(0, 12):
      init = i
      while True:
        i += 1
        if self.data[i] == "$":
          end = i
          break
        
      self.directions.append(Direction(''.join(self.data[init:end])))
      i += 1
  
  def set_name(self, str):
    self.modified = True
    self.name = str[0:254]

  def set_size(self, size):
    self.modified = True
    self.file_size = size

  def add_direction(self, type, path, size, key):
    self.add_direction_str(Direction(str(type)+"|"+path+"|"+str(size)+"|"+key+"$"), self.current+1)

  def add_direction_str(self, direction, index=-1):
    if index == -1 and len(self.directions) < 12:
      self.directions.append(direction)
    elif index < len(self.directions):
      self.directions[index] = direction

  def save_data(self):
    if not self.modified:
      return

    i = 0
    tmpname = self.name
    tmpname += "$"
    for char in tmpname:
      self[i] = char
      i += 1

    tmpsize = str(self.file_size)
    tmpsize += "$"
    for char in tmpsize:
      self[i] = char
      i += 1

    self[i] = self.type
    i += 1
    
    for dir in xrange(0, 12):
      dir_str = str(self.directions[dir])
      for char in dir_str:
        self[i] = char
        i += 1

    super(Inode, self).save_data()

    self.rewind()
    while self.exists_next_block():
      self.next_block().save_data()

    self.modified = False

  def exists_next_block(self):
    if self.current < 9 and self.directions[self.current+1].type != "0":
      return True
    return False

  def exists_prev_block(self):
    if self.current > 0 and self.directions[self.current-1].type != "0":
      return True
    return False

  def prev_block(self):
    if self.current > 0 and self.directions[self.current-1].type != "0":
      self.current -= 1
      return Block(self.directions[self.current].path, self.directions[self.current].key, prefix=self.prefix)
    return None

  def next_block(self):
    if self.current < 9 and self.directions[self.current+1].type != "0":
      self.current+=1
      return Block(self.directions[self.current].path, self.directions[self.current].key, prefix=self.prefix)
    return None

  def rewind(self, i=-1):
    if i > 9:
      return
    self.current = i

  def current_count(self):
    if self.current == -1:
      return 0

    count = 0
    i = 0
    while self.current != i:
      count += dir.size
      i += 1

    return count

  def current_block(self):
    if self.current == -1:
      return None
    return Block(self.directions[self.current].path, self.directions[self.current].key, prefix=self.prefix)

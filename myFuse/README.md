### How to use it?

First, you need to format your fuse partition. Is recommended using a lot of medium size images (512x512), so you'll be able to have both space and speed.

To format the partition, you'll do the following:

	$ cd <path to the code>
	$ python make.py <path to images>

After:

	$ python myFuse.py <path to mount>

Let's see an example:

	$ cd /home/user/
	$ python myFuse.py mountdir/
	Root inode: image.png
	Encryption key: your key
	Prefix: images/
	<do your filesystemy stuff here>
	$ fusermount -u mountdir

### Some Methods

# use read to read a file
# use write to write a file
# use mkdir to make a directory
# use rmdir to remove a directory

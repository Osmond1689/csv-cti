import hashlib

md5=hashlib.md5()

md5.update(b'test')

print (md5.hexdigest())
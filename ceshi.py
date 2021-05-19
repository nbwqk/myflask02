import hashlib

a=hashlib.md5('hello'.encode('utf-8')).hexdigest() # 32 位
c=hashlib.sha512('hello'.encode('utf-8')).hexdigest() # 128位
b=hashlib.sha256('hello'.encode('utf-8')).hexdigest() # 64 位
print(a)
print(b)
print(c)
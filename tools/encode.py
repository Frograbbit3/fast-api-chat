import zlib
file1 = open("cert.pem","rb").read()
file2 = open("key.pem","rb").read()


def hash(v):
    return zlib.crc32(v)

with open("saved.cmp", "wb") as file:
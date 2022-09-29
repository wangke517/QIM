
import gzip
import hashlib
import os
from reedsolo import RSCodec

# 自定义 
sr_file_path = 'zip/secret.py'   # 源文件路径名
cp_file_path = 'zip/s.bin' # 压缩后文件路径名
dc_file_path = 'zip/dec_secret.py'  # 解压后文件路径名
rs = RSCodec(47)

# 获取文件 MD5 码
def getMD5(filename):
    with open(filename,'r') as f:
        tmp = f.read(1024).encode()
    fmd5 = hashlib.md5(tmp).digest()
    return fmd5

# 以byte的形式读取文件
def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf) 
    return buf

# 压缩文件
def zipfile(filename,cp_filename):
    data_in = read_into_buffer(filename)  
    data_out = gzip.compress(data_in,9)

    with open(cp_filename,'wb') as f:
        f.write(data_out)

# 解压文件
def unzipfile(cp_filename,dc_filename):

    tmp = read_into_buffer(cp_filename)
    data_in = gzip.decompress(tmp).decode()

    with open(dc_filename,'w') as f:
        f.write(data_in)

# 差错控制编码
def RS_encode(arry):
    encoded_code = rs.encode(bytearray(arry))
    return encoded_code

# 差错控制解码
def RS_decode(arry):
    decoded_code = rs.decode(arry)
    return decoded_code

def main():
    # 计算源文件MD5码
    Inmd5 = getMD5(sr_file_path)

    # 压缩文件
    zipfile(sr_file_path,cp_file_path)

    # 解压文件
    unzipfile(cp_file_path,dc_file_path)

    # 计算解压文件的MD5码
    Outmd5 = getMD5(dc_file_path)

    # 校验 解压文件 
    print(Inmd5 == Outmd5)

    arry = read_into_buffer(cp_file_path)
    # print(arry)
    # print(len(arry))

    encoded_file = RS_encode(arry)

    # 将加了纠错码的编码进行压缩并存储
    encoded_allData = gzip.compress(encoded_file, 9)
    with open('compressedAllData.bin','wb') as f:
        f.write(encoded_allData)
    
    # print(len(encoded_file))

    # 测试 纠错能力  
    encoded_file[0] = encoded_file[2]
    encoded_file[260] = encoded_file[266]
    encoded_file[780] = encoded_file[800]
    encoded_file[1030] = encoded_file[1040]

    decoded_msg, decoded_msgecc, errata_pos = RS_decode(encoded_file)
    
    print(decoded_msg == arry)
    # print(list(errata_pos))

if __name__ == '__main__':
    main()


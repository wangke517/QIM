import gzip_ecc as gz
# import QIM
import non_blind_QIM as QIM

# 自定义
sr_file_path = 'zip/secret.py'   # 源文件路径名
cp_file_path = 'zip/s.bin' # 压缩后文件路径名
dc_file_path = 'zip/dec_secret.py'  # 解压后文件路径名
cp_allFile_path = 'zip/compressedAllData.bin' # 加了纠错码后压缩后文件路径名
# # 计算源文件MD5码
# Inmd5 = gz.getMD5(sr_file_path)

# 压缩文件
gz.zipfile(sr_file_path,cp_file_path)

# # 解压文件
# gz.unzipfile(cp_file_path,dc_file_path)

# # 计算解压文件的MD5码
# Outmd5 = gz.getMD5(dc_file_path)

arry = gz.read_into_buffer(cp_file_path)
print(type(arry))

# 加纠错
encoded_file = gz.RS_encode(arry)

 # 将加了纠错码的编码进行压缩并存储
# encoded_allData = gz.gzip.compress(encoded_file, 9)
# 存储
with open(cp_allFile_path,'wb') as f:
    f.write(encoded_file)

data = QIM.read_bin_data(cp_allFile_path)
cover_spa = QIM.read_jpeg(r"cover65_2.png")
dct_coff = QIM.block_dct(cover_spa)
ori_dct = dct_coff.copy()
stego_dct = QIM.Qim_embed(dct_coff,data)
stego_image = QIM.get_stego(stego_dct)
QIM.cv2.imwrite("stego_65_2.png",stego_image)
# QIM.cv2.imwrite("stego_65_no_blind.png",stego_image)
stego_spa = QIM.read_jpeg("pic/stego_65_2compress55.jpg")

stego_dct = QIM.block_dct(stego_spa)
# recover_data = QIM.Qim_extract(stego_dct,len(data))
recover_data = QIM.Qim_extract(stego_dct,len(data),ori_dct)
ori_data= QIM.np.array([int(i) for i in data])
recover_data = QIM.np.array([int(i) for i in recover_data])
error = QIM.np.abs(ori_data - recover_data)
error_rate = QIM.np.mean(error)
print(QIM.psnr(cover_spa, stego_spa))
print(error_rate)

newData = ""
for i in recover_data:
    newData  = newData + str(i)

bytes_msg = bytes(int(newData[i:i+8],2)for i in range(0, len(newData),8))
array_msg = bytearray(bytes_msg)

# 提取出来的数据解压缩
# data_in = gz.gzip.decompress(newData).decode()

# 纠错码解码
decoded_msg, decoded_msgecc, errata_pos = gz.RS_decode(array_msg)

# print(decoded_msg == arry)

data2 = gz.gzip.decompress(decoded_msg).decode()

with open(dc_file_path,'w') as f:
    f.write(data2)
# Inmd5 = gz.getMD5(sr_file_path)
# Outmd5 = gz.getMD5(dc_file_path)
f=open(sr_file_path)
sr=f.read()
f2=open(dc_file_path)
dc=f2.read()
print(dc == sr)
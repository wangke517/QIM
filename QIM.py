import cv2
import numpy as np
from scipy import io


import math

# import jpegio as jio
q_table = io.loadmat('q_table_65.mat')['Q_table']

Zig=np.array([
            0, 1, 5, 6, 14, 15, 27, 28,
            2, 4, 7, 13, 16, 26, 29, 42,
            3, 8, 12, 17, 25, 30, 41, 43,
            9, 11, 18, 24, 31, 40, 44, 53,
            10, 19, 23, 32, 39, 45, 52, 54,
            20, 22, 33, 38, 46, 41, 55, 60,
            21, 34, 37, 47, 50, 56, 59, 61,
            35, 36, 48, 49, 57, 58, 62, 63
        ])


def read_jpeg(file_path):
    '''
    读取JPEG文件并转换为float格式，cv2需要使用float才可以进行dct变换
    :param file_path:
    :return:
    '''
    cover_spa=cv2.imread(file_path,cv2.IMREAD_GRAYSCALE)
    return cover_spa.astype(float)

def block_dct(image):
    '''
     分块DCT
     :param image: numpy格式的数据
     :return:
     '''
    H,W=image.shape
    Hn=H//8
    Wn=W//8
    block_dct=image.copy()
    for h in range(Hn):
        for w in range(Wn):
            # 对图像块进行dct变换
            img_block = image[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)]
            block_dct[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)] = cv2.dct(img_block)

    return block_dct



def read_bin_data(binData):
    '''
       读取二进制数据，注意返回的二进制数据是字符串
       :return:
       '''
    file=open(binData,"rb")
    data=file.read()
    file.close()
    binary_code=''.join(format(x,'08b') for x in data)
    return binary_code

def find_AC(block,num_AC):
    '''
     寻找合适的AC系数进行隐藏，还没想好怎么写，可以先不用。
     :param block:
     :param num_AC:
     :return:
     '''
    AC=[]
    num=0
    for i in range(7,-1,-1):
        for j in range(7,-1,-1):
            if(block[i,j]!=0):
                AC.append((i,j))
                num+=1
            if(num>=num_AC):
                return AC


def psnr(x, y):
    squre_sum = np.sum(np.square(x - y))
    mse = squre_sum / (x.shape[0] * x.shape[1])
    result = 20 * math.log10(255 / math.sqrt(mse))
    return result


def Qim_embed(block_dct,bin_data):
    '''
    嵌入
    :param block_dct:
    :param bin_data:
    :return:
    '''
    num_ac=2
    # for bin_data in bin_data:
    H, W = block_dct.shape
    Hn = H // 8
    Wn = W // 8
    data_len=len(bin_data)
    data_index=0
    for h in range(Hn):
        for w in range(Wn):
            block=block_dct[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)]
            # AC=find_AC(block,num_ac)
            AC=[(2,2),(4,4)]
            if(AC!=None):
                for index in AC:
                    round_ac=np.round(block[index[0],index[1]]/q_table[index[0],index[1]])#round_ac表示量化后的AC系数

                    if(np.mod(round_ac,2)==0):
                        if(bin_data[data_index]=='0'):
                            # block[index[0], index[1]]=round_ac*q_table[index[0],index[1]]
                            pass
                        else:
                            round_ac2=np.floor(block[index[0],index[1]]/q_table[index[0],index[1]])
                            if(np.mod(round_ac2,2)==1):
                                block[index[0], index[1]] = (round_ac+1)*q_table[index[0],index[1]]
                            else:
                                block[index[0], index[1]] = (round_ac-1) * q_table[index[0], index[1]]
                    else:
                        if (bin_data[data_index] == '1'):
                            # block[index[0], index[1]] = round_ac * q_table[index[0], index[1]]
                            pass
                        else:
                            round_ac2 = np.floor(block[index[0], index[1]] // q_table[index[0], index[1]])
                            if (np.mod(round_ac2, 2) == 1):
                                block[index[0], index[1]] = (round_ac + 1) * q_table[index[0], index[1]]
                            else:
                                block[index[0], index[1]] = (round_ac - 1) * q_table[index[0], index[1]]
                    data_index+=1
                    if(data_index>=data_len):
                        return block_dct


def Qim_extract(block_dct,secret_length):
    '''
      提取
      :param block_dct:
      :param secret_length:
      :return:
      '''
    num_ac=2
    # for bin_data in bin_data:
    H, W = block_dct.shape
    Hn = H // 8
    Wn = W // 8
    data=""
    for h in range(Hn):
        for w in range(Wn):
            block=block_dct[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)]
            # AC=find_AC(block,num_ac)
            AC=[(2,2),(4,4)]
            if(AC!=None):
                for index in AC:
                    round_ac=np.round(block[index[0],index[1]]/q_table[index[0],index[1]])
                    if(np.mod(round_ac,2)==0):
                        data=data+"0"
                    else:
                        data=data+"1"
                    if(len(data)>=secret_length):
                        return data



def get_stego(block_dct):
    '''
      从block_dct还原为空域图片
      :param block_dct:
      :return:
      '''
    recover_image=block_dct.copy()
    H, W = block_dct.shape
    Hn = H // 8
    Wn = W // 8
    for h in range(Hn):
        for w in range(Wn):
            dct_block = block_dct[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)]
            img_block = cv2.idct(dct_block)
            recover_image[8 * h: 8 * (h + 1), 8 * w: 8 * (w + 1)] = img_block
    return recover_image

























if __name__ == '__main__':
    data=read_bin_data("zip/compressedData.bin")
    cover_spa=read_jpeg(r"E:\coding\python\pytorch\cover65_2.png")
    dct_coff=block_dct(cover_spa)
    ori_dct=dct_coff.copy()
    stego_dct=Qim_embed(dct_coff,data)
    stego_image=get_stego(stego_dct)
    cv2.imwrite("stego_65_2.png",stego_image)
    stego_spa = read_jpeg("stego_65_2.png")
    stego_dct = block_dct(stego_spa)
    recover_data=Qim_extract(stego_dct,len(data))
    ori_data=np.array([int(i) for i in data])
    recover_data=np.array([int(i) for i in recover_data])
    error = np.abs(ori_data - recover_data)
    error_rate = np.mean(error)
    print(error_rate)









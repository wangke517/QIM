from PIL import Image
import os
import cv2
def compress(image_path,Q):
    """
    对指定图片进行JPEG压缩
    :param image_path: 需要压缩的文件路径
    :param Q: 压缩的质量因子，越大代表压缩程度越小
    :return:
    """
    image=cv2.imread(image_path)
    out_filename="./pic/"+os.path.basename(image_path).split(".")[0]+"compress"+str(Q)+".jpg"
    cv2.imwrite(out_filename,image,[cv2.IMWRITE_JPEG_QUALITY, Q])


def rotate(image_path,angle,Q=95,filetype="jpg"):
    """
    任意角度旋转图片,逆时针旋转
    :param image_path: 图片路径
    :param angle: 旋转角度
    :return:
    """
    image = cv2.imread(image_path)
    if(filetype=="jpg"):
        out_filename = "./pic/"+os.path.basename(image_path).split(".")[0] +"rotate"+ str(angle) + ".jpg"
    else:
        out_filename = "./pic/"+os.path.basename(image_path).split(".")[0] + "rotate" + str(angle) + ".png"
    rows, cols, channel = image.shape

    # 绕图像的中心旋转
    # 参数：旋转中心 旋转度数 scale
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)

    # 参数：原始图像 旋转参数 元素图像宽高
    rotated = cv2.warpAffine(image, M, (cols, rows))
    if(filetype=="jpg"):
        cv2.imwrite(out_filename,rotated,[cv2.IMWRITE_JPEG_QUALITY, Q])
    else:
        cv2.imwrite(out_filename,rotated)

def resize(image_path,size,Q=95,filetype="jpg"):
    """
    根据size修改图片大小
    :param image_path:图片路径
    :param size: 需要修改的大小，格式为一个元组(W,H)
    :return:
    """
    image = cv2.imread(image_path)
    if(filetype=="jpg"):
        out_filename = "./pic/"+os.path.basename(image_path).split(".")[0] + "resize" + str(size) + ".jpg"
    else:
        out_filename = "./pic/"+os.path.basename(image_path).split(".")[0] + "resize" + str(size) + ".png"
    image=cv2.resize(image,size,interpolation=cv2.INTER_CUBIC)
    if (filetype == "jpg"):
        cv2.imwrite(out_filename,image,[cv2.IMWRITE_JPEG_QUALITY, Q])
    else:
        cv2.imwrite(out_filename,image)

def topng(image_path):
    """
    把图像格式变为PNG
    :param image_path:图片路径
    :return:
    """
    image = Image.open(image_path)
    out_filename = os.path.basename(image_path).split(".")[0] + ".png"
    image.save(out_filename)


if __name__ == '__main__':
    image_path=r"stego_65_2.png"
    # topng(image_path)
    resize(image_path,(800,600),filetype="png")
    # rotate(image_path,90,filetype="png")
    # rotate(r'pic/stego_65_2rotate90.png',-90,filetype="png")
    compress(image_path,55)

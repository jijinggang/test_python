from PIL import Image
import math
import cv2

def image_contrast(img1, img2):
  image1 = Image.open(img1)
  image2 = Image.open(img2)
  
  h1 = image1.histogram()
  h2 = image2.histogram()
  sum = 0
  print(len(h1),len(h2))
  for i in range(len(h1)):
    sum += (h1[i]-h2[i])**2
  return math.sqrt(sum/len(h1))





# 差异值哈希算法
def dhash(image):
    # 将图片转化为8*8
    image = cv2.resize(image, (9, 8), interpolation=cv2.INTER_CUBIC)
    # 将图片转化为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dhash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(dhash_str[i: i + 4], 2))
    # print("dhash值",result)
    return result

# 计算两个哈希值之间的差异
def campareHash(hash1, hash2):
    n = 0
    # hash长度不同返回-1,此时不能比较
    if len(hash1) != len(hash2):
        return -1
    # 如果hash长度相同遍历长度
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

def diff_img_hash(img1,img2):
  hash1 = dhash(cv2.imread(img1))
  hash2 = dhash(cv2.imread(img2))
  print(hash1, hash2)
  return campareHash(hash1,hash2)

if __name__ == '__main__':
  import sys
  args = sys.argv
  print(args)
  img1 = args[1] # 指定图片路径
  img2 = args[2]

  result = image_contrast(img1,img2)
  #result = diff_img_hash(img1,img2)
  print(result)
import cv2,math

def image_contrast(img1, img2):
  image1 = cv2.imread(img1)
  image2 = cv2.imread(img2)
  h1 = cv2.calcHist([image1],[0],None,[256],[0,256])
  h2 = cv2.calcHist([image2],[0],None,[256],[0,256])
  print(h1)
  sum = 0
  print(len(h1),len(h2))
  for i in range(len(h1)):
    sum += (h1[i]-h2[i])**2
  return math.sqrt(sum/len(h1))

if __name__ == '__main__':
  import sys
  args = sys.argv
  print(args)
  img1 = args[1] # 指定图片路径
  img2 = args[2]

  result = image_contrast(img1,img2)
  #result = diff_img_hash(img1,img2)
  print(result)
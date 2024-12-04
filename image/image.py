import math
import os.path
from os.path import splitext
import sys
from PIL import Image


# 裁剪空白透明区域
def crop_blank(file):
    with Image.open(file) as img:
        img_cropped = img.crop(img.getbbox())
        img_cropped.save(splitext(file)[0] + "_cropped.png")


# 透明化背景
def transparent_background(file):
    with Image.open(file) as img:
        img = img.convert("RGBA")
        data = img.getdata()
        newData = []
        (r, g, b) = img.getpixel((0, 0))
        for item in data:
            if item[0] == r and item[1] == g and item[2] == b:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(splitext(file)[0] + "_transparent.png")


# 合并图片
def merge_image(files, output, COLS, ROWS, scale=1.0):
    # COLS = int(input("请输入合并列数："))
    # ROWS = int(input("请输入合并行数："))
    images = [Image.open(file) for file in files]
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    max_height = max(heights)
    new_img = Image.new('RGB', (max_width * COLS, max_height * ROWS))
    index = 0
    for j in range(ROWS):
        for i in range(COLS):
            if index >= len(images):
                break
            img = images[index]
            new_img.paste(img, (i * max_width, j * max_height))
            index += 1
    new_img = new_img.resize((int(new_img.size[0] * scale), int(new_img.size[1] * scale)))
    new_img.save(output)


# 切分图片
# reverse 逆序切分
def split_image(file, reverse=False):
    COLS = int(input("请输入切分列数："))
    ROWS = int(input("请输入切分行数："))
    results = []
    with Image.open(file) as img:
        width, height = img.size
        min_bbox = None

        for j in range(ROWS):
            for i in range(COLS):
                img_split = img.crop(
                    (i * width // COLS, j * height // ROWS, (i + 1) * width // COLS, (j + 1) * height // ROWS))
                if bbox := img_split.getbbox():
                    if min_bbox is None:
                        min_bbox = bbox
                    else:
                        min_bbox = [min(min_bbox[0], bbox[0]), min(min_bbox[1], bbox[1]), max(min_bbox[2], bbox[2]), max(min_bbox[3], bbox[3])]
                    # img_split = img_split.transpose(Image.FLIP_LEFT_RIGHT) #镜像
                    if reverse:
                        results.insert(0, img_split)
                    else:
                        results.append(img_split)

    # 写文件
    # 创建子目录
    if not os.path.exists(splitext(file)[0]):
        os.makedirs(splitext(file)[0])
    index = 0
    for img in results:
        if min_bbox is not None:
            img = img.crop(min_bbox)
        img.save(splitext(file)[0] + "/" + f"{index}".zfill(2) +".png")
        index = index + 1

    # 循环显示图片
    for img in results:
        img.show()





    # 打开文件夹
    os.system(f"start explorer {splitext(file)[0]}")


# 把git每一帧存为图片
def _gif_to_images(file,MAX_FRAME=16):
    import imageio
    images = imageio.mimread(file)
    image_path = file.split(".")[0]
    # 减少帧数，大致在9~16帧
    images = images[::math.ceil(len(images) / MAX_FRAME)]
    for i, image in enumerate(images):
        imageio.imwrite(splitext(file)[0] + f"_frame_{i}.png", image)

    # 合并图片
    files = [splitext(file)[0] + f"_frame_{i}.png" for i in range(len(images))]
    COLS = math.ceil(math.sqrt(len(images)))
    ROWS = math.ceil(len(images) / COLS)
    merge_image(files, splitext(file)[0] + "_merged.png", COLS, ROWS, 0.5)
    for f in files:
        os.remove(f)
    # 显示图像
    with Image.open(splitext(file)[0] + "_merged.png") as img:
        img.show()

# 把mp4存成图片
def _mp4_to_images(file, MAX_FRAME=16):
    import cv2
    cap = cv2.VideoCapture(file)
    image_path = file.split(".")[0]
    frame_count = 0
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        frame_count += 1
    frames = frames[::math.ceil(len(frames) / MAX_FRAME)]
    for frame_count, frame in enumerate(frames):
        cv2.imwrite(splitext(file)[0] + f"_frame_{frame_count}.png", frame)
    cap.release()

    # 合并图片
    files = [splitext(file)[0] + f"_frame_{i}.png" for i in range(frame_count)]
    COLS = math.ceil(math.sqrt(frame_count))
    ROWS = math.ceil(frame_count / COLS)
    merge_image(files, splitext(file)[0] + "_merged.png", COLS, ROWS, 0.5)
    for f in files:
        os.remove(f)
    # 显示图像
    with Image.open(splitext(file)[0] + "_merged.png") as img:
        img.show()

def video_to_images(file):
    if file.endswith(".gif"):
        _gif_to_images(file)
    elif file.endswith(".mp4"):
        _mp4_to_images(file)

def main():
    if len(sys.argv) < 2 or (not os.path.isfile(sys.argv[1])):
        print("Usage: python image.py <file>")
        sys.exit(1)

    # 显示处理选项
    process = [("裁剪空白区域", crop_blank), ("切分图片", split_image),
               ("mp4/gif等视频转图片集", video_to_images), ("透明化背景", transparent_background)]
    for i, (name, _) in enumerate(process):
        print(f"{i + 1}. {name}")
    choice = 0
    while True:
        choice = input("请选择操作：")
        if not (choice.isdigit() and int(choice) in range(1, len(process) + 1)):
            print("无效的选择")
        else:
            break
    print(f"你选择了 {process[int(choice) - 1][0]}")
    process[int(choice) - 1][1](sys.argv[1])
    print("处理完成")


if __name__ == "__main__":
    main()

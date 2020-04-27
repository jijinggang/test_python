from PIL import Image


def noise_remove_pil(image_name, k):
    """
    8邻域降噪
    Args:
        image_name: 图片文件命名
        k: 判断阈值

    Returns:

    """
    def calculate_noise_count(img_obj, w, h):
        """
        计算邻域非白色的个数
        Args:
            img_obj: img obj
            w: width
            h: height
        Returns:
            count (int)
        """
        count = 0
        width, height = img_obj.size
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                color = img_obj.getpixel((_w_, _h_))
                if color < 230:  # 这里因为是灰度图像，设置小于230为非白色
                    count += 1

        return count

    img = Image.open(image_name)
    # 灰度
    gray_img = img.convert('L')

    w, h = gray_img.size
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img.putpixel((_w, _h), 255)
                continue
            # 计算邻域非白色的个数
            pixel = gray_img.getpixel((_w, _h))
            if pixel == 255:
                continue
            count = calculate_noise_count(gray_img, _w, _h)
            if count < k:
                gray_img.putpixel((_w, _h), 255)
            elif count > 6:
                gray_img.putpixel((_w, _h), pixel-5*(count-5))
    return gray_img


if __name__ == '__main__':
    image = noise_remove_pil("d:/1.jpg", 2)
    image.save("d:/result.jpg")
    image.show()

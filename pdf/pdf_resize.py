import re
import io
# pip install PyPDF4
import PyPDF4 as pdf

# pip install Pillow
from PIL import Image
from PyPDF4.pdf import Destination
from PyPDF4.generic import TextStringObject, NumberObject


def show_bookmarks(outlines, indent=0):
    for item in outlines:
        if isinstance(item, list):
            # recursive call with increased indentation
            show_bookmarks(item, indent + 4)
        else:
            print(" " * indent + item.title)


def _gen_bookmarks(r: pdf.PdfFileReader, w: pdf.PdfFileWriter, outlines, parent=None):
    curr_parent = parent
    for item in outlines:
        if isinstance(item, list):
            # recursive call with increased indentation
            _gen_bookmarks(r, w, item, curr_parent)
            pass
        else:
            curr_parent = w.addBookmark(
                item.title, r.getDestinationPageNumber(item), parent)


def copy_bookmarks(r: pdf.PdfFileReader, w: pdf.PdfFileWriter):
    outlines = r.outlines
    _gen_bookmarks(r, w, outlines)


def dealImg(imgData, sizeNew):
    with Image.open(io.BytesIO(imgData)) as img:
        # img.save("1.jpg")
        if TO_GRAY:
            img = img.convert("L")

        # 处理图片
        size = img.size
        img = img.resize(sizeNew)

        stream = io.BytesIO()
        # 将图片保存到stream中
        # 注意，保存的格式要和pdf中原图片的格式保持一致
        img.save(stream, 'jpeg')
        return stream.getvalue()


def dealImgObj(imgObj, obj):

    size = (imgObj['/Width'], imgObj['/Height'])
    sizeNew = (int(size[0]*RESIZE_RATE), int(size[1]*RESIZE_RATE))
    data = imgObj.getData()
    data = dealImg(data, sizeNew)
    # print(len(data))

    imgObj._data = data
    imgObj[TextStringObject('/Width')] = NumberObject(sizeNew[0])
    imgObj[TextStringObject('/Height')] = NumberObject(sizeNew[1])


def dealPage(page):

    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                dealImgObj(xObject[obj], obj)

    else:
        pass
    return page


def main(pdf_file, output=None):

    r = pdf.PdfFileReader(pdf_file)
    w = pdf.PdfFileWriter()
    index = 0
    totals = r.getNumPages()
    for page in r.pages:
        index += 1
        print(f"page:{index} / {totals}")
        w.addPage(dealPage(page))
        #newPage = w.addBlankPage()

    copy_bookmarks(r, w)

    if(output == None):
        output = pdf_file
    with open(output, 'wb') as outputf:
        w.write(outputf)


RESIZE_RATE = 0.5  # 图片缩小比率
TO_GRAY = True  # 是否转灰度
main("E:/book/技术/new/NET CLR via C#(第4版).pdf", "d:/1.pdf")
#main("d:/1.pdf", "d:/2.pdf")

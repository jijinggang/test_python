import re
import io
# pip install PyPDF4
import PyPDF4 as pdf


def readtoc(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        regex = re.compile(r"^([\S| ]*[^.])...[\.]+(\d+)$", re.MULTILINE)
        return regex.findall(text)


def main(pdf_file, toc_file, toc_offset, output=None):
    w = pdf.PdfFileWriter()
    r = pdf.PdfFileReader(pdf_file)
    for page in r.pages:
        # deal_page(page)
        w.addPage(page)
    tocs = readtoc(toc_file)
    for toc in tocs:
        w.addBookmark(toc[0], int(toc[1]) + toc_offset)
    if(output == None):
        output = pdf_file

    with open(output, 'wb') as out:
        w.write(out)


main("E:/book/技术/new/CLR+via+C#++第4版.pdf", "./pdf/toc.txt", 15)

import pdfplumber
import testDimension
def read_pdf_content(file_path: str) -> str:
    """
    读取PDF文件的内容并返回文本。

    :param file_path: PDF文件的路径
    :return: PDF文件的文本内容
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

a = read_pdf_content("./resume/Web前端开发工程师-稻小壳.pdf")
# print(a)
# testDimension.getMatchScore(a)
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import shutil
import uvicorn
import resumeCore
import testDimension

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
def read_root():
    content = resumeCore.read_pdf_content("./resume/Web前端开发工程师-稻小壳.pdf")
    testDimension.getMatchScore(content)
    return {"message": "Welcome to the FastAPI demo!"}

@app.post("/items/")
def create_item(item: Item):
    return item

# 接收POST请求，支持文件上传。
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # 创建一个临时文件，用于保存上传的文件内容。
    with open("temp.txt", "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)

    # 读取临时文件的内容，并返回给客户端。
    with open("temp.txt", "rb") as temp_file:
        content = temp_file.read()
        return {"content": content}

@app.post("/resumeFilter/")
async def resumeFilter():
    content = resumeCore.read_pdf_content("./resume/Web前端开发工程师-稻小壳.pdf")
    score = testDimension.getMatchScore(content)  
    print("score:::",score)
    return  "简历匹配程度为：" + score

    
if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, workers=3,reload=True)


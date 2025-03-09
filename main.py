from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, validator
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uvicorn
import resumeCore
import testDimension
import sqlite3
from db import init_db
import secrets
from datetime import datetime, timedelta
from cachetools import TTLCache

app = FastAPI()

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源访问，生产环境建议设置具体的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 数据库连接对象
db_connection = None

# 创建一个TTL缓存，设置过期时间为5分钟
token_cache = TTLCache(maxsize=100, ttl=300)  # 300秒 = 5分钟

@app.on_event("startup")
async def startup_event():
    """在应用启动时初始化数据库连接
    
    该事件处理器在FastAPI应用启动时被调用，负责初始化全局数据库连接对象。
    通过调用init_db()函数创建并初始化SQLite数据库连接。
    
    Returns:
        None
    """
    global db_connection
    db_connection = init_db()

@app.on_event("shutdown")
async def shutdown_event():
    """在应用关闭时关闭数据库连接
    
    该事件处理器在FastAPI应用关闭时被调用，负责安全关闭数据库连接。
    如果存在活动的数据库连接，将其关闭并打印确认消息。
    
    Returns:
        None
    """
    global db_connection
    if db_connection:
        db_connection.close()
        print("数据库连接已关闭！")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class LoginRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    password: str

    @validator('email', 'phone')
    def validate_login_fields(cls, v, values):
        # 检查email和phone字段
        if 'email' in values and values['email'] is None and 'phone' in values and values['phone'] is None:
            raise ValueError('邮箱或电话号码必须至少提供一个')
        return v

@app.get("/")
def read_root():
    """根路径的GET请求处理器
    
    读取示例PDF简历文件的内容并进行评分测试。
    
    Returns:
        dict: 包含欢迎消息的字典
    """
    content = resumeCore.read_pdf_content("./resume/Web前端开发工程师-稻小壳.pdf")
    testDimension.getMatchScore(content)
    return {"message": "Welcome to the FastAPI demo!"}

@app.post("/items/")
def create_item(item: Item):
    """创建新的商品项目
    
    Args:
        item (Item): 包含商品信息的Item模型实例
    
    Returns:
        Item: 创建的商品项目
    """
    return item

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """处理文件上传
    
    接收上传的文件，将其保存为临时文件并返回文件内容。
    
    Args:
        file (UploadFile): 上传的文件对象
    
    Returns:
        dict: 包含文件内容的字典
    """
    # 创建一个临时文件，用于保存上传的文件内容。
    with open("temp.txt", "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)

    # 读取临时文件的内容，并返回给客户端。
    with open("temp.txt", "rb") as temp_file:
        content = temp_file.read()
        return {"content": content}

@app.post("/resumeFilter/")
async def resumeFilter():
    """简历过滤评分接口
    
    读取指定PDF简历文件，计算匹配分数并返回评估结果。
    
    Returns:
        str: 简历匹配程度的评分结果
    """
    content = resumeCore.read_pdf_content("./resume/Web前端开发工程师-稻小壳.pdf")
    score = testDimension.getMatchScore(content)  
    print("score:::",score)
    print("SQLite 版本：", sqlite3.sqlite_version)  # 输出当前版本
    return  "简历匹配程度为：" + score

class ResumeSearchRequest(BaseModel):
    file_name: str | None = None
    candidate_name: str | None = None
    phone: str | None = None
    email: str | None = None

@app.post("/resumes/search/")
async def search_resumes(search_request: ResumeSearchRequest):
    """搜索简历列表接口
    
    支持通过简历名称、候选人姓名、手机号和邮箱进行模糊查询。
    所有查询参数都是可选的，可以单独使用或组合使用。
    
    Args:
        search_request: 包含搜索条件的请求体
    
    Returns:
        dict: 包含查询结果的字典
    """
    from resumeFileUtildb import search_resume_files
    
    # 调用数据库查询函数
    results = search_resume_files(
        db_connection,
        file_name=search_request.file_name,
        candidateName=search_request.candidate_name,
        phone=search_request.phone,
        email=search_request.email
    )
    
    # 将查询结果转换为字典列表
    resumes = [{
        "id": row[0],
        "file_name": row[1],
        "file_path": row[2],
        "file_size": row[3],
        "upload_time": row[4],
        "last_modified": row[5],
        "file_type": row[6],
        "user_id": row[7],
        "candidateName": row[8],
        "phone": row[9],
        "email": row[10],
        "status": row[11],
        "aiScore": row[12]
    } for row in results]
    
    return {"resumes": resumes}

@app.post("/login/")
async def login(login_request: LoginRequest):
    """用户登录接口
    
    处理用户登录请求，验证用户信息并返回登录结果。
    支持使用邮箱或电话号码进行登录。
    
    Args:
        login_request (LoginRequest): 包含登录信息的请求模型
    
    Returns:
        dict: 登录结果，包含状态、消息和用户信息
    """
    cursor = db_connection.cursor()
    
    # 构建查询条件
    query_conditions = []
    query_params = []
    
    if login_request.email:
        query_conditions.append('email = ?')
        query_params.append(login_request.email)
    if login_request.phone:
        query_conditions.append('phone = ?')
        query_params.append(login_request.phone)
    
    if not query_conditions:
        raise HTTPException(status_code=400, detail="必须提供邮箱或电话号码")
    
    query = f"SELECT * FROM users WHERE {' OR '.join(query_conditions)}"
    cursor.execute(query, query_params)
    user = cursor.fetchone()
    
    if user:
        # 验证密码是否匹配
        if user[3] != login_request.password:  # 数据库中密码存储在第4列
            return {
                "status": "error",
                "message": "密码错误"
            }
        # 生成token
        token = secrets.token_hex(32)
        # 将token和用户信息存储在缓存中
        token_cache[token] = {
            "user_id": user[0],
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "message": "登录成功",
            "token": token,
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "phone": user[3],
                "skills": user[4],
                "work_experience": user[5],
                "education": user[6]
            }
        }
    else:
        return {
            "status": "error",
            "message": "用户不存在"
        }

if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, workers=3,reload=True)


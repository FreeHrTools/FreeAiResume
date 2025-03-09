import os
from resumeFileUtildb import init_resume_file_db, add_resume_file

def init_resume_data():
    # 初始化数据库连接
    conn = init_resume_file_db()
    
    # 简历数据
    resumes = [
        {
            'id': 1,
            'name': '前端开发工程师简历.pdf',
            'candidateName': '张三',
            'phone': '13800138000',
            'email': 'zhangsan@example.com',
            'uploadTime': '2024-01-15 10:30:00',
            'status': '通过筛选',
            'aiScore': 85
        },
        {
            'id': 2,
            'name': '后端开发工程师简历.pdf',
            'candidateName': '李四',
            'phone': '13900139000',
            'email': 'lisi@example.com',
            'uploadTime': '2024-01-15 11:20:00',
            'status': '未通过筛选',
            'aiScore': 45
        },
        {
            'id': 3,
            'name': '产品经理简历.pdf',
            'candidateName': '王五',
            'phone': '13700137000',
            'email': 'wangwu@example.com',
            'uploadTime': '2024-01-15 14:15:00',
            'status': '待处理',
            'aiScore': 75
        },
        {
            'id': 4,
            'name': 'UI设计师简历.pdf',
            'candidateName': '赵六',
            'phone': '13600136000',
            'email': 'zhaoliu@example.com',
            'uploadTime': '2024-01-16 09:30:00',
            'status': '通过筛选',
            'aiScore': 88
        },
        {
            'id': 5,
            'name': '运维工程师简历.pdf',
            'candidateName': '钱七',
            'phone': '13500135000',
            'email': 'qianqi@example.com',
            'uploadTime': '2024-01-16 11:45:00',
            'status': '待处理',
            'aiScore': 72
        },
        {
            'id': 6,
            'name': '数据分析师简历.pdf',
            'candidateName': '孙八',
            'phone': '13400134000',
            'email': 'sunba@example.com',
            'uploadTime': '2024-01-16 14:20:00',
            'status': '未通过筛选',
            'aiScore': 55
        },
        {
            'id': 7,
            'name': '测试工程师简历.pdf',
            'candidateName': '周九',
            'phone': '13300133000',
            'email': 'zhoujiu@example.com',
            'uploadTime': '2024-01-17 10:15:00',
            'status': '通过筛选',
            'aiScore': 82
        },
        {
            'id': 8,
            'name': '算法工程师简历.pdf',
            'candidateName': '吴十',
            'phone': '13200132000',
            'email': 'wushi@example.com',
            'uploadTime': '2024-01-17 15:40:00',
            'status': '待处理',
            'aiScore': 78
        }
    ]
    
    # 为每个简历创建文件路径和设置文件大小
    resume_dir = os.path.join(os.path.dirname(__file__), 'resume_files')
    os.makedirs(resume_dir, exist_ok=True)
    
    for resume in resumes:
        # 生成文件路径
        file_path = os.path.join(resume_dir, resume['name'])
        # 模拟文件大小（500KB到2MB之间）
        file_size = 512 * 1024 + (resume['id'] * 100 * 1024)
        
        # 添加简历记录
        result = add_resume_file(
            conn,
            file_name=resume['name'],
            file_path=file_path,
            file_size=file_size,
            file_type='application/pdf',
            candidateName=resume['candidateName'],
            phone=resume['phone'],
            email=resume['email'],
            status=resume['status'],
            aiScore=resume['aiScore']
        )
        
        if result:
            print(f"成功添加简历记录：{resume['name']}")
        else:
            print(f"添加简历记录失败：{resume['name']}")
    
    # 关闭数据库连接
    conn.close()
    print("所有简历数据初始化完成！")

if __name__ == '__main__':
    init_resume_data()
import axios from 'axios'

// 创建axios实例
const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
instance.interceptors.request.use(
    config => {
        // 从sessionStorage获取token
        const token = sessionStorage.getItem('token')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
instance.interceptors.response.use(
    response => {
        return response.data
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 未授权，清除token并跳转到登录页面
                    sessionStorage.removeItem('token')
                    window.location.href = '/login'
                    break
                case 403:
                    ElMessage.error('没有权限访问该资源')
                    break
                case 404:
                    ElMessage.error('请求的资源不存在')
                    break
                case 500:
                    ElMessage.error('服务器错误')
                    break
                default:
                    ElMessage.error(error.response.data.message || '请求失败')
            }
        } else if (error.request) {
            ElMessage.error('网络错误，请检查您的网络连接')
        } else {
            ElMessage.error('请求配置错误')
        }
        return Promise.reject(error)
    }
)

// 封装GET请求
export const get = (url, params) => {
    return instance.get(url, { params })
}

// 封装POST请求
export const post = (url, data) => {
    return instance.post(url, data)
}

// 封装PUT请求
export const put = (url, data) => {
    return instance.put(url, data)
}

// 封装DELETE请求
export const del = (url) => {
    return instance.delete(url)
}

// 导出axios实例
export default instance
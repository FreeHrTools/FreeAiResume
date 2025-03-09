<template>
    <div class="login-container">
        <el-card class="login-card">
            <template #header>
                <h2>登录</h2>
            </template>
            <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="120px">
                <el-form-item label="邮箱/手机号" prop="username">
                    <el-input v-model="loginForm.email" placeholder="请输入邮箱或手机号" :prefix-icon="User" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" :prefix-icon="Lock"
                        show-password />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { post } from '../utils/apiUtils'

const router = useRouter()
const loginFormRef = ref(null)

const loginForm = reactive({
    email: '',
    password: ''
})

const rules = {
    email: [{ required: true, message: '请输入邮箱或手机号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = () => {
    loginFormRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const response = await post('http://127.0.0.1:8080/login', {
                    email: loginForm.email,
                    password: loginForm.password
                })
                if (response.token) {
                    sessionStorage.setItem('token', response.token)
                    sessionStorage.setItem('isAuthenticated', 'true')
                    ElMessage.success('登录成功')
                    router.push('/upload')
                } else {
                    ElMessage.error('登录失败：' + (response.message || '未知错误'))
                }
            } catch (error) {
                ElMessage.error('登录失败：' + (error.message || '网络错误'))
            }
        }
    })
}
</script>

<style scoped>
.login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
}

.login-card {
    width: 400px;
}

.el-card :deep(.el-card__header) {
    text-align: center;
}
</style>
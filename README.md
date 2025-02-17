# verification-code-ocr-service

验证码识别服务，支持URL和Base64格式的图片输入。

## 部署方式

### 方式一：Docker部署（推荐）

1. 克隆项目并进入项目目录
   ```bash
   git clone <repository_url>
   cd verification-code-ocr-service
   ```

2. 创建验证码图片存储目录
   ```bash
   mkdir -p captcha
   ```

3. 使用Docker Compose启动服务
   ```bash
   docker-compose up -d
   ```

4. 查看服务状态
   ```bash
   docker-compose ps
   ```

### 方式二：直接运行

1. 安装必要的包：
   ```bash
   pip install -r requirements.txt
   ```

2. 创建验证码图片存储目录：
   ```bash
   mkdir -p captcha
   ```

3. 运行服务：
   ```bash
   python main.py
   ```

## API 使用说明

### 接口信息
- 接口地址：http://localhost:8000/ocr/
- 请求方法：POST
- 请求体格式：
  ```json
  {
      "url": "验证码图片的URL或base64字符串"
  }
  ```

### 示例请求
```bash
# URL方式
curl -X POST "http://localhost:8000/ocr/" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://example.com/captcha.jpg"}'

# Base64方式
curl -X POST "http://localhost:8000/ocr/" \
  -H "Content-Type: application/json" \
  -d '{"url":"data:image/png;base64,iVBOR..."}'
```

### 返回格式
```json
{
    "code": 0,        // 0表示成功，400表示请求失败，500表示处理失败
    "msg": "success", // 成功或错误信息
    "data": "1234"    // 识别出的验证码，失败时为null
}
```

## 特性
- 支持URL和Base64格式的图片输入
- 自动将验证码图片转换为白底图片
- 自动将图片转换为JPG格式存储
- 所有处理过的验证码图片保存在 captcha 目录
- 详细的请求处理日志

## 注意事项
1. 确保 captcha 目录有写入权限
2. 服务默认运行在 8000 端口
3. 建议使用 Docker 方式部署，可以避免环境问题
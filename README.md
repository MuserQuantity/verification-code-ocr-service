# verification-code-ocr-service

使用说明：
1. 首先需要安装必要的包：
   pip install fastapi uvicorn ddddocr requests

2. 将代码保存为 app.py 并运行：
   python app.py

3. API 使用方法：
   - 接口地址：http://localhost:8000/ocr/
   - 请求方法：POST
   - 请求体格式：
     ```json
     {
         "url": "验证码图片的URL或base64字符串"
     }
     ```
   
4. 示例请求：
   ```bash
   # URL方式
   curl -X POST "http://localhost:8000/ocr/" -H "Content-Type: application/json" -d '{"url":"http://example.com/captcha.jpg"}'
   
   # Base64方式
   curl -X POST "http://localhost:8000/ocr/" -H "Content-Type: application/json" -d '{"url":"data:image/png;base64,iVBOR..."}'
   ```

5. 返回格式：
   {
       "code": "识别出的验证码",
       "msg": "success",
       "data": "识别出的验证码"
   }
   其中code为0表示成功，400表示请求失败，500表示处理失败。
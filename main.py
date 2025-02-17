from fastapi import FastAPI, HTTPException
import ddddocr
import requests
from io import BytesIO
import base64
from pydantic import BaseModel
import uvicorn
import logging
from datetime import datetime
from PIL import Image
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 实例
app = FastAPI()

# 创建请求模型
class ImageData(BaseModel):
    url: str

# 初始化 ddddocr
ocr = ddddocr.DdddOcr(beta=True)

def convert_to_white_background(image):
    """将图片背景转为白色"""
    # 转换为RGBA模式以处理透明度
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 转换为numpy数组
    data = np.array(image)
    
    # 创建一个白色背景
    white_background = np.ones_like(data) * 255
    
    # 根据alpha通道混合前景和背景
    alpha = data[:, :, 3] / 255.0
    for i in range(3):
        white_background[:, :, i] = data[:, :, i] * alpha + white_background[:, :, i] * (1 - alpha)
    
    # 转回PIL图像并转为RGB模式
    result = Image.fromarray(white_background.astype('uint8')).convert('RGB')
    return result

@app.post("/ocr/")
async def read_verification_code(image_data: ImageData):
    request_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    logger.info(f"Request {request_id} - 收到验证码识别请求")
    
    try:
        # 获取图片数据
        if image_data.url.startswith('http'):
            logger.info(f"Request {request_id} - 通过URL获取图片")
            response = requests.get(image_data.url)
            response.raise_for_status()
            image_bytes = response.content
            # 打开图片
            image = Image.open(BytesIO(image_bytes))
        else:
            logger.info(f"Request {request_id} - 接收到base64图片数据")
            # 如果base64字符串包含前缀，需要去掉前缀
            if ',' in image_data.url:
                base64_data = image_data.url.split(',')[1]
            else:
                base64_data = image_data.url
            image_bytes = base64.b64decode(base64_data)
            # 打开图片
            image = Image.open(BytesIO(image_bytes))
        
        # 转换为白底
        logger.info(f"Request {request_id} - 转换图片背景为白色")
        image = convert_to_white_background(image)
        
        # 保存为JPG
        jpg_path = f"./captcha/captcha_{request_id}.jpg"
        image.save(jpg_path, 'JPEG', quality=95)
        # 重新读取图片
        image_bytes = open(jpg_path, "rb").read()
        
        # 识别验证码
        logger.info(f"Request {request_id} - 开始识别验证码")
        result = ocr.classification(image_bytes, png_fix=True)
        logger.info(f"Request {request_id} - 验证码识别成功: {result}")
        
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error downloading image: {str(e)}"
        logger.error(f"Request {request_id} - {error_msg}")
        return {
            "code": 400,
            "msg": error_msg,
            "data": None
        }
    except base64.binascii.Error as e:
        error_msg = f"Invalid base64 data: {str(e)}"
        logger.error(f"Request {request_id} - {error_msg}")
        return {
            "code": 400,
            "msg": error_msg,
            "data": None
        }
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        logger.error(f"Request {request_id} - {error_msg}")
        return {
            "code": 500,
            "msg": error_msg,
            "data": None
        }

@app.get("/")
async def root():
    logger.info("收到健康检查请求")
    return {
        "code": 0,
        "msg": "Verification Code OCR API",
        "data": None
    }

if __name__ == "__main__":
    logger.info("验证码识别服务启动")
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
使用说明：
1. 首先需要安装必要的包：
   pip install fastapi uvicorn ddddocr requests

2. 将代码保存为 app.py 并运行：
   python app.py

3. API 使用方法：
   - 接口地址：http://localhost:8000/ocr/
   - 请求方法：POST
   - 请求体格式：
     {
         "url": "验证码图片的URL或base64编码"
     }
   
4. 示例请求：
   curl -X POST "http://localhost:8000/ocr/" -H "Content-Type: application/json" -d '{"url":"http://example.com/captcha.jpg"}'

5. 返回格式：
   {
       "code": 0,
       "msg": "success",
       "data": "识别出的验证码"
   }
"""
import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def encode_image(path):
    """
    将图片转换为Base64编码
    :param path:
    :return:
    """
    with open(path, 'rb') as f:  # 按照二进制方式读取文件
        return base64.b64encode(f.read()).decode('utf-8')


# 采用发送http请求的方式来调用 openai的接口。
def import_image(img_path, user_prompt='请介绍一些图片的内容', max_token=1000):
    """
    把本地的图片数据作为大语言模型的输入，
    本地的图片：必须要把图片转换为 Base64的编码格式
    :param img_path: 图片本地路径
    :param user_prompt: 用户对图片的要求
    :param max_token: 最大token数
    :return:
    """
    base64_img = encode_image(img_path)
    header = {
        'Content-Type': 'application/json',
        'authorization': 'Bearer {}'.format(os.getenv('OPENAI_API_KEY'))
    }
    # 构建请求负载
    payload = {
        'model': 'gpt-4-turbo',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': user_prompt},
                    {'type': 'image_url', 'image_url': {
                        'url': f'data:image/jpeg;base64,{base64_img}'
                    }}
                ]
            }
        ],
        'max_token': max_token
    }

    # 发送请求
    resp = requests.post(os.getenv("BASE_URL"), headers=header, json=payload)
    if resp.status_code == 200:  # 状态码200为成功请求
        resp_data = resp.json()
        content = resp_data['choices'][0]['content']
        print(content)
        return content
    else:
        return f'请求失败，状态码为:{resp.status_code}，失败的信息是：{resp.text}'

print(import_image('../images/painting.jpg'))
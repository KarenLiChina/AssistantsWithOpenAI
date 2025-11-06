from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")  # 指定 base URL
)

# 处理在线图片
resp = client.chat.completions.create(
    model='gpt-4-turbo',
    messages=[
        {
            'role':'user',
            'content':[
                {'type':'text', 'text':'介绍一下这个图片'},
                {'type':'image_url', 'image_url':{
                    'url':'https://www.keaitupian.cn/cjpic/frombd/2/253/1659552792/3869332496.jpg'
                }}
            ]
        }
    ],
    max_tokens=400
)

print(resp.choices[0].message.content)
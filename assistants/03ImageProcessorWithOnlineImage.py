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
                    'url':'https://cn.bing.com/images/search?view=detailV2&ccid=JMfKpS8A&id=33C1778F53E87FBD0A115E7292FC077F27135537&thid=OIP.JMfKpS8A4mr-Am598t9OiAHaF7&mediaurl=https%3a%2f%2fcdn.pixabay.com%2fphoto%2f2022%2f03%2f10%2f11%2f06%2fpainting-7059647_1280.jpg&cdnurl=https%3a%2f%2fts1.tc.mm.bing.net%2fth%2fid%2fR-C.24c7caa52f00e26afe026e7df2df4e88%3frik%3dN1UTJ38H%252fJJyXg%26pid%3dImgRaw%26r%3d0&exph=1024&expw=1280&q=%e9%a3%8e%e6%99%af%e7%94%bb&FORM=IRPRST&ck=C48ABDCFA88169B51F228CD1C0671795&selectedIndex=0&itb=0&idpp=overlayview&ajaxhist=0&ajaxserp=0'
                }}
            ]
        }
    ],
    max_tokens=400
)

print(resp.choices[0].message.content)
import base64

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")  # 指定 base URL
)

resp = client.images.generate(
    model='dall-e-3',
    prompt='生成一只可爱的四蹄踏雪的黑猫，要求通体全黑，只有四只脚是白色的',
    size='1024x1024',  # 生成图像的尺寸，dall-e-2 必须是256*256，512*512或者是1024*1024，对于dall-e-3模型，必须是1024*1024，1792*1792，1024*1792之一
    quality='standard',  # 清晰度默认是standard标准，还可以是hd 高清
    n=1  # dall-e-3模型只支持 n=1， dall-e-2支持 1-10之间，默认是1
)  # 返回图形的格式必须是 url后者是b64_json之一，默认是url

print(resp)
print(resp.data[0].url)  # 生成图片的url

resp = client.images.generate(
    model='dall-e-3',
    prompt='生成一只可爱的四蹄踏雪的黑猫，通体全黑，在雪地里奔跑，踩出一排小脚印',
    size='1024x1024',  # 生成图像的尺寸，dall-e-2 必须是256*256，512*512或者是1024*1024，对于dall-e-3模型，必须是1024*1024，1792*1792，1024*1792之一
    quality='hd',  # 清晰度默认是standard标准，还可以是hd 高清
    n=1,  # dall-e-3模型只支持 n=1， dall-e-2支持 1-10之间，默认是1
    style='natural',  # 风格为自然，还可以选择vivid，倾向于超现实和戏剧性的图像
    response_format='b64_json'  # 返回图形的格式必须是 url后者是b64_json之一，默认是url
)

print(resp)
b64_img = resp.data[0].b64_json  # 生成图片的b64编码
with open('../images/output_cat.jpg', 'wb') as f:  # 二进制写
    f.write(base64.b64decode(b64_img))

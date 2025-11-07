from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")  # 指定 base URL
)

with client.audio.speech.with_streaming_response.create(
        model='tts-1',  # 模型
        voice='echo',  # 音色 echo回声
        response_format='mp3',  # 输出格式默认为mp3
        speed=1.2,  # 速度1.2
        input='动物界的伪装术，就像是一场奇妙的魔法表演。'
) as resp:  # resp是文件流才可以这样写
    resp.stream_to_file('../audio/test1.mp3')

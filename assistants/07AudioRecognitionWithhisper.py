from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")  # 指定 base URL
)

# 将配音变成文字(语音转录)
audio_file = open('../audio/test.mp3', 'rb')

transcription = client.audio.transcriptions.create(
    model='whisper-1',
    file=audio_file
)
print(transcription.text)

# 转录加翻译(只能翻译成英语)， 用translations
transcription = client.audio.translations.create(
    model='whisper-1',
    file=audio_file,
    prompt='Translate to English'  # 提示不写也会翻译成英文文字
)
english_txt = transcription.text
print(english_txt)

# 给中文音频转换成 英文版
english_audio_file = '../audio/english_test.mp3'
audio_file.close()
with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='onyx',
        input=english_txt
) as resp: resp.stream_to_file(english_audio_file)

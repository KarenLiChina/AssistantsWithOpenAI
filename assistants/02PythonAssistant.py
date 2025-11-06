from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")  # 指定 base URL
)

# 1. 创建assistant
assistant = client.beta.assistants.create(
    name="Python Assistant",  # 助手名字
    instructions="你是一个非常经验丰富的高级python程序员，可以根据给出的问题编写可运行的python代码。",
    tools=[{'type': 'code_interpreter'}],
    # type 有三种类型：code_interpreter 擅长代码、数学等逻辑问题，Retrieval 擅长总结归纳，在输入的内容中检索，Function calling 标准方法输出
    model="gpt-4o"
)

# 2. 创建线程
thread = client.beta.assistants.create()  # 可以理解成为一次会话

# 3. 发送消息
message = client.beta.threads.messages.create(
    thread_id=thread.id,  # 线程id
    role='user',
    content='请帮我写一个快速排序的代码'
)

# 4. 处理相应
# 4.1 处理完成后，再得到所有结果
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='请用“小朋友”的称呼用户'
)

if run.status=='completed':
    #输出最终结果
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print('\n消息：\n')
    for message in messages:
        print(f'Role: {message.role.capitalize()}')
        print(message.content[0].text.value)

message = client.beta.threads.messages.create(
    thread_id=thread.id,  # 线程id
    role='user',
    content='那红黑树呢？'
)
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)
if run.status=='completed':
    #输出最终结果，此时输出会把上一次的问题也输出， thread 会帮助我们存储消息，包括上次的问题和回答
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print('\n消息：\n')
    for message in messages:
        print(f'Role: {message.role.capitalize()}')
        print(message.content[0].text.value)

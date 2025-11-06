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
    name="Math Assistant",  # 助手名字
    instructions="你是一个非常博学的数学老师，非常擅长解决数学问题和数学计算。",
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
    content='请帮我解一个方程：3x+2x+8=9'
)

# 4. 处理相应
# 4.1 处理完成后，再得到所有结果
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='请用“小朋友”的称呼用户'
)

print("run的状态为："+run.status)
if run.status=='completed':
    #输出最终结果
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print('\n消息：\n')
    for message in messages:
        print(f'Role: {message.role.capitalize()}')
        print(message.content[0].text.value)

# 4.2 采用流式方式得到结果：逐个token返回
stream = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions='请用“小朋友”的称呼用户',
    stream=True # 采用流方式得到结果，也可以用create_and_stream 的方式，就不用标准stream=True
)
# 遍历流中的事件

for event in stream:
    # 返回的每个token都是json对象
    print(event.model_dump_json(indent=2, exclude_unset=True))

# 用完之后需要关闭thread和assistant
client.beta.threads.delete(thread_id=thread.id)
client.beta.assistants.delete(assistant_id=assistant.id)

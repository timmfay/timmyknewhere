"""M0 环境自检：确认 Python、依赖和两家大模型的 API 都能用。

运行：python check_setup.py
期望：每家打印一行 OK，并且 reasoning 为空（说明思考模式已经关掉）。
"""
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读取当前文件夹里的 .env，把里面的 key 放进环境变量
print("python", sys.version.split()[0])

PROVIDERS = [
    # (名字, .env 里的变量名, base_url, 模型, 额外参数)
    ("zhipu", "ZHIPUAI_API_KEY", "https://open.bigmodel.cn/api/paas/v4/", "glm-4-flash-250414",
     {"extra_body": {"do_sample": False}}),  # 贪心解码；智谱不要传 temperature=0
    ("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com", "deepseek-v4-pro",
     {"temperature": 0, "extra_body": {"thinking": {"type": "disabled"}}}),  # 必须关掉思考模式
]
QUESTION = "What is 17*23? Answer with the number only."
EXPECTED = "391"

for name, env_var, base_url, model, extra in PROVIDERS:
    key = os.getenv(env_var)

    # TODO 1: key 是 None 或空字符串时，打印「缺少 <env_var>，跳过 <name>」，然后 continue。
    #         提示：None 和 "" 在 if 里都算假，所以一个 `if not key:` 就够了。

    # TODO 2: 只打印 key 的前 4 个字符，后面接 "***"。绝不打印整个 key。
    #         提示：字符串切片 key[:4]

    client = OpenAI(api_key=key, base_url=base_url, timeout=60)
    try:
        resp = client.chat.completions.create(
            model=model,
            max_tokens=50,
            messages=[{"role": "user", "content": QUESTION}],
            **extra,
        )
    except Exception as e:
        print(name, "调用失败：", e)
        continue
    msg = resp.choices[0].message

    # TODO 3: 取出回答 msg.content，去掉首尾空白。等于 EXPECTED 就打印 "<name> OK"，
    #         否则打印 "<name> FAIL" 和回答原文。
    #         提示：msg.content 有可能是 None，可以写 (msg.content or "").strip()

    # TODO 4: 打印三样东西：
    #         - resp.model：服务器实际用的模型名
    #         - resp.usage.total_tokens：这次一共用了多少 token
    #         - reasoning 是否为空：getattr(msg, "reasoning_content", None)
    #           为 None 或空字符串说明思考模式确实关掉了，这是我们要的

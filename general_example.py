import os
import time
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:18000/v1",
    api_key=os.environ["VLLM_API_KEY"],
    timeout=120.0,
)

start = time.perf_counter()

response = client.chat.completions.create(
    model="qwen3.8-27b",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in evolutionary computation. "
                       "Return only executable Python code."
        },
        {
            "role": "user",
            "content": (
                "Implement differential evolution in Python using NumPy. "
                "The function should minimize a user-provided objective."
            ),
        },
    ],
    temperature=0.7,
    max_tokens=1024,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    },
)

elapsed = time.perf_counter() - start

print("=== Generated code ===")
print(response.choices[0].message.content)

print("\n=== Performance ===")
print(f"Elapsed: {elapsed:.2f}s")
usage = response.usage
if usage is not None:
    print(f"Input tokens: {usage.prompt_tokens}")
    print(f"Output tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

    if usage.completion_tokens and elapsed > 0:
        print(
            f"End-to-end throughput: "
            f"{usage.completion_tokens / elapsed:.2f} tokens/s"
        )
else:
    print("Token usage unavailable: server did not return usage data.")

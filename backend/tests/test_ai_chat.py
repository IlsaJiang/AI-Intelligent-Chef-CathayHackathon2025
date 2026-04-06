import dashscope

dashscope.api_key = "sk-058cf7fbf53644ffa0939e6edb4715fe"

resp = dashscope.Generation.call(
    model="qwen-plus",
    prompt="請用繁體中文介紹宮保雞丁的由來。"
)

print("=== 原始返回 ===")
print(resp)

# ✅ 新版取值方式
try:
    if hasattr(resp, "output") and "text" in resp.output:
        print("\n=== 模型輸出 ===")
        print(resp.output["text"])
    elif hasattr(resp, "output") and "choices" in resp.output:
        print("\n=== 模型輸出 ===")
        print(resp.output["choices"][0]["message"]["content"])
    else:
        print("\n⚠️ 未找到文本輸出欄位，原始返回結構為：")
        print(resp)
except Exception as e:
    print("❌ 出錯：", e)


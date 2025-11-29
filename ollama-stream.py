from ollama import chat

# --- helper ---
def add_msg(history, role_code, text):
    # 定義代碼對照表
    role_map = {
        'SYS': 'system',    # SYS 代表 system
        'USER': 'user',      # USER 代表 user
        'AI': 'assistant'  # AI 代表 assistant
    }
    
    # 這裡會自動把 S/U/A 換成完整單字，如果打錯就預設用 user
    full_role = role_map.get(role_code, 'user')
    
    history.append({
        'role': full_role,
        'content': text
    })

# --- 主程式開始 ---
memories = []

# 1. 【重點】一開始先設定 System (用簡短的 'SYS')
# 這一行只會執行一次，設定 AI 的人設
add_msg(memories, 'SYS', '你是一個極簡主義助手，所有回答請務必控制在30字以內。')

while True:
    user_input = input("請輸入中文 (輸入 /bye 離開)：")
    if user_input == "/bye": break

    # 2. 存使用者的話 (用 'U')
    add_msg(memories, 'USER', user_input)

    # 呼叫模型
    response = chat(model='gemma3:12b', messages=memories)
    answer = response.message.content
    print("翻譯結果：", answer)

    # 3. 存 AI 的話 (用 'A')
    add_msg(memories, 'AI', answer)
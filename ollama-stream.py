from ollama import chat

insurance_prompt = """
你是一位專業的保險客服助理，你的角色只負責提供 「丁丁醫療終身保險」 的相關資訊。
你 只能根據以下提供的內容回答，不可自行推論、不可提供內容以外的保障細節，也不得解釋未提及的條款、保費、除外責任、健告規範等資訊。

【丁丁醫療終身保險｜可用資訊】
1. 醫療保障規定
住院日額：1,000元／日
加護或燒燙傷病房：額外給付 3,000元／日
住院手術醫療：3,000～80,000元／次
住院手術看護：3,000元／次
門診手術醫療：3,000元／次
特定處置：2,000元／次（168項）
醫材補助：10,000元／次

2. 無理賠回饋金
每年可獲得相當於 一個月保費 的回饋
用意：鼓勵健康管理、提供額外經濟回饋

3. 醫材補助特色
涵蓋八大類醫材補助
包含人工水晶體、關節置換等高額醫材
也包含心臟血管支架、心律調節器等重要醫材
最高給付 10 次

4. 其他保障特點
提供 1–6 級失能豁免保險費
終身型商品，可長期保障
保障範圍完整、理賠項目多元

【回覆規範】
只能根據提供的內容回答。
若使用者詢問超出上述資料的問題（如保費、理賠細節、等待期、核保、除外責任、疾病定義），你必須回答：
「很抱歉，這部分不在我可提供的資訊範圍內。」
若使用者問的是提供內容中的資訊，你需清楚、精準、禮貌地回答。
不得自行推論或補充額外條款內容。
不可以用簡字，你的所有對話內容需要以「繁體中文」進行回覆
"""

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
add_msg(memories, 'SYS', insurance_prompt)
print("保險客服機器人已啟動 (輸入 /bye 離開)...")
while True:
    user_input = input("\n請輸入您的問題：")
    if user_input.strip() == "/bye":
        print("客服結束，祝您順心！")
        break

    # 2. 存使用者的話 (用 'U')
    add_msg(memories, 'USER', user_input)

    # 呼叫模型
    response = chat(model='gemma3:12b', messages=memories, options={
        'temperature': 1.0, 
    })
    answer = response.message.content
    print("客服回答：", answer)

    # 3. 存 AI 的話 (用 'A')
    add_msg(memories, 'AI', answer)
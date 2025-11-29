from ollama import chat

response = chat(model='gemma3:12b', messages=[
  {
    'role': 'user',
    'content': '如果時間是一種味道，那是什麼味道？請在20字以內回答。',
  },
], options={'temperature': 0.0,})

print(response.message.content)
